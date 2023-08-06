import asyncio
import json
import logging
from functools import cache, partial
from typing import List, Union

import pandas as pd
from attrs import define
from merge_args import merge_args  # also makefun has a decorator that does this

from juice_core_uplink_api_client.api.rest_api import (
    rest_api_events_list,
    rest_api_plan_list,
    rest_api_plan_read,
    rest_api_series_list,
    rest_api_trajectory_engineering_segments_list,
    rest_api_trajectory_event_list,
    rest_api_trajectory_series_list,
)
from juice_core_uplink_api_client.client import Client

log = logging.getLogger(__name__)


DEFAULT_START = "2020"
DEFAULT_END = "2040"
DEFAULT_TRAJECTORY = "CREMA_5_1_150lb_23_1"
DEFAULT_URL = "https://juicesoc.esac.esa.int"


def convert_times(table, columns=[]):
    if isinstance(columns, str):
        columns = [columns]

    if len(columns) == 0 or columns is None:
        return table

    for col in columns:
        table[col] = pd.to_datetime(table[col]).dt.tz_localize(None)

    return table


def table_to_timeseries(table, name=None):
    return pd.Series(data=table.value.values, index=table.epoch.values, name=name)


def pandas_convertable(func=None, time_fields=[], is_timeseries=False):
    if func is None:
        return partial(pandas_convertable, time_fields=time_fields, is_timeseries=is_timeseries)

    from copy import copy

    @merge_args(func)
    def wrapper(*args, as_pandas=True, **kwargs):
        time_fields_ = copy(time_fields)

        series_name = None
        if is_timeseries and ("epoch" not in time_fields_):
            time_fields_ += ["epoch"]
            if "series_name" in kwargs:
                series_name = kwargs["series_name"]
            else:
                series_name = args[1]

        result = func(*args, **kwargs)  # call actual function

        # convert to pandas if needed
        if as_pandas:
            table = convert_times(
                pd.DataFrame([d.to_dict() if hasattr(d, "to_dict") else d for d in result]), columns=time_fields_
            )

            if is_timeseries:
                return table_to_timeseries(table, name=series_name)
            else:
                return table

        else:
            return result

    return wrapper


def synchronize_async_helper(to_await):
    async_response = []

    async def run_and_capture_result():
        r = await to_await
        async_response.append(r)

    loop = asyncio.get_event_loop()
    coroutine = run_and_capture_result()
    loop.run_until_complete(coroutine)
    return async_response[0]


@define(auto_attribs=True, eq=False)
class SHTRestInterface:
    """
    Main entry point for interacting with the Juice Core Uplink API
    """

    client: [None, Client] = None
    timeout: float = 40.0

    def __attrs_post_init__(self):
        if not self.client:
            self.client = Client(DEFAULT_URL)
        self.client.timeout = self.timeout

    @cache
    @pandas_convertable(time_fields=["created"])
    def plans(self):
        """Retrieve all the plans available on the endpoint"""
        return rest_api_plan_list.sync(client=self.client)

    def plan_id_by_name(self, name):
        """Retrieve the plan id from the plane name"""
        for plan in self.plans(as_pandas=False):
            if plan.name.lower().strip() == name.lower().strip():
                log.debug(f"Plan {name} has id {plan.id}")
                return plan.id

        log.warning(f"No plan with name {name} found")
        return None

    @cache
    @pandas_convertable(time_fields=["start", "end"])
    def plan_segments(self, plan_id_or_name):
        """Retrieve the segments of a plan"""
        plan = self.plan(plan_id_or_name, as_pandas=False)
        return plan.segments

    @cache
    @pandas_convertable(time_fields=["start", "end"])
    def engineering_segments(self, trajectory=DEFAULT_TRAJECTORY) -> pd.DataFrame:
        """Retrieve the engineering segments for a mnemonic"""
        return rest_api_trajectory_engineering_segments_list.sync(mnemonic=trajectory, client=self.client)

    @cache
    @pandas_convertable
    def plan(self, plan_id_or_name):
        """Retrieve the plan from the plan id or name"""
        if isinstance(plan_id_or_name, str):
            plan_id_or_name = self.plan_id_by_name(plan_id_or_name)
        return rest_api_plan_read.sync(plan_id_or_name, client=self.client)

    @cache
    @pandas_convertable
    def known_series(self, trajectory=DEFAULT_TRAJECTORY):
        """Retrieve all the series available on the endpoint"""
        return rest_api_trajectory_series_list.sync(client=self.client, mnemonic=trajectory)

    @cache
    @pandas_convertable(is_timeseries=True)
    def series(self, series_name, trajectory=DEFAULT_TRAJECTORY, start=DEFAULT_START, end=DEFAULT_END):
        """Retrieve a serie from the endpoint"""

        q = dict(start=str(start), end=str(end), trajectory=trajectory, series=series_name)

        body = json.dumps(q)
        return rest_api_series_list.sync(client=self.client, body=body)

    def series_multi_(self, series_names, trajectory=DEFAULT_TRAJECTORY, start=DEFAULT_START, end=DEFAULT_END):

        loop = asyncio.get_event_loop()
        coroutine = self.series_multi(series_names, trajectory=trajectory, start=start, end=end)
        return loop.run_until_complete(coroutine)

    def series_multi(self, series_names, trajectory=DEFAULT_TRAJECTORY, start=DEFAULT_START, end=DEFAULT_END):
        """Retrieve multiple series from the endpoint"""
        out = []
        for series_name in series_names:
            q = dict(start=str(start), end=str(end), trajectory=trajectory, series=series_name)

            body = json.dumps(q)
            got = rest_api_series_list.asyncio(client=self.client, body=body)
            out.append(got)

        return asyncio.gather(*out)

    @cache
    @pandas_convertable
    def event_types(self, trajectory=DEFAULT_TRAJECTORY):
        """Retrieve all the events applicable for a trajectory"""
        return rest_api_trajectory_event_list.sync(client=self.client, mnemonic=trajectory)

    @cache
    @pandas_convertable(time_fields=["start", "end"])
    def events(
        self,
        mnemonics: Union[List[str], str] = [],
        trajectory: str = DEFAULT_TRAJECTORY,
        start=DEFAULT_START,
        end=DEFAULT_END,
    ):
        """Retrieve events of a given type from the endpoint"""
        if isinstance(mnemonics, str):
            mnemonics = [mnemonics]

        if len(mnemonics) == 0:
            mnemonics = self.event_types(trajectory=trajectory, as_pandas=False)
            mnemonics = [m.name for m in mnemonics]
            log.info(f"Retrieving all known events {mnemonics}")

        q = dict(start=str(start), end=str(end), trajectory=trajectory, mnemonics=mnemonics)

        body = json.dumps(q)
        return rest_api_events_list.sync(client=self.client, body=body)

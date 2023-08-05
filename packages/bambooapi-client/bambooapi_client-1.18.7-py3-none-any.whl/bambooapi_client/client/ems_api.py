"""Energy Management System."""
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

from bambooapi_client.client.helpers import convert_time_index_to_utc
from bambooapi_client.openapi.apis import EMSApi as _EMSApi
from bambooapi_client.openapi.models import EmsOperations, EmsOperationsEnum


class EmsApi:
    """Implementation for '/ems/ endpoints."""

    def __init__(self, bambooapi_client):
        """Initialize defaults."""
        self._bambooapi_client = bambooapi_client
        self._api_instance = _EMSApi(bambooapi_client.api_client)

    def read_ems_operations(
        self,
        site_id: int,
        start_time: datetime,
        end_time: datetime,
        operations: List[EmsOperationsEnum],
    ) -> Dict[str, pd.DataFrame]:
        """Read EMS operations."""
        response = self._api_instance.read_ems_operations(
            site_id=site_id,
            start_time=start_time,
            end_time=end_time,
            operations=operations,
        )
        operations_dfs = {}
        for op_name in map(str, operations):
            if response.get(op_name):
                df = pd.DataFrame.from_records(
                    [row.to_dict() for row in response[op_name]],
                    index='time',
                )
                convert_time_index_to_utc(df)
                operations_dfs[op_name] = df
        return operations_dfs

    def update_ems_operations(
        self,
        site_id: int,
        schedule: Optional[pd.DataFrame] = None,
        responses: Optional[pd.DataFrame] = None,
        profits: Optional[pd.DataFrame] = None,
    ) -> None:
        """Update EMS operations."""
        operations_dict = {
            'schedule': schedule,
            'responses': responses,
            'profits': profits,
        }
        # Remove Nones, convert to records
        operations_dict = {
            k: v.reset_index().to_dict(orient='records')
            for k, v in operations_dict.items()
            if v is not None
        }
        operations = EmsOperations(**operations_dict)
        self._api_instance.update_ems_operations(
            site_id=site_id,
            ems_operations=operations,
        )

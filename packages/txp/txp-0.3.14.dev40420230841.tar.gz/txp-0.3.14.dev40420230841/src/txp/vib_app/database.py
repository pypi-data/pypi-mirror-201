"""
This file contains the definition of data access operations
to pull data from the tabular database.
"""
import txp.common.utils.bigquery_utils as bqutils
from data_objects import *
import datetime

_BIGQUERY_DATASET="telemetry"
_BIGQUERY_TIME_TABLE="vibration"


def get_vibration_plot_current_day(
    tenant_id: str,
    asset_id: str,
    perception: str,
    bq_client,
    num_signals: int = 1000  # number of signals to show from the current day
) -> VibrationCascadeGraph:
    # TODO: Hardcode dates for development

    START_MEX = datetime.datetime(year=2023, month=2, day=10, hour=12, minute=00)
    START_MEX = START_MEX.astimezone(pytz.timezone('America/Mexico_City'))
    END_MEX = datetime.datetime(year=2023, month=2, day=10, hour=14, minute=00)
    END_MEX = END_MEX.astimezone(pytz.timezone('America/Mexico_City'))

    data_req = bqutils.BigQueryDataRequest(
        START_MEX, END_MEX, _BIGQUERY_DATASET, _BIGQUERY_TIME_TABLE,
        tenant_id, asset_id, perception, bq_client
    )

    # get the vibration data in DESC order by observation_timestamp
    vibration_data = data_req.get_data_from_table()
    vibration_data = vibration_data[-num_signals:]  # TODO: add protection of slice out of index

    cascade_graph = VibrationCascadeGraph(
        SampleDistribution.CURRENT_DAY,
        vibration_data,
        asset_id,
        tenant_id
    )

    return cascade_graph

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import plotly.graph_objects as go
from typing import List, Dict
import dash
import txp.vib_app.database as db
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, DiskcacheManager, ctx, Dash
from txp.vib_app.pages.styles import *
import os

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings
from numpy import trapz
import logging
import time
import txp.vib_app.data_objects as entities
import google.cloud.firestore as firestore
from google.oauth2 import service_account
from google.cloud import bigquery
import txp.vib_app.auth as auth

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

#####################################################
# Backend cache for long running callbacks. We configure the local recommended.
# More info here: https://dash.plotly.com/background-callbacks
#####################################################
import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

#####################################################
# Register Page on the dash pages
#####################################################
dash.register_page(__name__)


#####################################################
# Dash Components Declaration
# From here on, you'll see the declaration of components
# that are in the Vibration Analysis View.
# Components that requires input values to render, will be setup
# with the helper function "init_view_components"
#####################################################
X_AXIS_GRAPH_ID = "x-axis-graph"
X_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID = "x-axis-amp-var-for-freq-graph"
X_AXIS_FFT_AREA_VAR_PLOT_ID = "x-axis-fft-area-var-graph"
Y_AXIS_GRAPH_ID = "y-axis-graph"
Y_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID = "y-axis-amp-var-for-freq-graph"
Y_AXIS_FFT_AREA_VAR_PLOT_ID = "y-axis-fft-area-var-graph"
Z_AXIS_GRAPH_ID = "z-axis-graph"
Z_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID = "z-axis-amp-var-for-freq-graph"
Z_AXIS_FFT_AREA_VAR_PLOT_ID = "z-axis-fft-area-var-graph"
X_AXIS_GRAPH_TAB_ID = "x-axis-graph-tab"
Y_AXIS_GRAPH_TAB_ID = "y-axis-graph-tab"
Z_AXIS_GRAPH_TAB_ID = "z-axis-graph-tab"
TRIDIMENSIONAL_GRAPHS_TABS_ID = "3d-graphs-tabs"
TENANT_ID_INPUT_ID = "tenant-id-input"
MACHINE_ID_INPUT_ID = "machine-id-input"
VISUALIZATION_PERIOD_INPUT_ID = "visualization-period-input"
SENSOR_TYPE_INPUT_KEY = "vibration-sensor-input"
SHOW_DATA_BUTTON_ID = "show-data-btn"
SHOW_DATA_BUTTON_SPINNER_ID = "show-data-3d-spinner"
VIEW_TITLE_DIV_ID = "vibration-analysis-div"
LOADING_CONTENT_WRAPPER_ID = "vibration-analysis-view-content-wrapper"
ALL_AXIS_CASCADE_GRAPHS_IDS = [X_AXIS_GRAPH_ID, Y_AXIS_GRAPH_ID, Z_AXIS_GRAPH_ID]
ALL_AXIS_AMP_VAR_FOR_FREQ_IDS = [
    X_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID,
    Y_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID,
    Z_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID,
]
ALL_AXIS_AREA_VAR_IDS = [
    X_AXIS_FFT_AREA_VAR_PLOT_ID,
    Y_AXIS_FFT_AREA_VAR_PLOT_ID,
    Z_AXIS_FFT_AREA_VAR_PLOT_ID,
]

div_view_title = html.Div(
    html.H2("Análisis de Vibraciones"),
    id=VIEW_TITLE_DIV_ID,
)

div_tenant_id = html.Div(
    [html.P("Cliente"), dcc.Dropdown([""], id=TENANT_ID_INPUT_ID, value="")]
)

div_machine_id = html.Div(
    [html.P("Equipo"), dcc.Dropdown([], id=MACHINE_ID_INPUT_ID, value="")]
)

div_visualization_period = html.Div(
    [html.P("Período"), dcc.Dropdown([], id=VISUALIZATION_PERIOD_INPUT_ID, value="")]
)

div_vibration_sensor = html.Div(
    [html.P("Sensor"), dcc.Dropdown([], id=SENSOR_TYPE_INPUT_KEY, value="")]
)

btn_show_data = html.Div(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        id=SHOW_DATA_BUTTON_ID,
                        children=["Ver Datos"],
                        n_clicks=0,
                        color="primary",
                        className="me-1",
                    ),
                    width=2,
                )
            ],
            justify="start",
        ),
    ]
)

data_selection_card_row = dbc.Spinner(
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(div_tenant_id),
                        dbc.Col(div_machine_id),
                        dbc.Col(div_visualization_period),
                        dbc.Col(div_vibration_sensor),
                    ]
                ),
                dbc.Row(btn_show_data),
            ]
        )
    ),
    type="grow",
    color="primary",
    spinner_style={"position": "absolute", "left": "50%", "top": "50px"},
)

X_AXIS_GRAPH_3D_GRAPH = dcc.Graph(
    id=X_AXIS_GRAPH_ID,
)

X_AXIS_AMP_VAR_FOR_FREQ_GRAPH = dcc.Graph(id=X_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID)

X_AXIS_AREA_VAR_GRAPH = dcc.Graph(id=X_AXIS_FFT_AREA_VAR_PLOT_ID)

Y_AXIS_GRAPH_3D_GRAPH = dcc.Graph(
    id=Y_AXIS_GRAPH_ID,
)

Y_AXIS_AMP_VAR_FOR_FREQ_GRAPH = dcc.Graph(id=Y_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID)

Y_AXIS_AREA_VAR_GRAPH = dcc.Graph(id=Y_AXIS_FFT_AREA_VAR_PLOT_ID)

Z_AXIS_GRAPH_3D_GRAPH = dcc.Graph(
    id=Z_AXIS_GRAPH_ID,
)

Z_AXIS_AMP_VAR_FOR_FREQ_GRAPH = dcc.Graph(id=Z_AXIS_AMP_VAR_FOR_FREQ_GRAPH_ID)

Z_AXIS_AREA_VAR_GRAPH = dcc.Graph(id=Z_AXIS_FFT_AREA_VAR_PLOT_ID)

ADD_FAILURE_FREQ_TRACE_INPUT_ID = "add-failure-freq-input"
ADD_FAILURE_FREQ_BTN_ID = "add-failure-freq-button"
ADD_FAILURE_FREQ_INPUT_DIV = html.Div(
    [
        html.P("Ingrese una frecuencia de fallo para marcar la traza"),
        dbc.Input(type="number", min=0, id=ADD_FAILURE_FREQ_TRACE_INPUT_ID),
    ]
)
ADD_FAILURE_FREQ_BTN = dbc.Button(
    id=ADD_FAILURE_FREQ_BTN_ID,
    children=["Añadir Traza"],
    n_clicks=0,
    color="secondary",
    className="me-1",
)


X_AXIS_GRAPH_TAB = dbc.Tab(
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                        dbc.Col(
                            [
                                ADD_FAILURE_FREQ_INPUT_DIV,
                                html.Br(),
                                ADD_FAILURE_FREQ_BTN,
                            ],
                            width=2,
                        ),
                ),
                dbc.Col(X_AXIS_GRAPH_3D_GRAPH, width=10),
                X_AXIS_AREA_VAR_GRAPH,
                X_AXIS_AMP_VAR_FOR_FREQ_GRAPH,
            ]
        )
    ),
    id=X_AXIS_GRAPH_TAB_ID,
    label="Eje X",
)

Y_AXIS_GRAPH_TAB = dbc.Tab(
    dbc.Card(
        dbc.CardBody(
            [
                Y_AXIS_GRAPH_3D_GRAPH,
                Y_AXIS_AREA_VAR_GRAPH,
                Y_AXIS_AMP_VAR_FOR_FREQ_GRAPH,
            ]
        )
    ),
    id=Y_AXIS_GRAPH_TAB_ID,
    label="Eje Y",
)


Z_AXIS_GRAPH_TAB = dbc.Tab(
    dbc.Card(
        dbc.CardBody(
            [
                Z_AXIS_GRAPH_3D_GRAPH,
                Z_AXIS_AREA_VAR_GRAPH,
                Z_AXIS_AMP_VAR_FOR_FREQ_GRAPH,
            ]
        )
    ),
    id=Z_AXIS_GRAPH_TAB_ID,
    label="Eje Z",
)

TRIDIMENSIONAL_GRAPHS_TABS = dbc.Spinner(
    dbc.Tabs(
        [X_AXIS_GRAPH_TAB, Y_AXIS_GRAPH_TAB, Z_AXIS_GRAPH_TAB],
        id=TRIDIMENSIONAL_GRAPHS_TABS_ID,
    ),
    type="grow",
    color="primary",
    spinner_style={"position": "absolute", "left": "50%", "top": "50px"},
    delay_show=250
)

layout_nested_div = html.Div(
    [div_view_title, data_selection_card_row, TRIDIMENSIONAL_GRAPHS_TABS],
    id="vibration-analysis-view-nested",
    style=VISIBILE_STYLE,
)

#####################################################
# Data Store components declaration to hold downloaded
# information.
#####################################################
vibration_store = dcc.Store(id="vibration-data", storage_type="session")


#####################################################
# Declaration of spinner to show load of view the first time
#####################################################
progress_views_transition_spinner = dbc.Spinner(
    color="primary",
    spinner_style=HIDDEN_STYLE,
    id="vibration-analysis-load-spinner",
    size="md",
)


layout = html.Div(
    [layout_nested_div, vibration_store],
    id="vibration-analysis-view",
    style=CONTENT_STYLE,
)


#####################################################
# Dash Callbacks Declaration
# From here on, you'll see the declaration of callbacks
# that connect inputs/outputs based on the components
# declared above.
# https://dash.plotly.com/callback-gotchas
#####################################################
@callback(
    Output(vibration_store, "data"),
    Output(TENANT_ID_INPUT_ID, "options"),
    Output(TENANT_ID_INPUT_ID, "value"),
    Output(MACHINE_ID_INPUT_ID, "options"),
    Output(MACHINE_ID_INPUT_ID, "value"),
    Output(VISUALIZATION_PERIOD_INPUT_ID, "options"),
    Output(VISUALIZATION_PERIOD_INPUT_ID, "value"),
    Output(SENSOR_TYPE_INPUT_KEY, "options"),
    Output(SENSOR_TYPE_INPUT_KEY, "value"),
    Output(
        TRIDIMENSIONAL_GRAPHS_TABS_ID, "children"
    ),  # We don't update. Only for spinner animation
    Input(vibration_store, "data"),
    background=True,
    manager=background_callback_manager,
)
def init_view_data(data):
    log.info("Trying to download information from remote server...")

    if data:
        log.info(f"Remote data is already locally saved in the session.")
        tenant_ids = ["labshowroom-001"]
        machines_id = {"labshowroom-001": list(["Motor_lab"])}
        perceptions = ["VibrationAcceleration", "VibrationSpeed"]
        visualization_periods = ["Día Actual"]
        stored_data = {"vibration-analysis-downloaded": True}
        out_tuple = (
            stored_data,
            tenant_ids,
            tenant_ids[0],
            machines_id[tenant_ids[0]],
            machines_id[tenant_ids[0]][0],
            perceptions,
            perceptions[0],
            visualization_periods,
            visualization_periods[0],
            dash.no_update,
        )
        return out_tuple

    else:
        log.info(f"Pulling information from remote server started...")
        tenant_ids = ["labshowroom-001"]
        machines_id = {"labshowroom-001": list(["Motor_lab"])}
        perceptions = ["VibrationAcceleration", "VibrationSpeed"]
        visualization_periods = ["Día Actual"]
        stored_data = {"vibration-analysis-downloaded": True}
        out_tuple = (
            stored_data,
            tenant_ids,
            tenant_ids[0],
            machines_id[tenant_ids[0]],
            machines_id[tenant_ids[0]][0],
            perceptions,
            perceptions[0],
            visualization_periods,
            visualization_periods[0],
            dash.no_update,
        )
        return out_tuple


@callback(
    Output(X_AXIS_GRAPH_3D_GRAPH, "figure"),
    Output(Y_AXIS_GRAPH_ID, "figure"),
    Output(Z_AXIS_GRAPH_ID, "figure"),
    Input(SHOW_DATA_BUTTON_ID, "n_clicks"),
    Input(ADD_FAILURE_FREQ_BTN_ID, "n_clicks"),
    State(TENANT_ID_INPUT_ID, "value"),
    State(MACHINE_ID_INPUT_ID, "value"),
    State(VISUALIZATION_PERIOD_INPUT_ID, "value"),
    State(SENSOR_TYPE_INPUT_KEY, "value"),
    State(X_AXIS_GRAPH_ID, "figure"),
    State(Y_AXIS_GRAPH_ID, "figure"),
    State(Z_AXIS_GRAPH_ID, "figure"),
    State(ADD_FAILURE_FREQ_TRACE_INPUT_ID, "value"),
    background=True,
    manager=background_callback_manager,
    prevent_initial_call=True,
    running=[(Output(SHOW_DATA_BUTTON_ID, "disabled"), True, False)],
)
def show_vibration_data_3d(
    n_clicks_1st,
    n_clicks_2nd,
    tenant_id,
    machine_id,
    visualization_period,
    perception_selected,
    figure_3d_x,
    figure_3d_y,
    figure_3d_z,
    failure_freq_value
):
    if ctx.triggered_id == SHOW_DATA_BUTTON_ID:
        logging.info("Donwloading data...")
        credentials = service_account.Credentials.from_service_account_file(
            auth.CREDENTIALS_PATH
        )

        bigquery_client = bigquery.Client(
            credentials=credentials, project=credentials.project_id
        )
        graph: entities.VibrationCascadeGraph = db.get_vibration_plot_current_day(
            tenant_id, machine_id, "VibrationAcceleration", bigquery_client
        )

        # ensemble plotly 3d graphs for the dimensions
        plts = graph.get_fig()
        for i in range(graph.num_axis):
            camera = dict(eye=dict(x=5, y=5, z=0.1))
            plts[i].update_layout(
                autosize=True,
                # margin=dict(l=240, r=240, t=120, b=120),
                scene=dict(aspectmode="manual", aspectratio=dict(x=15, y=10, z=3)),
                scene_camera=camera,
                height=720,
            )

        return plts[0], plts[1], plts[2]
    elif ctx.triggered_id == ADD_FAILURE_FREQ_BTN_ID:
        return (
            entities.add_vertical_3d_failure_freq(figure_3d_x, failure_freq_value),
            entities.add_vertical_3d_failure_freq(figure_3d_y, failure_freq_value),
            entities.add_vertical_3d_failure_freq(figure_3d_z, failure_freq_value),
        )


# REGISTER CALLBACK FOR CLICKED DATA ON CASCADE GRAPHS
for i in range(3):
    current_3d_plot_id = ALL_AXIS_CASCADE_GRAPHS_IDS[i]
    current_amp_var_for_freq_plot_id = ALL_AXIS_AMP_VAR_FOR_FREQ_IDS[i]
    current_area_plot = ALL_AXIS_AREA_VAR_IDS[i]

    @callback(
        Output(current_amp_var_for_freq_plot_id, "figure"),
        Input(current_3d_plot_id, "clickData"),
        State(current_3d_plot_id, "figure"),
        prevent_initial_call=True,
    )
    def show_amplitude_for_selected_freq(clickData, figure):
        if "pointNumber" not in clickData["points"][0]:
            return dash.no_update  # The clicked was not in a signal

        x_freq_index = clickData["points"][0]["pointNumber"]
        x_values = []  # dates
        y_values = []  # amplitude
        for scatter_data in figure["data"]:
            if scatter_data["customdata"][0] == entities.SIGNAL_TRACE_TYPE_VALUE:
                y_values.append(scatter_data["z"][x_freq_index])
                x_values.append(scatter_data["x"][x_freq_index])
        graph = entities.FrequencyAmplitudeVariationGraph(
            x_values, y_values, clickData["points"][0]["y"]
        )
        return graph.get_fig()

    @callback(
        Output(current_area_plot, "figure"),
        Input(current_3d_plot_id, "figure"),
        State(current_3d_plot_id, "figure"),
        prevent_initial_call=True,
    )
    def show_area_variation_for_cascade_lines(clickData, figure):
        x_values = []  # dates
        y_values = []  # amplitude
        for scatter_data in figure["data"]:
            if scatter_data["customdata"][0] == entities.SIGNAL_TRACE_TYPE_VALUE:
                area_value = trapz(scatter_data["z"], scatter_data["y"])
                x_values.append(scatter_data["x"][0])
                y_values.append(area_value)

        graph = entities.AreaVariationGraph(x_values, y_values)

        return graph.get_fig()

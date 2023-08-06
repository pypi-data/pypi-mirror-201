import dash_bootstrap_components as dbc
import urllib.parse
from dash import Input, Output, State, dcc, html, dash_table, callback, DiskcacheManager, ctx
import dash
from google.oauth2 import service_account
from txp.common.models import (
    ProjectFirestoreModel,
    get_project_model,
    models_pb2,
    get_assets_metrics, AssetMetrics,
)
from txp.vib_app.pages.styles import *
import txp.vib_app.auth as auth
import logging

# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

dash.register_page(__name__, path="/asset-details")


#####################################################
# Backend cache for long running callbacks. We configure the local recommended.
# More info here: https://dash.plotly.com/background-callbacks
#####################################################
import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)


######################################################
# Dummy component to trigger init callback of the page
######################################################
INIT_CALLBACK_DUMMY_COMPONENT_ID = "dummy-component"
init_callback_dummy_component = html.Div(
    "I'm dummy", id=INIT_CALLBACK_DUMMY_COMPONENT_ID, style={"visibility": "hidden"}
)


#####################################################
# Dash Components Declaration
# From here on, you'll see the declaration of components shown in the
# General Dashboard.
# Components that requires input values to render, will be setup
# with the helper function "init_view_components"
#####################################################
#####################################################
# Page Header Declaration
#####################################################
PAGE_HEADER = html.Div(
    children=[
        html.H1("Detalles de Máquina"),
        html.Br(),  # let a space in the vertical layout
    ]
)


#####################################################
# Declaration of Location element to handle query params
#####################################################
LOCATION_URL = dcc.Location(id='url', refresh=True)


#####################################################
# Declaration of view layout elements
#####################################################

ASSET_CARD_ASSET_ID = 'asset-card-asset-id'
ASSET_CARD_LAST_SEEN_ID = 'asset-card-last-seen'
ASSET_CARD_METRIC_TEMPERATURE_ID = 'asset-card-metric-temperature'
ASSET_CARD_METRIC_RPM_ID = 'asset-card-metric-rpm'
ASSET_CARD_METRIC_WORKED_TIME_ID = 'asset-card-metric-worked-time'


TITLE_DIV = html.H1("Detalles de Equipo")

ASSETS_GROUP_SELECTBOX_ID = 'assets-group-select'
ASSETS_GROUP_SELECTBOX = dcc.Dropdown(
    [],
    id=ASSETS_GROUP_SELECTBOX_ID,
    clearable=False
)

ASSET_SELECTBOX_ID = "asset-select"
ASSET_SELECTBOX = dcc.Dropdown(
    [],
    id=ASSET_SELECTBOX_ID,
    clearable=False
)

SEE_DETAILS_BTN_ID = 'see-details-btn'
SEE_DETAILS_BTN = dbc.Button(
    "Ver Detalles", outline=True, color="primary", id=SEE_DETAILS_BTN_ID
)

ASSET_CARD_ASSET_TR_ID = html.Tr(
    [
        html.Td("Equipo"),
        html.Td("No Disponible", id=ASSET_CARD_ASSET_ID)
    ]
)

ASSET_CARD_LAST_SEEN_TR_ID = html.Tr(
    [
        html.Td("Visto por última vez"),
        html.Td("No Disponible", id=ASSET_CARD_LAST_SEEN_ID)
    ]
)

ASSET_CARD_INFO_TABLE = dbc.Table(
    [html.Tbody([
        ASSET_CARD_ASSET_TR_ID,
        ASSET_CARD_LAST_SEEN_TR_ID
    ])],
    bordered=True
)

ASSET_CARD_METRIC_TEMPERATURE_DIV = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    "Temperatura",
                    className="card-title",
                    style={"font-weight": "bold"},
                ),
                dbc.CardBody(
                    html.Div(
                        "No hay data para mostrar",
                        id=ASSET_CARD_METRIC_TEMPERATURE_ID,
                        style={"font-size": "22px", "color": "green"},
                    )
                )
            ]
        )
    ]
)

ASSET_CARD_METRIC_RPM_DIV = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    "Velocidad",
                    className="card-title",
                    style={"font-weight": "bold"},
                ),
                dbc.CardBody(
                    html.Div(
                        "No hay data para mostrar",
                        id=ASSET_CARD_METRIC_RPM_ID,
                        style={"font-size": "22px", "color": "green"},
                    )
                )
            ]
        )
    ]
)

ASSET_CARD_METRIC_WORKED_TIME_DIV = html.Div(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    "Horas Encendido",
                    className="card-title",
                    style={"font-weight": "bold"},
                ),
                dbc.CardBody(
                    html.Div(
                        "No hay data para mostrar",
                        id=ASSET_CARD_METRIC_WORKED_TIME_ID,
                        style={"font-size": "22px", "color": "green"},
                    )
                )
            ]
        )
    ]
)

ASSET_CARD_CONTAINER = dbc.Spinner(
    [
        dbc.Row([
            dbc.Col(ASSETS_GROUP_SELECTBOX, width=4),
            dbc.Col(ASSET_SELECTBOX, width=4),
            dbc.Col(SEE_DETAILS_BTN, width=4)
        ]),
        html.Br(),
        dbc.Row([
          dbc.Col(
              ASSET_CARD_INFO_TABLE
          )
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                ASSET_CARD_METRIC_TEMPERATURE_DIV
            ),
            dbc.Col(
                ASSET_CARD_METRIC_RPM_DIV
            ),
            dbc.Col(
                ASSET_CARD_METRIC_WORKED_TIME_DIV
            )
        ])
    ],
    type="grow",
    color="primary",
    spinner_style={"position": "absolute", "left": "50%", "top": "50px"},
)


layout = html.Div(
    [
        LOCATION_URL,
        TITLE_DIV,
        html.Br(),
        ASSET_CARD_CONTAINER
    ],
    style=CONTENT_STYLE
)


#####################################################
# Dash Callbacks Declaration
# From here on, you'll see the declaration of callbacks
# that connect inputs/outputs based on the components
# declared above.
# https://dash.plotly.com/callback-gotchas
#####################################################
def _download_project_model() -> ProjectFirestoreModel:
    credentials = service_account.Credentials.from_service_account_file(
        auth.CREDENTIALS_PATH
    )

    project_model = get_project_model(
        credentials,
        [models_pb2.ALWAYS_REQUIRED, models_pb2.IOT_DEVICES_REQUIRED],
        "heinz-001",
    )

    return project_model

# Define the callback to update the content of the current page based on the URL
@callback(
    Output(ASSET_CARD_ASSET_ID, 'children'),
    Output(ASSET_CARD_LAST_SEEN_ID, 'children'),
    Output(ASSET_CARD_METRIC_TEMPERATURE_ID, 'children'),
    Output(ASSET_CARD_METRIC_RPM_ID, 'children'),
    Output(ASSET_CARD_METRIC_WORKED_TIME_ID, 'children'),
    Output(ASSETS_GROUP_SELECTBOX_ID, 'options'),
    Output(ASSETS_GROUP_SELECTBOX_ID, 'value'),
    Output('url', 'search'),
    Output('url', 'pathname'),
    Input('url', 'search'),
    Input(SEE_DETAILS_BTN_ID, 'n_clicks'),
    State("project-model-snapshot", "data"),
    State(ASSETS_GROUP_SELECTBOX_ID, 'value'),
    State(ASSET_SELECTBOX_ID, 'value'),
    State("logged-in-status", "data"),
    background=True,
    manager=background_callback_manager
)
def render_for_url_params(search, n_clicks, data, asset_groups_select, asset_select, login_data):
    if not login_data or \
            not login_data.get('logged-in', False):
        return (
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        "",
        "/login"
    )

    log.info(f"Rendering page. Context invocation by: {ctx.triggered_id}")
    print(f"Rendering page. Context invocation by: {ctx.triggered_id}")\

    if not data or "project-model" not in data:
        logging.info(
            "Local project data was not found in browser. "
            "Connecting to remote DB to get info"
        )

        project_model: ProjectFirestoreModel = _download_project_model()

    else:
        logging.info("Reading project model from local store")
        project_model: ProjectFirestoreModel = ProjectFirestoreModel.from_dict(
            data["project-model"]
        )

    if ctx.triggered_id == SEE_DETAILS_BTN_ID:
        asset_id = asset_select
        assets_group = asset_groups_select

    elif search:
        params = urllib.parse.parse_qs(search[1:])
        asset_id = params.get('asset', [''])[0]
        assets_group = params.get('group', [''])[0]

    else:
        # Grab the first machine
        assets_group = project_model.assets_groups[0].name
        asset_id = project_model.assets_groups[0].assets[0]

    credentials = service_account.Credentials.from_service_account_file(
        auth.CREDENTIALS_PATH
    )
    metric: AssetMetrics = get_assets_metrics(credentials, [asset_id], 'heinz-001')[0]

    ret = (
        f"{metric.asset_id}",
        f"{metric.last_seen}",
        f"{metric.temperature:.2f} C",
        f"{metric.rpm:.2f} RPM",
        f"{metric.worked_hours:.2f} Hrs",
        list(project_model.assets_groups_table.keys()),
        assets_group,
        dash.no_update,
        dash.no_update
    )

    return ret


# Defin the callback for when the user changes the Asset Group Dropdown
@callback(
    Output(ASSET_SELECTBOX_ID, 'options'),
    Output(ASSET_SELECTBOX_ID, 'value'),
    Input(ASSETS_GROUP_SELECTBOX_ID, 'value'),
    State("project-model-snapshot", "data"),
)
def update_assets_dropdown(group_value, data):
    project_model: ProjectFirestoreModel = ProjectFirestoreModel.from_dict(
        data["project-model"]
    )

    options = project_model.assets_groups_table[group_value].assets

    return options, options[0]

"""
    This is the Dash application for Tranxpert UI based.

    The Web Application Dashboard is composed by a Sidebar that's acts as the
        navigation mechanisms between the views.

    Each individual View is contained on it's own file under the
    `pages` folder. Learn more: https://dash.plotly.com/urls#dash-pages
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, DiskcacheManager, Dash
import os
from txp.vib_app.pages.styles import *
import logging
# TODO: This might be a problem. The logging configuration is being taken from `txp` package
from txp.common.config import settings
log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

#####################################################
# Credentials SETUP
# This setup should change for deployed application.
# If deployed inside GCP, then authentication is transparent for client libs.
#####################################################
# CREDENTIALS SETUP
script_path = os.path.realpath(__file__)
root_path = os.path.dirname(os.path.dirname(script_path))
common_path = os.path.join(os.path.dirname(root_path), "txp", "common")
CREDENTIALS_PATH = os.path.join(
    os.path.join(common_path, "credentials"), "pub_sub_to_bigquery_credentials.json"
)


#####################################################
# Backend cache for long running callbacks. We configure the local recommended.
# More info here: https://dash.plotly.com/background-callbacks
#####################################################
import diskcache

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)


#####################################################
# Dash Components Declaration
# From here on, you'll see the declaration of components
# that are used across the app in different views.
#####################################################
#####################################################
# Sidebar Declaration
#####################################################
sidebar = html.Div(
    [
        html.H1("Tranxpert"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Resumen", href="/", active="exact", id='inicio-nav-btn', n_clicks=0),
                dbc.NavLink(
                    "Detalles de Equipo",
                    href="/asset-details",
                    active="exact",
                    id='asset-details-btn',
                    n_clicks=0
                ),
                dbc.NavLink(
                    "Análisis de Vibraciones",
                    href="/vibration-analysis",
                    active="exact",
                    id='vibration-nav-btn',
                    n_clicks=0
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#####################################################
# Data Store components declaration to hold downloaded
# information.
#####################################################
project_model_store = dcc.Store(id="project-model-snapshot", storage_type="session")
logged_in_status = dcc.Store(id='logged-in-status', storage_type="local")


app = dash.Dash(external_stylesheets=[dbc.themes.SIMPLEX])

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SIMPLEX])

app.layout = html.Div([
	sidebar,
    project_model_store,
    logged_in_status,
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)

import dash_bootstrap_components as dbc
from dash import html


def layout():
    return dbc.Container(
        [
            html.H2("Edit / Diff View"),
            dbc.Alert("Edit UI coming soon — Step 8.", color="info"),
        ]
    )

import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import dash_ag_grid as dag


def layout():
    return dbc.Container(
        [
            # Page header
            dbc.Row(
                [
                    dbc.Col(html.H2("Concept Set Library"), width=8),
                    dbc.Col(
                        dbc.Button(
                            "+ New Concept Set",
                            id="btn-new-concept-set",
                            color="primary",
                            className="float-end",
                        ),
                        width=4,
                    ),
                ],
                className="mb-3",
            ),

            # Search and filter bar
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Input(
                            id="search-concept-set",
                            placeholder="Search by name...",
                            type="text",
                            debounce=True,
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Select(
                            id="filter-domain",
                            options=[
                                {"label": "All Domains", "value": ""},
                                {"label": "Drug", "value": "Drug"},
                                {"label": "Condition", "value": "Condition"},
                                {"label": "Measurement", "value": "Measurement"},
                                {"label": "Procedure", "value": "Procedure"},
                                {"label": "Observation", "value": "Observation"},
                            ],
                            value="",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Select(
                            id="filter-status",
                            options=[
                                {"label": "All Statuses", "value": ""},
                                {"label": "Draft", "value": "draft"},
                                {"label": "In Review", "value": "in_review"},
                                {"label": "Final", "value": "final"},
                            ],
                            value="",
                        ),
                        width=3,
                    ),
                ],
                className="mb-4",
            ),

            # Level 1 — Concept Set Library table
            html.Div(id="concept-set-library-table"),

            html.Hr(),

            # Level 2 — Version History (shown when a concept set is selected)
            html.Div(id="version-history-panel", style={"display": "none"},
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.H4(id="selected-concept-set-name"), width=8),
                            dbc.Col(
                                dbc.Button(
                                    "+ New Version",
                                    id="btn-new-version",
                                    color="success",
                                    className="float-end",
                                ),
                                width=4,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(id="version-history-table"),
                ]
            ),

            # Store selected concept set id
            dcc.Store(id="selected-concept-set-id"),
        ],
        fluid=True,
    )

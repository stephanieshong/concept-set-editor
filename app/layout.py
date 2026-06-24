import dash_bootstrap_components as dbc
from dash import html, dcc


def serve_layout():
    return dbc.Container(
        [
            # URL routing
            dcc.Location(id="url", refresh=False),

            # Navigation bar
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.NavbarBrand("Concept Set Editor", href="/"),
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Browse", href="/")),
                            ],
                            navbar=True,
                        ),
                    ]
                ),
                color="dark",
                dark=True,
                className="mb-4",
            ),

            # Page content — swapped by URL callback
            html.Div(id="page-content"),
        ],
        fluid=True,
    )

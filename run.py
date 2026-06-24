from app.app import app as dash_app
from app.layout import serve_layout
from dash import Input, Output
import dash_bootstrap_components as dbc

# Import callbacks so they register with the app
import app.callbacks.browse_callbacks  # noqa: F401
import app.callbacks.edit_callbacks    # noqa: F401

dash_app.layout = serve_layout


@dash_app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    from app.pages.browse import layout as browse_layout
    from app.pages.edit import layout as edit_layout

    if pathname == "/" or pathname == "/browse":
        return browse_layout()
    elif pathname and pathname.startswith("/edit"):
        return edit_layout()
    return dbc.Alert("Page not found.", color="warning")


if __name__ == "__main__":
    dash_app.run(debug=True, port=8050)

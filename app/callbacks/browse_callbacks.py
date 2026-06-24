import dash
from dash import Input, Output, State, callback, dash_table, html, no_update
import dash_bootstrap_components as dbc
from db.session import SessionLocal
from db.models import ConceptSet, ConceptSetVersion


STATUS_BADGE = {
    "draft":     dbc.Badge("📝 Draft",     color="secondary"),
    "in_review": dbc.Badge("🔍 In Review", color="warning"),
    "final":     dbc.Badge("✅ Final",      color="success"),
}


@callback(
    Output("concept-set-library-table", "children"),
    Input("search-concept-set", "value"),
    Input("filter-domain", "value"),
    Input("filter-status", "value"),
)
def render_library(search, domain, status):
    db = SessionLocal()
    try:
        query = db.query(ConceptSet)
        if search:
            query = query.filter(ConceptSet.concept_set_name.ilike(f"%{search}%"))
        if domain:
            query = query.filter(ConceptSet.domain_id == domain)

        concept_sets = query.order_by(ConceptSet.concept_set_name).all()

        if not concept_sets:
            return dbc.Alert("No concept sets found. Click '+ New Concept Set' to create one.", color="info")

        rows = []
        for cs in concept_sets:
            versions = cs.versions
            if status:
                versions = [v for v in versions if v.status == status]

            final_versions = [v for v in cs.versions if v.status == "final"]
            latest = max(cs.versions, key=lambda v: v.created_at) if cs.versions else None
            latest_status = latest.status if latest else "—"

            rows.append(
                html.Tr(
                    [
                        html.Td(
                            html.A(
                                cs.concept_set_name,
                                id={"type": "cs-name-link", "index": cs.id},
                                href="#",
                                style={"cursor": "pointer"},
                            )
                        ),
                        html.Td(cs.domain_id or "—"),
                        html.Td(len(cs.versions)),
                        html.Td(STATUS_BADGE.get(latest_status, latest_status)),
                    ]
                )
            )

        return dbc.Table(
            [
                html.Thead(
                    html.Tr([
                        html.Th("Concept Set Name"),
                        html.Th("Domain"),
                        html.Th("# Versions"),
                        html.Th("Latest Status"),
                    ])
                ),
                html.Tbody(rows),
            ],
            bordered=True,
            hover=True,
            striped=True,
            responsive=True,
        )
    finally:
        db.close()


@callback(
    Output("version-history-panel", "style"),
    Output("selected-concept-set-name", "children"),
    Output("version-history-table", "children"),
    Output("selected-concept-set-id", "data"),
    Input({"type": "cs-name-link", "index": dash.ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def render_version_history(n_clicks):
    from dash import ctx
    import dash

    if not ctx.triggered_id or not any(n_clicks):
        return {"display": "none"}, no_update, no_update, no_update

    concept_set_id = ctx.triggered_id["index"]

    db = SessionLocal()
    try:
        cs = db.get(ConceptSet, concept_set_id)
        if not cs:
            return {"display": "none"}, no_update, no_update, no_update

        versions = sorted(
            cs.versions,
            key=lambda v: (v.version_number is None, -(v.version_number or 0)),
        )

        rows = []
        for v in versions:
            rows.append(
                html.Tr([
                    html.Td(f"v{v.version_number}" if v.version_number else "—"),
                    html.Td(v.version_name or "—"),
                    html.Td(STATUS_BADGE.get(v.status, v.status)),
                    html.Td(
                        f"v{v.parent_version_id}" if v.parent_version_id else "—"
                    ),
                    html.Td(v.author_name or "—"),
                    html.Td(
                        v.created_at.strftime("%Y-%m-%d") if v.created_at else "—"
                    ),
                    html.Td(
                        dbc.ButtonGroup([
                            dbc.Button("View",    size="sm", color="outline-primary",
                                       href=f"/edit?version_id={v.version_id}"),
                            dbc.Button("Compare", size="sm", color="outline-secondary"),
                        ])
                    ),
                ])
            )

        table = dbc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Version #"),
                    html.Th("Version Name"),
                    html.Th("Status"),
                    html.Th("Based On"),
                    html.Th("Author"),
                    html.Th("Date"),
                    html.Th("Actions"),
                ])),
                html.Tbody(rows),
            ],
            bordered=True,
            hover=True,
            striped=True,
            responsive=True,
        )

        return {"display": "block"}, cs.concept_set_name, table, concept_set_id
    finally:
        db.close()

# Technology Stack for the Concept Set Editor

The following technology stack is recommended for building a concept set editor with support for concept hierarchy visualization, concept set comparison, review workflows, and scalable querying of OMOP vocabularies.

| Layer                   | Technology                | Purpose                                                                                            |
| ----------------------- | ------------------------- | -------------------------------------------------------------------------------------------------- |
| Web Framework           | Dash                      | User interface, routing, and callback handling                                                     |
| UI Components           | dash-bootstrap-components | Responsive layouts, forms, collapsible panels, and navigation                                      |
| Tree Visualization      | dash-cytoscape            | Interactive concept hierarchy and concept set difference trees                                     |
| Charts                  | Plotly                    | Visualizations such as Venn diagrams and summary statistics                                        |
| Concept Table           | dash-ag-grid              | Large concept tables with filtering, sorting, and virtual scrolling                                |
| Database ORM            | SQLAlchemy                | Object-relational mapping (ORM) between Python classes and SQL tables; helps prevent SQL injection |
| Database Migrations     | Alembic                   | Database schema versioning and migration management                                                |
| PostgreSQL Adapter      | psycopg2                  | Database connectivity between SQLAlchemy and PostgreSQL                                            |
| Performance Cache       | Flask-Caching             | Caching of resolved concept sets and expensive queries                                             |
| Configuration & Secrets | python-dotenv             | Management of environment variables and database credentials                                       |
| Email Notifications     | smtplib or Flask-Mail     | Reviewer notifications and workflow alerts                                                         |

## Architecture Overview

```text
+------------------------------------------------------+
|                    Dash Web UI                       |
+------------------------------------------------------+
             |                    |
             |                    |
             v                    v
+-------------------+    +------------------------+
|  dash-ag-grid     |    |    dash-cytoscape      |
|  Concept Tables   |    |  Concept Hierarchies   |
+-------------------+    +------------------------+
             |
             v
+------------------------------------------------------+
|                 Dash Callback Layer                  |
+------------------------------------------------------+
             |
             v
+------------------------------------------------------+
|                  SQLAlchemy ORM                      |
+------------------------------------------------------+
             |
             v
+------------------------------------------------------+
|                    PostgreSQL                        |
+------------------------------------------------------+

Supporting Services:
- Alembic for schema migrations
- Flask-Caching for performance optimization
- python-dotenv for configuration management
- Flask-Mail or smtplib for notifications
- Plotly for analytics and visualizations
```

## Benefits of This Stack

* Fully Python-based architecture
* Excellent integration with OMOP vocabulary databases
* Supports interactive concept hierarchy visualization
* Scales to large concept sets through virtualized grids
* Provides robust review and approval workflows
* Easy deployment within institutional environments
* Well-suited for OHDSI, AI-READI, and OMOP-based terminology management applications

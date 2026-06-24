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
## Required Python Packages

| Package                              | Purpose                                                                                    |
| ------------------------------------ | ------------------------------------------------------------------------------------------ |
| `dash` + `dash-bootstrap-components` | Web framework and UI layout/components                                                     |
| `dash-cytoscape`                     | Concept hierarchy diff tree visualization                                                  |
| `dash-ag-grid`                       | Large concept tables with virtual scrolling and filtering                                  |
| `plotly`                             | Interactive Venn diagram visualization                                                     |
| `sqlalchemy` + `alembic`             | Object-relational mapping (ORM) and database schema migrations                             |
| `psycopg2-binary`                    | PostgreSQL database adapter (binary distribution avoids requiring a C compiler on Windows) |
| `flask-caching`                      | Caches resolved concept sets to improve application performance                            |
| `python-dotenv`                      | Loads configuration values from `.env` files into environment variables                    |
| `flask-mail`                         | Sends reviewer notification emails                                                         |
| `requests`                           | Retrieves concept set JSON documents from the Zenodo API                                   |
| `orjson`                             | High-performance JSON serialization and deserialization for large concept sets             |

### Installation

```bash
pip install \
  dash \
  dash-bootstrap-components \
  dash-cytoscape \
  dash-ag-grid \
  plotly \
  sqlalchemy \
  alembic \
  psycopg2-binary \
  flask-caching \
  python-dotenv \
  flask-mail \
  requests \
  orjson
```

## Benefits of This Stack

* Fully Python-based architecture
* Integration with OMOP vocabulary databases
* Supports interactive concept hierarchy visualization
* Scales to large concept sets through virtualized grids
* Provides review and approval workflows of concept set edit and creation
* Provide deployment within institutional environments
* Suited for OHDSI and OMOP-based vocabulary/terminology management applications

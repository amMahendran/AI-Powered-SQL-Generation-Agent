from sqlalchemy import inspect
from local_ai_data_analyst.database.connection import engine

def get_database_context():

    inspector = inspect(engine)

    schema_name = inspector.default_schema_name

    context = {
        "database_dialect": engine.dialect.name.lower(),
        "default_schema": schema_name,
        "tables": [],
        "relationships": []
    }

    table_names = inspector.get_table_names(schema=schema_name)
    view_names = inspector.get_view_names(schema=schema_name)

    # Discover tables and views
    for object_name, object_type in (
        [(name, "table") for name in table_names]
        + [(name, "view") for name in view_names]
    ):

        columns = inspector.get_columns(
            object_name,
            schema=schema_name
        )

        primary_key = (
            inspector.get_pk_constraint(
                object_name,
                schema=schema_name
            )
            if object_type == "table"
            else {}
        )

        table_info = {
            "schema": schema_name,
            "table": object_name,
            "object_type": object_type,
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column.get("nullable", True)
                }
                for column in columns
            ],
            "primary_key": primary_key.get(
                "constrained_columns", []
            )
        }

        context["tables"].append(table_info)

        # Foreign keys are discovered from actual tables
        if object_type == "table":

            foreign_keys = inspector.get_foreign_keys(
                object_name,
                schema=schema_name
            )

            for fk in foreign_keys:
                context["relationships"].append({
                    "from_schema": schema_name,
                    "from_table": object_name,
                    "from_columns": fk.get(
                        "constrained_columns", []
                    ),
                    "to_schema": fk.get("referred_schema"),
                    "to_table": fk.get("referred_table"),
                    "to_columns": fk.get("referred_columns", []),
                    "source": "database_foreign_key"
                })

    return context

def get_database_schema():
    return get_database_context()
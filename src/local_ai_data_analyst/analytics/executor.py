from local_ai_data_analyst.database.connection import engine
import pandas as pd
import sqlglot
from sqlglot import exp
from sqlalchemy import inspect,text

def get_sqlglot_dialect():
    dialect = engine.dialect.name.lower()

    dialect_mapping = {
        "postgresql": "postgres",
        "mysql": "mysql",
        "mariadb": "mysql",
        "sqlite": "sqlite",
        "mssql": "tsql",
        "oracle": "oracle",
        "snowflake": "snowflake",
        "duckdb": "duckdb",
        "bigquery": "bigquery"
    }

    if dialect not in dialect_mapping:
        raise ValueError(
            f"Unsupported SQL dialect: {dialect}"
        )

    return dialect_mapping[dialect]


def validate_sql(sql):
    statements = sqlglot.parse(
        sql,
        read=get_sqlglot_dialect()
    )

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed")

    tree = statements[0]

    if not isinstance(tree, exp.Query):
        raise ValueError("Only read-only queries are allowed")

    if tree.find(exp.Into):
        raise ValueError("SELECT INTO is not allowed")

    # Check whether LIMIT exists
    has_limit = tree.find(exp.Limit) is not None

    # Detect GROUP BY
    has_group_by = tree.find(exp.Group) is not None

    # Detect aggregate functions
    has_aggregate = any(
        isinstance(node, exp.AggFunc)
        for node in tree.walk()
    )

    # Scalar aggregate without GROUP BY returns one row
    scalar_aggregate = has_aggregate and not has_group_by

    if not has_limit and not scalar_aggregate:
        raise ValueError("A LIMIT clause is required")

    # Get actual database tables
    allowed_tables = {
        name.lower()
        for name in inspect(engine).get_table_names()
    }

    # Get CTE names
    cte_names = {
        cte.alias_or_name.lower()
        for cte in tree.find_all(exp.CTE)
    }

    # Get referenced physical tables, excluding CTE names
    referenced_tables = {
        table.name.lower()
        for table in tree.find_all(exp.Table)
        if table.name.lower() not in cte_names
    }

    # Validate physical table access
    if not referenced_tables.issubset(allowed_tables):
        raise ValueError("Query references an unauthorized table")

    return tree.sql(dialect=get_sqlglot_dialect())


def execute_sql(sql):

    safe_sql = validate_sql(sql)

    dialect = engine.dialect.name.lower()

    with engine.connect() as connection:

        with connection.begin():

            if dialect == "postgresql":

                connection.execute(
                    text("SET TRANSACTION READ ONLY")
                )

                connection.execute(
                    text("SET LOCAL statement_timeout='10000ms'")
                )

            else:
                raise NotImplementedError(
                    f"Read-only execution adapter "
                    f"not implemented for {dialect}"
                )

            df = pd.read_sql_query(
                text(safe_sql),
                connection
            )

    return df
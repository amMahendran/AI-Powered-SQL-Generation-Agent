# AI-Powered SQL Generation Agent

## Overview

An AI-powered SQL Generation Agent that converts natural-language business questions into SQL queries using Large Language Models (LLMs) and executes analytical queries against PostgreSQL databases.

The application uses dynamic database schema discovery to provide database context to the LLM, helping generate context-aware SQL queries.

## Features

- Natural-language-to-SQL generation using Google Gemini API
- Dynamic database schema discovery
- Table, column, datatype, and relationship metadata retrieval
- PostgreSQL database integration
- SQL query validation using SQLGlot
- Read-only SQL query execution
- Query result retrieval using Pandas
- Analytical SQL generation, including aggregations, filtering, grouping, CTEs, and window functions

## Technology Stack

- Python
- Google Gemini API
- LangChain
- PostgreSQL
- SQLAlchemy
- SQLGlot
- Pandas
- uv

## Project Structure

```text
src/
└── local_ai_data_analyst/
    ├── analytics/
    │   └── executor.py
    ├── database/
    │   ├── connection.py
    │   └── schema.py
    ├── evaluation/
    │   └── test_questions.py
    ├── llm/
    │   ├── model.py
    │   └── prompt_builder.py
    ├── main.py
    └── __init__.py
```

## Installation

1. Clone the repository.
2. Install Python 3.12 or later, within the supported project version range.
3. Install uv.
4. Install project dependencies:

```bash
uv sync
```

## Environment Configuration

Create a `.env` file using `.env.example` as a template.

Configure:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_postgresql_connection_string
```

Use your own credentials. Never commit your `.env` file.

## Usage

Run the application:

```bash
uv run python -m local_ai_data_analyst.main
```

## Example Business Questions

- Which are the top 10 highest-paid employees?
- What is the average salary by department?
- Which departments have more than five employees?
- Rank employees by salary within each department.
- Find employees earning above their department's average salary.

## Security

The application uses SQLGlot-based query validation and read-only PostgreSQL transaction execution. These safeguards are not a substitute for database permissions, credential protection, and further security testing.

## Current Limitations

- SQL generation accuracy depends on the selected LLM and database schema context.
- Complex relationships may require explicit relationship metadata.
- Query generation and execution should be validated against the target database.

## Future Improvements

- Expand SQL generation evaluation across different datasets.
- Improve handling of complex database relationships.
- Add systematic LLM response and SQL accuracy evaluation.
- Improve error handling and query explanation capabilities.
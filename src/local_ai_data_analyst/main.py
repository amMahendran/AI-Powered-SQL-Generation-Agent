from local_ai_data_analyst.llm.model import ask_llm
from local_ai_data_analyst.analytics.executor import execute_sql
from local_ai_data_analyst.llm.prompt_builder import build_sql_prompt
from local_ai_data_analyst.database.schema import get_database_context

def generate_sql(question):
    # Step 1: Discover database metadata dynamically
    database_context = get_database_context()

    # Step 2: Build the dynamic SQL prompt
    prompt = build_sql_prompt(
        question=question,
        database_context=database_context,
        max_rows=100
    )
    response = ask_llm(prompt)

    # Handle string and structured LLM responses
    if isinstance(response, list):
        response = "".join(
            item.get("text", "")
            for item in response
            if isinstance(item, dict) and item.get("type") == "text"
        )

    if not isinstance(response, str) or not response.strip():
        raise ValueError("The LLM returned an empty or invalid response.")

    sql = response.strip()

    # Step 4: Handle insufficient schema information
    if sql.upper().startswith("INSUFFICIENT_SCHEMA_INFORMATION"):
        return None

    # Step 5: Validate response format
    if not sql.upper().startswith(("SELECT", "WITH")):
        raise ValueError(
            f"Unexpected LLM response: {sql}"
        )
    return sql

def main():
    question = input("Enter your Business question: ")

    try:
        sql = generate_sql(question)

        if sql is None:
            print(
                "Unable to answer this question. "
                "The required information is not available "
                "in the database schema."
            )
        else:
            print("Generated SQL:", sql)

            result = execute_sql(sql)

            print("Query Result:")
            print(result.head(20))

    except Exception as e:
        print(f"Query Rejected or Failed: {e}")


if __name__ == "__main__":
    main()
import openai
import pyodbc
import pandas as pd
from pandasai import PandasAI
from langchain.llms import OpenAI

# Your API key from OpenAI
openai.api_key = 'your-openai-api-key'

# Set up Langchain OpenAI agent
openai_l = OpenAI(api_key=openai.api_key)

# Set up your SQL server and database connection
def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=your_server;DATABASE=your_database;'
        'UID=your_username;PWD=your_password'
    )
    return connection

# Use Langchain's SQL agent to convert NLP to SQL
def nlp_to_sql(nlp_input):
    response = openai_l.query(nlp_input, task_name="sql")
    return response

# Execute the SQL query on your database
def execute_query(query):
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Visualize the database query result using Pandasai
def visualize(df):
    ai = PandasAI(df)
    visualization = ai.explore()
    return visualization

# The main function to integrate all steps
def nlp_to_query_to_visualization(nlp_input):
    # Convert NLP text input to SQL
    sql_query = nlp_to_sql(nlp_input)

    # Execute the SQL query
    df = execute_query(sql_query)

    # Visualize the results
    visualization = visualize(df)

    return visualization

# Example usage
if __name__ == "__main__":
    nlp_input = "Show me the total sales for the last month"
    visualization_result = nlp_to_query_to_visualization(nlp_input)
    print(visualization_result)

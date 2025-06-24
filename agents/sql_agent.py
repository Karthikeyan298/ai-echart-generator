from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from agents.agent_factory import AgentFactory, AgentType
from utils.settings import engine

open_ai_agent = AgentFactory.create_agent(AgentType.OPENAI, """""", "gpt-4o")

db = SQLDatabase(engine)

PREFIX = """You are an agent designed to interact with a SQL database to build the SQL query that should return the final result. 
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.

Must remove LIMIT from the final answer query unless user asks it.
Must ensure you are creating the optimistic query to get the results.

DON'T use the markdown code block for the SQL query. Final answer should be a single SQL query that can be executed on the database.

"""

SQL_SUFFIX = """Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
{agent_scratchpad}"""

agent_executor = create_sql_agent(
    llm=open_ai_agent.model,
    prefix=PREFIX,
    toolkit=SQLDatabaseToolkit(db=db, llm=open_ai_agent.model),
    agent_executor_kwargs={"handle_parsing_errors": True},
    verbose=True,
    max_iterations=10
)


def invoke_sql_agent(query: str):
    response = agent_executor.invoke({"input": query})
    return response


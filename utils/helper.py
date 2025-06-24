import json
import re

import markdown
import psycopg2
from bs4 import BeautifulSoup

from .settings import engine

conn = engine.connect().connection

def markdown_remover(md: str) -> str:
    """
    Function to remove Markdown formatting from a string.
    """
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()


def is_valid_sql_query(query: str) -> bool:
    """
    Function to check if a SQL query is valid.
    This is a placeholder function and should be replaced with actual SQL validation logic.
    """
    # For now, we just check if the query is not empty
    is_correct = False
    cur = conn.cursor()
    try:
        conn.autocommit = False  # Start transaction
        cur.execute(query)  # Your query
        is_correct = True
    except psycopg2.Error as e:
        print("Syntax error:", e.pgerror)
    finally:
        conn.rollback()  # Undo query
        # conn.close()
    return is_correct

def extract_code_blocks(markdown_text):
    # Match code blocks enclosed in triple backticks ``` (with optional language)
    pattern = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)
    return pattern.findall(markdown_text)


def get_echart_options(chart_type, category):
    with open("utils/echarts_options.json", "r") as file:
        json_data = json.load(file)
        for chart in json_data.get(category, []):
            if chart.get("name") == chart_type:
                return chart.get("option", {})


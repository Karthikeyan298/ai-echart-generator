import json

from agents.chart_agents import chart_identifier_agent, echart_option_generator, query_extractor_agent
from agents.sql_agent import invoke_sql_agent
from utils.helper import markdown_remover, is_valid_sql_query, extract_code_blocks, get_echart_options

def start(query: str):

    # Selecting Chart
    yield update_status("Identifying Chart...")
    chart = chart_identifier_agent.invoke(query)
    print(f"Selected Chart: {chart}")
    selected_chart = chart.split(",")
    yield update_status(f"Chart Identified: {selected_chart[1]}")
    result = None
    for attempt in range(0, 3):
        # Generating SQL Query
        yield update_status("Creating Query...")
        result = invoke_sql_agent(query)
        print(f"SQL Query: {result}")

        # Extracting SQL Query
        result = query_extractor_agent.invoke(result)
        print(f"Extracted Query: {result}")
        final_query = markdown_remover(result)
        print(f"Markdown Removed Query: {final_query}")

        # Validating SQL Query
        result = is_valid_sql_query(final_query)
        if result:
            break
        yield update_status(f"Sorry unable to create the valid query. Retry: {attempt}")

    if not result:
        yield update_status("Sorry unable to create the valid query. Try again with different query.")
        return
    # final_query = "SELECT date_trunc('hour', c.time) AS hour, AVG(c.usage_user) AS avg_usage_user, AVG(c.usage_system) AS avg_usage_system, AVG(c.usage_idle) AS avg_usage_idle FROM cpu c JOIN tags t ON c.tags_id = t.id WHERE t.hostname = 'host_76' GROUP BY hour ORDER BY hour"

    yield update_status("Finalized Query")

    # Generating Echart Options
    yield update_status("Generating Chart Options...")

    context = {}
    # Three attempts to generate the echart options
    for _ in range(0, 4):
        try:
            extracted_code = echart_option_generator.invoke(
                f"{final_query}, Chart Type: {chart}, Example: {get_echart_options(selected_chart[0], selected_chart[1])}")
            extracted_code = extract_code_blocks(extracted_code)[0].encode().decode('unicode_escape')
            print(extracted_code)
            exec(extracted_code, {}, context)
            if "echart_options" in context:
                break
        except Exception as e:
            print(f"Error executing code: {e}")


    if 'echart_options' not in context:
        yield update_status("Sorry unable to generate the chart options. Try again with different query.")
        return

    # print(f"Echart Options: {context['echart_options']}")

    yield update_chart_options(context['echart_options'])

    json.dump(context['echart_options'], open("chart_options.json", "w"), indent=4)


def update_status(data):
    return f"event: status\ndata: {data}\n\n"

def update_chart_options(data):
    return f"event: echart\ndata: {json.dumps(data)}\n\n"

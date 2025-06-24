from agents.agent_factory import AgentFactory, AgentType

chart_list = [
    {
        'name': 'line-simple',
        'catagory': 'Line'
    },
    {
        'name': 'bar-simple',
        'catagory': 'Bar'
    },
    {
        'name': 'pie-simple',
        'catagory': 'Pie'
    }
]

chart_identifier_agent = AgentFactory.create_agent(AgentType.LLAMA, f"""
    You are an assistant who can help select the right chart along with its category from the given chart list.
    Your response should have only the name of the chart from the list below.
    Think and select the proper chart that best fits the user query.
    Following is the example the question and response format:
    Question: Show me the distribution of the people using different transportation in the city
    Answer:  <chart-name>, <catagory>


    Charts List:
    {chart_list}
    """, model_name='llama3')

echart_option_generator = AgentFactory.create_agent(AgentType.OPENAI, """
    You are an agent who can generate the python code which can consume the result of the given query and generate the echart options for the given chart.
    Write a python code that get postgres connection url from env CONNECTION_URL and execute the given query then convert the result into echart options.
    Your final response should be a valid python code that can be executed to generate the given chart type from echart.
    Do not use any additional packages other than echarts-python, os,psycopg2 and json. Must import packages before you use in the code. Make sure the generated code is syntactically correct and can be executed without any errors.
    Final echart options should be valid echart options.
    Final echart options should be returned in the variable `echart_options`. Dates should be in the format 'YYYY-MM-DD HH:MM:SS'.
    Do not include any explanation or additional text. 
    Sample echart package usage:
    from echarts import Echart, Legend, Bar, Axis

    chart = Echart('GDP', 'This is a fake chart')
    chart.use(Bar('China', [2, 3, 4, 5]))
    chart.use(Legend(['GDP']))
    chart.use(Axis('category', 'bottom', data=['Nov', 'Dec', 'Jan', 'Feb']))
    chart.use(Tooltip(
    trigger='axis',
    axis_pointer_type='cross',
    formatter='{b0}: {c0}'))
    print(chart.json)

    Query: 
    """, "gpt-4o")

query_extractor_agent = AgentFactory.create_agent(AgentType.LLAMA, """
    Extract the SQL query from the given text without any explanation or additional text or markdown.
    """, "llama3")
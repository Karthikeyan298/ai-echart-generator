import os

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from flask import request, Response, stream_with_context

from workflow.flow import start

app = Flask(__name__)
CORS(app)


# Shared message queue for simplicity
client_queues = {}

@app.route('/sse')
def sse():
    query = request.args.get("query") or "Default Query or Prompt"
    return Response(stream_with_context(start(query)), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)


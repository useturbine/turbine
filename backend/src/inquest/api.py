from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# in-memory database for data source configurations
# replace this with DB
data_sources = {}


@app.route('/status', methods=['GET'])
def status():
    # check status here
    return jsonify({'status': 'ok'})

@app.route('/source/add', methods=['POST'])
def add_data_source():
    data = request.json()

    source_type = data.get('type')
    config = data.get('config')

    if source_type not in ['mongo', 'postgres']:
        return jsonify({'error': 'Invalid data source type'}), 400

    data_sources[source_type] = config
    return jsonify({'message': 'Data source configuration added successfully'}), 201


@app.route('/index/start', methods=['POST'])
def start_indexing():
    # spawn a background process or a task in a job queue
    # This background process would handle the time-consuming task of indexing.

    # process not alive start
    # if alive, return 202
    return jsonify({'message': 'Indexing started'}), 202

@app.route('/source/tokens', methods=['POST', 'GET'])
def source_count_tokens():
    pass


if __name__ == '__main__':
    app.run(debug=True)

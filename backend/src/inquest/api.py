from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# in-memory database for data source configurations
# replace this with DB
data_sources = {}


class Status(Resource):
    def get(self):
        return {'status': 'ok'}, 200


class DataSourceAdd(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True, help="Data source type cannot be blank!")
        self.parser.add_argument('config', type=dict, required=True, help="Configuration cannot be blank!")

    def post(self):
        args = self.parser.parse_args()

        source_type = args['type']
        config = args['config']

        if source_type not in ['mongo', 'postgres']:
            return {'error': 'Invalid data source type'}, 400

        data_sources[source_type] = config
        return {'message': 'Data source configuration added successfully'}, 201


class StartIndexing(Resource):
    def post(self):
        # spawn a background process or a task in a job queue
        # This background process would handle the time-consuming task of indexing.

        # process not alive start
        # if alive, return 202
        return {'message': 'Indexing started'}, 202


# Add other resources as needed...

api.add_resource(Status, '/status')
api.add_resource(DataSourceAdd, '/source/add')
api.add_resource(StartIndexing, '/index/start')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# replace w in-memory db
data_sources = {}

class DataSource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, required=True, choices=['mongo', 'postgres'],
                                 help="Data source type must be 'mongo' or 'postgres'")
        self.parser.add_argument('config', type=dict, required=True, help="Configuration details cannot be blank!")

    def get(self, source_id=None):
        if not source_id:
            return data_sources, 200

        source = data_sources.get(source_id)
        if not source:
            return {"error": "data source not found"}, 404

        return source, 200

    def post(self):
        args = self.parser.parse_args()
        pass

    def put(self, source_id):
        if source_id not in data_sources:
            return {"error": "Data source not found"}, 404

        args = self.parser.parse_args()
        data_sources[source_id].update(args)

        return {'message': f'Data source {source_id} updated successfully'}, 200

    def delete(self, source_id):
        if source_id in data_sources:
            del data_sources[source_id]
            return {'message': f'Data source {source_id} removed successfully'}, 200
        return {"error": "Data source not found"}, 404


class DataSourceSync(Resource):
    def post(self, source_id):
        return {'message': f'Manual sync for data source {source_id} started'}, 202


# Test data source connection
class TestConnection(Resource):
    def __init__(self):
        pass

    def post(self):
        pass

api.add_resource(DataSource, '/source/', '/source/<string:source_id>')
api.add_resource(DataSourceSync, '/source/sync/<string:source_id>')
api.add_resource(TestConnection, '/source/test-connection')

if __name__ == '__main__':
    app.run(debug=True)

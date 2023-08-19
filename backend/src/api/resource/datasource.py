from flask import request
from flask_restful import Resource, reqparse
from src.api.auth import requires_auth, get_user
from src.api.models import DataSource as DataSourceModel
from typing import Optional


class DataSource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            "type",
            type=str,
            required=True,
            choices=["mongo", "postgres"],
            help="Data source type must be either mongo or postgres",
        )
        self.parser.add_argument(
            "config",
            type=dict,
            required=True,
            help="Configuration details for the data source cannot be blank",
        )

    @requires_auth
    def get(self, source_id: Optional[str] = None):
        user = get_user()
        if not source_id:
            data_sources = [
                source.to_dict()
                for source in DataSourceModel.select().where(
                    DataSourceModel.user == user
                )
            ]
            return data_sources, 200

        data_source = DataSourceModel.get_or_none(
            DataSourceModel.id == source_id, DataSourceModel.user == user
        )
        if not data_source:
            return {"error": "Data source not found"}, 404
        return data_source.to_dict(), 200

    @requires_auth
    def post(self):
        args = self.parser.parse_args()
        data_source = DataSourceModel.create(
            type=args["type"], config=args["config"], user=get_user()
        )
        return {"message": f"Data source {data_source.id} created successfully"}, 201

    @requires_auth
    def delete(self, source_id: str):
        data_source = DataSourceModel.get_or_none(
            DataSourceModel.id == source_id, DataSourceModel.user == get_user()
        )
        if data_source:
            data_source.delete_instance()
            return {"message": f"Data source {source_id} removed successfully"}, 200
        return {"error": "Data source not found"}, 404

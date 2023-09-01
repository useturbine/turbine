from flask import Flask
from flask_restful import Api
from src.api.resource.project import Project
from src.api.resource.search import Search
import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level=logging.DEBUG)

"""
api:
- adding project, remove project, update project, get project
- get search
- get logs
"""


api.add_resource(Project, "/project/", "/source/<string:project_id>")
api.add_resource(Search, "/project/<string:project_id>/search")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_restful import Api
from src.api.resource.datasource import DataSource
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
api = Api(app)


api.add_resource(DataSource, "/source/", "/source/<string:source_id>")

if __name__ == "__main__":
    app.run(debug=True)

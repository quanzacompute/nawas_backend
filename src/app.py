from time import sleep

# flask modules
from flask import Flask
from flask_restful import Api

## import model
from src.db.connection import DBConnection
from src.urls import initUrls

app = Flask(__name__)
api = Api(app)
DBConnection.init(app)

initUrls(api)

## INIT
if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")
    DBConnection.close()

# flask modules
from flask import Flask
from flask_restful import Api

## import model
from .models import db
from .urls import initUrls

app = Flask(__name__)
api = Api(app)
db.init(app)

initUrls(api)

## INIT
if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")

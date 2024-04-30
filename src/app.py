from time import sleep
from flask import Flask
from flask_restful import Api

## import model
from src.db.connection import DBConnection
from src.resources.tenant import Tenant
from src.resources.asn import ASN
from src.resources.prefix import Prefix

app = Flask(__name__)
api = Api(app)

## Register resources
api.add_resource(Tenant, "/tenant/<int:id>")
api.add_resource(ASN, "/asn/<int:asn>")
api.add_resource(Prefix, "/prefix/<int:id>")

if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")
    DBConnection.close()

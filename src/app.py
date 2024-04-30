from time import sleep

# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

## import model
from src.db.connection import DBConnection
from src.resources.tenant import Tenant
from src.resources.asn import ASN
from src.resources.prefix import Prefix


app = Flask(__name__)

api = Api(app)
DBConnection.init(app)

## Register resources
api.add_resource(TenantList, "/tenant/")
api.add_resource(TenantByID, "/tenant/id/<int:id>")
api.add_resource(TenantByName, "/tenant/name/<string:name>")
api.add_resource(ASN, "/asn/<int:asn>")
api.add_resource(Prefix, "/prefix/<int:id>")

if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")
    DBConnection.close()

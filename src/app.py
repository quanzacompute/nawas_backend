from time import sleep

# flask modules
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

## import model
from src.db.connection import DBConnection
from src.model.tenant import TenantList, TenantByID, TenantByName
from src.model.asn import ASNList, ASNListByTenant, ASNByASN
from src.model.prefix import PrefixList, PrefixByASN, PrefixByID 


app = Flask(__name__)

api = Api(app)
DBConnection.init(app)

## Register resources

#tenant
api.add_resource(TenantList, "/tenant/")
api.add_resource(TenantByID, "/tenant/<int:id>")
api.add_resource(TenantByName, "/tenant/name/<string:name>")

#asn
api.add_resource(ASNList, "/asn/")
api.add_resource(ASNListByTenant, "/asn/tenant/<int:id>")
api.add_resource(ASNByASN, "/asn/<int:asn>")

#prefix
api.add_resource(PrefixList, "/prefix/")
api.add_resource(PrefixByASN, "/prefix/asn/<int:asn>")
api.add_resource(PrefixByID, "/prefix/<int:id>")


if __name__ == "__main__":
    app.config["DEBUG"] = bool(os.environ.get("DEBUG"))
    app.config["RESTFUL_JSON"] = {
        "ensure_ascii": False
    }
    app.run(host = "0.0.0.0")
    DBConnection.close()

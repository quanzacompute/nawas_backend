from src.db.connection import DBConnection

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse
   
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


class Tenant():
    name = None
    id = None
    
    def __init__(self, id):
        self.id = id

    def __init__(self, id, name):
        self.id = id
        self.name = name

class TenantList(Resource):
    def get(self):
        return_list = []
        cursor = DBConnection.get_cursor()
        cursor.execute("SELECT id, name from tenants;")
        tenants = cursor.fetchall()
        for t in tenants:
            return_list.append({
                "id": t[0],
                "name": t[1]
            })

class TenantById(Resource):

    @marshal_with(resource_fields, envelope='resource')
    def get(self, tenant_id):
        cursor = DBConnection.get_cursor()
        cursor.execute("SELECT id, name from tenants where id={}".format(tenant_id))
        
        for t in cursor.fetchall():
            return Tenant(t["id"], t["name"])

    
    @marshal_with(resource_fields, envelope='resource')
    def post(self, tenant_id):
       cursor = DBConnection.get_cursor()
       args = request.get_json()
       tenant = 

def TenantByName(Resource):

    @marshal_with(resource_fields, envelope='resource')
    def get(self, tenant_name):

    

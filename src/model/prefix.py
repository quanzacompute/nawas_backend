from src.db.connection import DBConnection

from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse

db = DBConnection.get_connection()

class Prefix(db.model):
    ## metadata
    __tablename__ = 'prefix'

    ## columns
    id = db.Column(db.Integer, primary_key=True)
    asn = db.Column(db.Integer, db.ForeignKey('asn.asn'), nullable=False)
    cidr = db.Column(db.String(100), unique=True, nullable=False)  ##ASSUMPTION: unique

prefix_fields = {
    'id': fields.Integer,
    'asn': fields.Integer,
    'cidr': fields.String
}

class PrefixList(Resource):

    @marshal_fields(prefix_fields)
    def get(self):
        prefixes = Prefix.query.all()
        return prefixes, 200
    
    ## CREATE SINGLE PREFIX
    @marshal_fields(prefix_fields)
    def post(self):
        prefix = Prefix.query.filter_by(cidr=args.get('cidr')).first()
        if not prefix:
            new_prefix = Prefix(cidr=args.get('cidr'), asn=args.get('asn'))
            db.session.add(new_prefix)
            db.session.commit()
            
            prefix = Prefix.query.filter_by(cidr=args.get('cidr')).first()
            return prefix, 201
        else:
            return {'error': 'Prefix already exists'}, 409

class PrefixById(Resource):

    @marshal_fields(prefix_fields)
    def get(self, prefix_id):
        prefix = Prefix.get.query(prefix_id)
        if prefix:
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404

    @marshal_fields(prefix_fields)
    ## UPDATE
    def put(self, prefix_id):
        args = get_json()
        prefix = Prefix.get.query(prefix_id)
        if prefix:
            prefix.id = args.get('id', prefix.id)
            prefix.asn = args.get('asn', prefix.asn)
            prefix.cidr = args.get('cidr', prefix.cidr)
            return prefix, 200
        else:
            return {'error': 'Prefix not found'}, 404


    ## DELETE
    def delete(self, prefix_id):
        prefix = Prefix.get.query(prefix_id)
        if prefix:
            db.session.delete(prefix)
            db.session.commit()
            return {'message': 'Prefix deleted succesfully'}, 200
        else:
            return {'error': 'Prefix not found'}, 404

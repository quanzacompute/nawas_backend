## packages
import enum
from flask import jsonify, request, Flask
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import event, desc
from datetime import datetime

## models
from app.models.tenant import Tenant
from app.models.asn import ASN
from app.models.prefix import Prefix

## database
from app import db

#############
### MODEL ###
#############

## Enum representing different possible actions
class ActionType(enum.Enum):
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

## Database model representing a change to prefixes
class PrefixChange(db.Model):
    ## metadata
    __tablename__ = 'prefix_change'

    ## columns
    count = db.Column( db.Integer, primary_key=True) 
    timestamp = db.Column( db.DateTime, nullable=False, server_default=db.func.now())
    asn = db.Column( db.Integer, nullable=True )
    prefix_id = db.Column( db.Integer, nullable=True)
    prefix_name = db.Column(db.String(100), nullable=True)
    action = db.Column( db.Enum(ActionType))
    cidr = db.Column(db.String(100), nullable=True)

    ## inserts a row into prefix_change table using the execute method of connection, to work around sessions in event listeners
    def insert_with_execute(self,conn):
        return conn.execute(PrefixChange.__table__.insert().values(
            prefix_id=self.prefix_id,
            prefix_name=self.prefix_name,
            asn=self.asn,
            cidr=self.cidr,
            action=self.action
        ))

    ## string representation
    def __repr__(self):
        return str(self.__dict__)


## tracks changes after a flush event (when changes are committed to db)
@event.listens_for(Prefix, 'after_insert')
def log_prefix_insert(mapper, connection, target):
    ## process insert
    change = PrefixChange(prefix_id=target.id, asn=target.asn, cidr=target.cidr, prefix_name=target.name, action=ActionType.INSERT)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Insert {}".format(change))

@event.listens_for(Prefix, 'after_update')
def log_prefix_update(mapper, connection, target):
    ## process update
    old_cidr = connection.scalars(
        db.select( Prefix.cidr ).filter_by(id=target.id)
    ).first()
    change = PrefixChange(prefix_id=target.id, asn=target.asn, cidr=target.cidr, prefix_name=target.name, action=ActionType.UPDATE)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Update {}".format(change))

@event.listens_for(Prefix, 'after_delete')
def log_prefix_delete(mapper, connection, target):
    ## process delete
    change = PrefixChange(prefix_id=target.id, asn=target.asn, cidr=target.cidr, prefix_name=target.name, action=ActionType.DELETE)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Delete {}".format(change))


#########
## API ##
#########

## API fields
prefix_change_fields = {
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'asn': fields.Integer,
    'prefix_id': fields.Integer,
    'prefix_name': fields.String,
    'action': fields.String,
    'cidr': fields.String
}

## get prefix changes by prefix
class PrefixChangeById(Resource):
   
    @marshal_with(prefix_change_fields)
    def get(self, id):
        before = request.args.get('before', None)
        after = request.args.get('after', None)

        query = db.session.query(PrefixChange)
        query = query.filter(PrefixChange.prefix_id == id)

        if before: query = query.filter(PrefixChange.timestamp < datetime.fromisoformat(before))
        if after: query = query.filter(PrefixChange.timestamp > datetime.fromisoformat(after))

        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes, 200

## get prefix changes per asn
class PrefixChangeByASN(Resource):
    
    @marshal_with(prefix_change_fields)
    def get(self, asn):
        before = request.args.get('before', None)
        after = request.args.get('after', None)

        ## get all prefix_ids associated with provided asn
        prefix_ids = [ prefix[0] for prefix in db.session.query(Prefix).filter( Prefix.asn == asn ).with_entities(Prefix.id).all() ]

        query = db.session.query(PrefixChange)
        query = query.filter(PrefixChange.asn == asn)
        if before: query = query.filter(PrefixChange.timestamp <= datetime.fromisoformat(before))
        if after: query = query.filter(PrefixChange.timestamp >= datetime.fromisoformat(after))


        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes, 200

## get prefix changes per tenant
class PrefixChangeByTenant(Resource):
    
    @marshal_with(prefix_change_fields)
    def get(self, id):
        before = request.args.get('before', None)
        after = request.args.get('after', None)
        
        # get asns associated with tenant_id, get prefix_ids associated with asns
        asns = [ asn[0] for asn in db.session.query(ASN).filter( ASN.tenant_id == id).with_entities(ASN.asn).all() ]
        
        query = db.session.query(PrefixChange)
        if before: query = query.filter(PrefixChange.timestamp <= datetime.fromisoformat(before))
        if after: query = query.filter(PrefixChange.timestamp >= datetime.fromisoformat(after))
        query = query.filter(PrefixChange.asn.in_( asns ))

        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes


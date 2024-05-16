import enum
from flask import jsonify, request, Flask
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import event
from app.models.prefix import Prefix

from app import db

#############
### MODEL ###
#############

class ActionType(enum.Enum):
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

class PrefixChange(db.Model):
    ## metadata
    __tablename__ = 'prefix_change'

    ## columns
    timestamp = db.Column( db.DateTime, nullable=False, server_default=db.func.now(), primary_key=True )
    prefix_id = db.Column( db.Integer, db.ForeignKey('prefix.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False, primary_key=True)
    action = db.Column( db.Enum(ActionType), primary_key=True )
    old_cidr = db.Column(db.String(100), nullable=True)
    new_cidr = db.Column(db.String(100), nullable=True)


    ## inserts a row into prefix_change table using the execute method of connection, to work around sessions in event listeners
    def insert_with_execute(self,conn):
        return conn.execute(PrefixChange.__table__.insert().values(
            prefix_id=self.prefix_id,
            old_cidr=self.old_cidr,
            new_cidr=self.new_cidr,
            action=self.action
        ))

    def __repr__(self):
        return str(self.__dict__)


## tracks changes after a flush event (when changes are committed to db)
@event.listens_for(Prefix, 'after_insert')
def log_prefix_insert(mapper, connection, target):
    ## process insert
    change = PrefixChange(prefix_id=target.id, new_cidr=target.cidr, action=ActionType.INSERT)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Insert {}".format(change))

@event.listens_for(Prefix, 'after_update')
def log_prefix_update(mapper, connection, target):
    ## process update
    old_cidr = connection.scalars(
        db.select( Prefix.cidr ).filter_by(id=target.id)
    ).first()
    change = PrefixChange(prefix_id=target.id, old_cidr=old_cidr, new_cidr=target.cidr, action=ActionType.UPDATE)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Update {}".format(change))

@event.listens_for(Prefix, 'after_delete')
def log_prefix_delete(mapper, connection, target):
    ## process delete
    change = PrefixChange(prefix_id=target.id, old_cidr=target.cidr, action=ActionType.DELETE)
    change.insert_with_execute(connection)
    current_app.logger.debug("Processing Prefix Delete {}".format(change))


#########
## API ##
#########

prefix_change_fields = {
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'prefix_id': fields.Integer,
    'action': fields.String,
    'old_cidr': fields.String,
    'new_cidr': fields.String
}

class PrefixChangeById(Resource):
   
    @marshal_with(prefix_change_fields)
    def get(self):
        before = datetime.fromisoformat(requests.args.get('before', None))
        after = datetime.formisoformat(requests.args.get('after', None))
        
        query = db.session.query(PrefixChange)
        if before: query.filter(PrefixChange.timestamp <= before)
        if after: query.filter(PrefixChange.timestamp >= after)

        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes, 200


class PrefixChangeByASN(Resource):
    
    @marshal_with(prefix_change_fields)
    def get(self, asn):
        before = datetime.fromisoformat(requests.args.get('before', None))
        after = datetime.formisoformat(requests.args.get('after', None))

        ## get all prefix_ids associated with provided asn
        prefix_ids = [ prefix[0] for prefix in db.session.query(Prefix).filter( asn=asn ).with_entities(Prefix.id).all() ]

        query = db.session.query(PrefixChange)
        if before: query.filter(PrefixChange.timestamp <= before)
        if after: query.filter(PrefixChange.timestamp >= after)

        ## filter for prefix_ids associated with the provided asn
        PrefixChange.prefix_id.in_( prefix_ids )

        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes, 200

class PrefixChangeByTenant(Resource):
    
    @marshal_with(prefix_change_fields)
    def get(self, id):
        before = datetime.fromisoformat(requests.args.get('before', None))
        after = datetime.formisoformat(requests.args.get('after', None))
        
        # get asns associated with tenant_id, get prefix_ids associated with asns
        asns = [ asn[0] for asn in ASN.query.filter_by(tenant_id=id).with_entities(ASN.asn).all() ]
        prefix_ids = [ prefix[0] for prefix in db.session.query(Prefix).filter( Prefix.asn.in_( asns )).with_entities(Prefix.id).all() ]
        
        query = db.session.query(PrefixChange)
        if before: query.filter(PrefixChange.timestamp <= before)
        if after: query.filter(PrefixChange.timestamp >= after)
        PrefixChange.prefix_id.in_( prefix_ids )

        changes = query.order_by(desc(PrefixChange.timestamp)).all()
        return changes


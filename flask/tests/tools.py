import unittest
from datetime import datetime, timedelta
import json
from app import create_app, db

from app.models.tenant import Tenant
from app.models.asn import ASN
from app.models.prefix import Prefix

## General tools for the testcases

class NawasTestCase(unittest.TestCase):
    
    ## get the db session
    def get_session(self):
        return db.session

    ## utility functions 
    def create_tenant(self, tenant_id=1, commit=True):
        tenant = Tenant(id=tenant_id, name="test_tenant{}".format(tenant_id))
        db.session.add(tenant)
        if commit: db.session.commit()
        return tenant
    
    def create_asn(self, tenant, asn_id=1, commit=True):
        asn = ASN(asn=asn_id, tenant_id=tenant.id)
        db.session.add(asn)
        if commit: db.session.commit()
        return asn
    
    def create_prefix(self, asn, prefix_id=1, cidr="8.8.8.8/32", commit=True):
        prefix = Prefix(id=prefix_id, asn=asn.asn, cidr=cidr)
        db.session.add(prefix)
        if commit: db.session.commit()
        return prefix

    ## setup and teardown to use in all testcases
    def setUp(self):
        app = create_app(test=True)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app_context().push()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestDBOperation(NawasTestCase):
    def setUp(self):
        super().setUp()
        self.tenant = self.create_tenant(commit=False)
        self.asn = self.create_asn(self.tenant, commit=False)
        self.prefix = self.create_prefix(self.asn)

class TestAPICall(NawasTestCase):
    ## generate a change to find
    def setUp(self):
        super().setUp()
        self.tenant = self.create_tenant(commit=False)
        self.asn = self.create_asn(self.tenant, commit=False)
        self.prefix = self.create_prefix(self.asn)

        self.before = datetime.now() + timedelta(hours=1)
        self.after = datetime.now() - timedelta(hours=1)

    def get(self, url):
        response = self.app.get(url)

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        return json.loads(response.data)        

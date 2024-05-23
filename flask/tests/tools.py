import unittest
from datetime import datetime, timedelta
import json
from app import create_app, db

from app.models.tenant import Tenant
from app.models.asn import ASN
from app.models.prefix import Prefix
from parameterized import parameterized

## General tools for the testcases
def doc_func(func, num, param):
    return "%s: %s with %s" %(num, func.__name__, param)

def name_func(testcase_func, param_num, param):
    return "%s_%s" %(
        testcase_func.__name__,
        parameterized.to_safe_name(param.args[0])
    )


class GeneralTestCase(unittest.TestCase):
    ## get the db session
    def get_session(self):
        return db.session

    ## utility functions 
    def create_tenant(self, tenant_id=1, tenant_name="test_tenant{}", commit=True):
        tenant = Tenant(id=tenant_id, name=tenant_name.format(tenant_id))
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

class TestAPICall(GeneralTestCase):
    ## generate a change to find

    def get(self, url, expected_status_code=200):
        response = self.app.get(url)

        # check if request was succesfull
        self.assertEqual(response.status_code, expected_status_code)

        # check data
        return json.loads(response.data)

    def post(self, url, data, expected_status_code=201):
        response = self.app.post(url, json=data)

        # check if request was succesfull
        self.assertEqual(response.status_code, expected_status_code)

        # check data
        return json.loads(response.data)
    
    def put(self, url, data, expected_status_code=200):
        response = self.app.put(url, json=data)

        # check if request was succesfull
        self.assertEqual(response.status_code, expected_status_code)

        # check data
        return json.loads(response.data)

    def delete(self, url, expected_status_code=200):
        response = self.app.delete(url)

        # check if request was succesfull
        self.assertEqual(response.status_code, expected_status_code)

        # check data
        return json.loads(response.data)



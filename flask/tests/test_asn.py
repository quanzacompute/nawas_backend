import unittest
from app import app, db
from models.tenant import Tenant
from models.asn import ASN

from tests import tools

class TestASNs(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app_context().push()
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



    def test_create_asn(self):
        tenant=tools.create_tenant(db)

        response = self.app.post('/asn/1', json={'asn': 1, 'tenant_id': tenant.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ASN.query.count(), 1)

    def test_get_asn(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db,tenant)

        response = self.app.get('/asn/1')
        self.assertEqual(response.status_code, 200)

    def test_update_asn(self):
        tenant = tools.create_tenant(db,1)
        tenant2 = tools.create_tenant(db,2)
        asn = tools.create_asn(db,tenant)
        
        new_data = {'asn': 1,  'tenant_id': tenant2.id}

        response = self.app.put('/asn/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_asn = ASN.query.get(1)
        self.assertEqual(updated_asn.tenant_id, tenant2.id)

    def test_delete_asn(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db,tenant)
        
        response = self.app.delete("/asn/{}".format(asn.asn))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ASN.query.get(1))

if __name__ == '__main__':
    unittest.main()


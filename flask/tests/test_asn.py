import unittest
from app import app, db
from models.tenant import Tenant
from models.asn import ASN

class TestASNs(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_tenant(self, tenant_id=1):
        tenant = Tenant(id=tenant_id, name="test_tenant{}".format(tenant_id))
        db.session.add(tenant)
        db.session.commit()
        return tenant

    def create_asn(self, tenant):
        asn = ASN(asn=1, tenant_id=tenant.id)
        db.session.add(asn)
        db.session.commit()
        return asn


    def test_create_asn(self):
        tenant=self.create_tenant()

        response = self.app.post('/asns', json={'asn': 1, 'tenant_id': tenant.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ASN.query.count(), 1)

    def test_get_asn(self):
        tenant = self.create_tenant()
        asn = self.create_asn()

        response = self.app.get('/asn/1')
        self.assertEqual(response.status_code, 200)

    def test_update_asn(self):
        tenant = self.create_tenant(1)
        tenant2 = self.create_tenant(2)
        ans = self.create_asn()
        
        new_data = {'asn': 1,  'tenant_id': tenant2.id}

        response = self.app.post('/asn/id/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_asn = ASN.query.get(1)
        self.assertEqual(updated_asn.tenant_id, tenant2.id)

    def test_delete_asn(self):
        tenant = self.create_tenant()
        asn = self.create_ans()
        
        response = self.app.delete("/asn/id/{}".format(asn.asn))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ASN.query.get(1))

if __name__ == '__main__':
    unittest.main()


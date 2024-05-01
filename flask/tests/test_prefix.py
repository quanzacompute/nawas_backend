import unittest
from app import app, db
from models.tenant import Tenant
from models.asn import ASN
from models.prefix import Prefix

class TestPrefixes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app_context().push()
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

    def create_asn(self, tenant, asn_id=1):
        asn = ASN(asn=asn_id, tenant_id=tenant.id)
        db.session.add(asn)
        db.session.commit()
        return asn

    def create_prefix(self, asn, prefix_id=1, cidr="8.8.8.8/32"):
        prefix = Prefix(id=prefix_id, asn=ans.id, cidr=cidr)
        db.session.add(prefix)
        db.session.commit()

    def test_create_prefix(self):
        tenant=self.create_tenant()
        asn = self.create_asn(tenant)

        response = self.app.post('/prefix', json={'asn': asn.asn, cidr:'255.255.255.255/32'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, cidr:'0.0.0.0/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, cidr:':::::::/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, cidr:'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128'})
        self.assertEqual(response.status_code, 201)

        self.assertEqual(ASN.query.count(), 4)

    def test_get_prefix(self):
        tenant = self.create_tenant()
        asn = self.create_asn(tenant)
        prefix = self.create_prefix(asn)

        response = self.app.get('/prefix/id/1')
        self.assertEqual(response.status_code, 200)

    def test_update_prefix(self):
        tenant = self.create_tenant()
        asn = self.create_asn(tenant)
        prefix = self.create_prefix(asn)
        
        new_data = {'asn': asn.asn, cidr: '8.8.8.8/24'}

        response = self.app.post('/prefix/id/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_asn = ASN.query.get(1)
        self.assertEqual(updated_asn.cidr, '8.8.8.8/24')

    def test_delete_prefix(self):
        tenant = self.create_tenant()
        asn = self.create_ans(tenant)
        prefix = self.create_prefix(asn)
        
        response = self.app.delete("/prefix/id/{}".format(prefix.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ASN.query.get(1))

if __name__ == '__main__':
    unittest.main()


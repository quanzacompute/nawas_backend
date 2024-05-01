import unittest
from app import app, db
from models.tenant import Tenant
from models.asn import ASN
from models.prefix import Prefix

from tests import tools

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

    def test_create_prefix(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db, tenant)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'255.255.255.255/32'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'0.0.0.0/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':':::::::/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128'})
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Prefix.query.count(), 4)

    def test_get_prefix(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db,tenant)
        prefix = tools.create_prefix(db,asn)

        response = self.app.get('/prefix/1')
        self.assertEqual(response.status_code, 200)

    def test_update_prefix(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db,tenant)
        prefix = tools.create_prefix(db,asn)
        
        new_data = {'asn': asn.asn, 'cidr': '8.8.8.8/24'}

        response = self.app.put('/prefix/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_prefix = Prefix.query.get(1)
        self.assertEqual(updated_prefix.cidr, '8.8.8.8/24')

    def test_delete_prefix(self):
        tenant = tools.create_tenant(db)
        asn = tools.create_asn(db,tenant)
        prefix = tools.create_prefix(db,asn)
        
        response = self.app.delete("/prefix/{}".format(prefix.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Prefix.query.get(1))

if __name__ == '__main__':
    unittest.main()


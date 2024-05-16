from app.models.tenant import Tenant
from app.models.asn import ASN
from app.models.prefix import Prefix

from app.tests import tools

class TestPrefix(tools.NawasTestCase):
    def test_create_prefix(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'255.255.255.255/32'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'0.0.0.0/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':':::::::/0'})
        self.assertEqual(response.status_code, 201)

        response = self.app.post('/prefix', json={'asn': asn.asn, 'cidr':'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff/128'})
        self.assertEqual(response.status_code, 201)

        self.assertEqual(self.get_session().query(Prefix).count(), 4)

    def test_get_prefix(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)

        response = self.app.get('/prefix/1')
        self.assertEqual(response.status_code, 200)

    def test_update_prefix(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)
        
        new_data = {'asn': asn.asn, 'cidr': '8.8.8.8/24'}

        response = self.app.put('/prefix/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_prefix = self.get_session().get(Prefix, 1)
        self.assertEqual(updated_prefix.cidr, '8.8.8.8/24')

    def test_delete_prefix(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)
        
        response = self.app.delete("/prefix/{}".format(prefix.id))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.get_session().get(Prefix, 1))



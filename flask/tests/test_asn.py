from app.models.tenant import Tenant
from app.models.asn import ASN
from app.tests import tools

class TestASN(tools.NawasTestCase):
    def test_create_asn(self):
        tenant=self.create_tenant()

        response = self.app.post('/asn/1', json={'asn': 1, 'tenant_id': tenant.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ASN.query.count(), 1)

    def test_get_asn(self):
        tenant = self.create_tenant()
        asn = self.create_asn(tenant)

        response = self.app.get('/asn/1')
        self.assertEqual(response.status_code, 200)

    def test_update_asn(self):
        tenant = self.create_tenant(1)
        tenant2 = self.create_tenant(2)
        asn = self.create_asn(tenant)
        
        new_data = {'asn': 1,  'tenant_id': tenant2.id}

        response = self.app.put('/asn/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_asn = ASN.query.get(1)
        self.assertEqual(updated_asn.tenant_id, tenant2.id)

    def test_delete_asn(self):
        tenant = self.create_tenant()
        asn = self.create_asn(tenant)
        
        response = self.app.delete("/asn/{}".format(asn.asn))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ASN.query.get(1))

if __name__ == '__main__':
    unittest.main()


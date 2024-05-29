from parameterized import parameterized
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from app.models.tenant import Tenant
from app.models.asn import ASN
from app.tests import tools
from app.tests.tools import name_func, doc_func

class TestASN(tools.GeneralTestCase):
    def test_primary_key(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, asn_id=1)

        try:
            self.create_asn(tenant, asn_id=1)
            self.assertFalse(False)
        except IntegrityError:
            self.assertTrue(True)

    def test_update(self):
        tenant1 = self.create_tenant(commit=False, tenant_id=1)
        tenant2 = self.create_tenant(commit=False, tenant_id=2)
        asn = self.create_asn(tenant1)

        asn.tenant_id = tenant2.id
        self.get_session().commit()
    
    def test_delete(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant)

        self.get_session().delete(asn)
        self.get_session().commit()

    def test_delete_with_children(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)

        self.get_session().delete(asn)
        try:
            self.get_session().commit()
            self.assertTrue(False)
        except IntegrityError:
            self.assertTrue(True)

    

class TestASNAPI(tools.TestAPICall):
    
    get_data = [
        [ "root", "/asn", 2, 200 ],
        [ "asn", "/asn/1", 4, 404 ]
    ]
    
    @parameterized.expand(get_data, doc_func=doc_func, name_func=name_func)
    def test_get_asn(self, test_name, endpoint, expected_size,exp_code):
        tenant = self.create_tenant(commit=False)
        asn1 = self.create_asn(tenant, asn_id=1)
        asn2 = self.create_asn(tenant, asn_id=2)
        self.assertNotEqual(asn1.asn, asn2.asn)

        response = self.get(endpoint)
        self.assertEqual(len(response), expected_size)
    
    @parameterized.expand(get_data, doc_func=doc_func, name_func=name_func)
    def test_get_asn_not_exists(self, test_name, endpoint, expected_size, exp_code):
        response = self.get(endpoint, expected_status_code=exp_code)

    def test_create_asn(self):
        tenant = self.create_tenant()
        
        response = self.post('/asn/1', {'name': 'test_asn_post', 'tenant_id': tenant.id })
        self.assertEqual(self.get_session().query(ASN).count(), 1)

    def test_create_asn_exists(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, asn_id=1)
        
        response = self.post('/asn/1', {'tenant_id': tenant.id }, expected_status_code=409)
        self.assertEqual(self.get_session().query(ASN).count(), 1)

    def test_update_asn(self):
        tenant1 = self.create_tenant(commit=False, tenant_id=1)
        tenant2 = self.create_tenant(commit=False, tenant_id=2)
        asn = self.create_asn(tenant1, asn_id=1)

        response = self.put('/asn/1', {'tenant_id': tenant2.id })
        updated_asn = self.get_session().get(ASN, 1)
        self.assertEqual(tenant2.id, updated_asn.tenant_id)
        
    def test_update_asn_not_exists_asn(self):
        tenant1 = self.create_tenant(commit=False, tenant_id=1)
        tenant2 = self.create_tenant(commit=False, tenant_id=2)

        response = self.put('/asn/1', {'tenant_id': tenant2.id }, expected_status_code=404)
    
    def test_update_asn_not_exists_tenant(self):
        tenant1 = self.create_tenant(commit=False)
        asn = self.create_asn(tenant1, asn_id=1)

        response = self.put('/asn/1', {'tenant_id': 999 }, expected_status_code=409)

    def test_delete_asn(self):
        tenant1 = self.create_tenant(commit=False)
        asn = self.create_asn(tenant1)

        response = self.delete('/asn/1')
        self.assertIsNone(self.get_session().get(ASN, 1))

    def test_delete_asn_not_exists(self):
        tenant1 = self.create_tenant(commit=False)

        response = self.delete('/asn/1', expected_status_code=404)

    def test_delete_asn_with_prefixes(self):
        tenant1 = self.create_tenant(commit=False)
        asn = self.create_asn(tenant1,commit=False)
        prefix = self.create_prefix(asn)
        
        response = self.delete('/asn/1', 409)
        self.assertIsNotNone(self.get_session().get(ASN, 1))

if __name__ == '__main__':
    unittest.main()


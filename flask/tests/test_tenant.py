from parameterized import parameterized

from app.models.tenant import Tenant
from app.tests import tools
from app.tests.tools import name_func, doc_func

from sqlalchemy.exc import IntegrityError

class TestTenant(tools.GeneralTestCase):
    
    def test_primary_key(self):
        self.create_tenant(tenant_id=1)
        try:
            self.create_tenant(tenant_id=1)
            self.assertTrue(False)
        except IntegrityError as e:
            self.assertTrue(True)

    def test_unique_name(self):
        self.create_tenant(tenant_name="test123")
        try:
            self.create_tenant(tenant_name="test123")
            self.assertTrue(False)
        except IntegrityError as e:
            self.assertTrue(True)

    def test_update(self):
        tenant = self.create_tenant()

        tenant.name="test123"
        self.get_session().commit() 

    def test_delete(self):
        tenant = self.create_tenant()
        self.get_session().delete(tenant)
        self.get_session().commit()

class TestTenantAPI(tools.TestAPICall):

    data = [
        [ "id", "/tenant", {'name': 'test_tenant1'}, 200 ],
        [ "name", "/tenant/name/test_tenant1", {}, 404 ]
    ]

    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_create_tenant(self, test_name, endpoint, payload, exp_code):
        response = self.post(endpoint, data=payload)
        self.assertEqual(self.get_session().query(Tenant).count(), 1)
    
    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_create_tenant_exists(self, test_name, endpoint, payload, exp_code):
        self.create_tenant(tenant_id=1, tenant_name='test_tenant1')

        response = self.post(endpoint, data=payload, expected_status_code=409)
        self.assertEqual(self.get_session().query(Tenant).count(), 1)
    
    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_get_tenant(self, test_name, endpoint, payload, exp_code):
        tenant = self.create_tenant()

        response = self.get(endpoint)
        self.assertIn('test_tenant1', str(response))

    def test_get_tenant_root(self):
        tenant = self.create_tenant(tenant_id=1)
        tenant = self.create_tenant(tenant_id=2)

        response = self.get('/tenant')
        self.assertEqual(len(response), 2)

    
    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_get_tenant_not_exists(self, test_name, endpoint, payload, exp_code):
        response = self.get(endpoint, expected_status_code=exp_code)

    def test_update_tenant(self):
        tenant = self.create_tenant()

        new_data = { 'name': 'updated_tenant' }
        data = self.put('/tenant/1', data=new_data)
        
        updated_tenant = self.get_session().get(Tenant, 1)  
        self.assertEqual(updated_tenant.name, new_data['name'])
   
    def test_update_tenant_not_exists(self):
        new_data = { 'name': 'updated_tenant' }
        data = self.put('/tenant/1', data=new_data, expected_status_code=404)

    def test_delete_tenant(self):
        tenant = self.create_tenant()

        response = self.app.delete('/tenant/1')
        self.assertIsNone(self.get_session().get(Tenant, 1))



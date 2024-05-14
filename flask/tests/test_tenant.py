from app.models.tenant import Tenant
from app.tests import tools

class TestTenant(tools.NawasTestCase):

    def test_create_tenant(self):
        response = self.app.post('/tenant', json={'name': 'test_tenant'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tenant.query.count(), 1)
    
    def test_create_tenant_by_name(self):
        response = self.app.post('/tenant/name/test_tenant', json={})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tenant.query.count(), 1)

    def test_get_tenant_by_name(self):
        tenant = tools.create_tenant(db)

        response = self.app.get('/tenant/name/test_tenant1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_tenant1', str(response.data))

    def test_get_tenant_by_id(self):
        tenant = self.create_tenant()

        response = self.app.get('/tenant/name/test_tenant1')
        self.assertEqual(response.status_code, 200)

        response = self.app.get("/tenant/1")
        self.assertEqual(response.status_code, 200)

    def test_update_tenant(self):
        tenant = self.create_tenant()

        new_data = { 'name': 'updated_tenant' }
        response = self.app.put('/tenant/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_tenant = Tenant.query.get(1)
        self.assertEqual(updated_tenant.name, new_data['name'])

    def test_delete_tenant(self):
        tenant = self.create_tenant()

        response = self.app.delete('/tenant/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Tenant.query.get(1))


import unittest
from app import app, db
from models.tenant import Tenant

class TestTenants(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.app_context().push()
        self.app = app.test_client()        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_tenant(self):
        response = self.app.post('/tenant', json={'name': 'test_tenant'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tenant.query.count(), 1)

    def test_get_tenant_by_name(self):
        tenant = Tenant(name='test_tenant2')
        db.session.add(tenant)
        db.session.commit()

        response = self.app.get('/tenant/name/test_tenant2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('test_tenant2', str(response.data))

    def test_get_tenant_by_id(self):
        tenant = Tenant(name='test_tenant3')
        db.session.add(tenant)
        db.session.commit()

        response = self.app.get('/tenant/name/test_tenant3')
        self.assertEqual(response.status_code, 200)

        t2_id = response.data['id']
        response = self.app.get("/tenant/id/{}".format(t2_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], t2_id)       
        

    def test_update_tenant(self):
        tenant = Tenant(name='test_tenant4')
        db.session.add(tenant)
        db.session.commit()

        new_data = { 'name': 'updated_tenant' }
        response = self.app.post('/tenant/id/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        updated_tenant = Tenant.query.get(1)
        self.assertEqual(updated_tenant.name, new_data['name'])

    def test_delete_tenant(self):
        tenant = Tenant(name='test_tenant5')
        db.session.add(tenant)
        db.session.commit()

        response = self.app.delete('/tenant/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Tenant.query.get(1))


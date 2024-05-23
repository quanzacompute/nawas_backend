from app.models.tenant import Tenant
from app.models.asn import ASN
from app.models.prefix import Prefix
from app.tests import tools
from app.tests.tools import name_func, doc_func

from sqlalchemy.exc import IntegrityError
from parameterized import parameterized

class TestPrefix(tools.GeneralTestCase):
    def test_primary_key(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn, prefix_id=1)
        
        try:
            prefix = self.create_prefix(asn, prefix_id=1)
            self.assertTrue(False)
        except IntegrityError:
            self.assertTrue(True)
    
    def test_unique(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn, prefix_id=1, cidr="8.8.8.8/32")
        
        try:
            prefix = self.create_prefix(asn, prefix_id=2, cidr="8.8.8.8/32")
            self.assertTrue(False)
        except IntegrityError:
            self.assertTrue(True)

    def test_update(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn, prefix_id=1, cidr="8.8.8.8/32")
        
        prefix.cidr="7.7.7.7/32"
        self.get_session().commit()

    def test_delete(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn, prefix_id=1, cidr="8.8.8.8/32")

        self.get_session().delete(prefix)
        self.get_session().commit()

class TestPrefixAPI(tools.TestAPICall):

    data = [
        [ "root", "/prefix", { "id": 1, "asn": 1, "cidr": "8.8.8.8/32" } ],
        [ "id", "/prefix/1", { "id": 1, "asn": 1, "cidr": "8.8.8.8/32" } ]
    ]

    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_get_prefix(self, test_name, endpoint, data):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a)

        response = self.get(endpoint)
        if isinstance(response, dict):
            self.assertEqual(response["id"], p.id)
        else:
            self.assertEqual(len(response), 1)

    def test_get_prefix_not_exists(self):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a)

        response = self.get('/prefix/2', expected_status_code=404)

    def test_create_prefix(self):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t)
        data = { "asn": 1, "cidr": "7.7.7.7/32" }

        response = self.post('/prefix', data=data)
        self.assertEqual(self.get_session().query(Prefix).count(), 1)

    def test_create_prefix_exists(self):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t)
        p = self.create_prefix(a, prefix_id=1)
        data = { "asn": 1, "cidr": "8.8.8.8/32" }

        response = self.post('/prefix', data=data, expected_status_code=409)
        self.assertEqual(self.get_session().query(Prefix).count(), 1)

    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_update_prefix(self, test_name, endpoint, data):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a, cidr="7.7.7.7/32")

        response = self.put(endpoint, data=data)
        self.assertEqual(p.cidr, response["cidr"])
        self.assertEqual(p.id, response["id"])

    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_update_prefix_not_exists(self, test_name, endpoint, data):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a, prefix_id=2, cidr="7.7.7.7/32")

        response = self.put(endpoint, data=data, expected_status_code=404)
    
    @parameterized.expand(data, doc_func=doc_func, name_func=name_func)
    def test_update_prefix_not_exists_asn(self, test_name, endpoint, data):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, asn_id=2, commit=False)
        p = self.create_prefix(a)

        response = self.put(endpoint, data=data, expected_status_code=409)

    def test_delete_prefix(self):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a)
        
        response = self.delete('/prefix/1')
        self.assertEqual(self.get_session().query(Prefix).count(), 0)
    
    def test_delete_prefix(self):
        t = self.create_tenant(commit=False)
        a = self.create_asn(t, commit=False)
        p = self.create_prefix(a)
        
        response = self.delete('/prefix/2', expected_status_code=404)
        self.assertEqual(self.get_session().query(Prefix).count(), 1)



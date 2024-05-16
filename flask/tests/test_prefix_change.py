import unittest
from app import db
from app.models.prefix import Prefix
from app.models.prefix_change import PrefixChange, ActionType
from datetime import datetime, timedelta
import json
from parameterized import parameterized

from app.tests import tools


class TestPrefixChange(tools.NawasTestCase):

    def test_insert_prefix_change(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)

        # assert single insert
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.INSERT).count(), 1)

        # assert only inserts were made
        self.assertEqual(PrefixChange.query.count(), 1)

    def test_update_prefix_change(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)
        
        ## execute update
        prefix.cidr = "9.9.9.9/32"
        db.session.commit()

        # assert single insert
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.INSERT).count(), 1)
        
        # assert single update
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.UPDATE).count(), 1)

        # assert two changes were made
        self.assertEqual(PrefixChange.query.count(), 2)

    def test_delete_prefix_change(self):
        tenant = self.create_tenant(commit=False)
        asn = self.create_asn(tenant, commit=False)
        prefix = self.create_prefix(asn)

        ## assert insert has happened
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.INSERT).count(), 1)

        ## delete prefix
        db.session.delete(prefix)
        db.session.commit()

        ## assert delete message has been placed
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.DELETE).count(), 1)

        ## assert insert has been preserved
        self.assertEqual(PrefixChange.query.filter_by(action=ActionType.INSERT).count(), 1)

class TestPrefixChangeAPICall(tools.TestAPICall):
    endpoints = [
        ["prefix", 1 ],
        ["asn", 1 ],
        ["tenant", 1 ]
    ]

    @parameterized.expand(endpoints)
    def test_get_prefix_change(self, endpoint, id):
        data = self.get('/{}/change/{}'.format(endpoint, id))
        self.assertEqual(data[0]['prefix_id'],1)        

    @parameterized.expand(endpoints)
    def test_get_prefix_change_before_time(self, endpoint, id):
        data = self.get('/{}/change/{}?before={}'.format(endpoint, id, self.before.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    @parameterized.expand(endpoints)
    def test_get_prefix_change_before_time_empty(self,endpoint, id):
        data = self.get('/{}/change/{}?before={}'.format(endpoint, id, self.after.isoformat()))
        self.assertEqual(len(data),0)        

    @parameterized.expand(endpoints)
    def test_get_prefix_change_after_time(self, endpoint, id):
        data = self.get('/{}/change/{}?after={}'.format(endpoint, id, self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    @parameterized.expand(endpoints)
    def test_get_prefix_change_after_time_empty(self, endpoint, id):
        data = self.get('/{}/change/{}?after={}'.format(endpoint, id, self.before.isoformat()))
        self.assertEqual(len(data),0)        
    
    @parameterized.expand(endpoints)
    def test_get_prefix_change_range(self, endpoint, id):
        data = self.get('/{}/change/{}?before={}&after={}'.format(endpoint, id, self.before.isoformat(), self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    @parameterized.expand(endpoints)
    def test_get_prefix_change_range_empty(self, endpoint, id):
        data = self.get('/{}/change/{}?before={}&after={}'.format(endpoint, id, self.after.isoformat(), self.before.isoformat()))
        self.assertEqual(len(data),0)        

if __name__ == '__main__':
    unittest.main()

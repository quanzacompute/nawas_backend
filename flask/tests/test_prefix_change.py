import unittest
from app import db
from app.models.prefix import Prefix
from app.models.prefix_change import PrefixChange, ActionType
from datetime import datetime, timedelta
import json

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


class TestPrefixChangeById(tools.TestAPICall):
        
    def test_prefix_change_by_id(self):
        data = self.get('/prefix/change/{}'.format(self.prefix.id))
        self.assertEqual(data[0]['prefix_id'],1)        

    def test_prefix_change_by_id_before_time(self):
        data = self.get('/prefix/change/{}?before={}'.format(self.prefix.id, self.before.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_id_before_time_empty(self):
        data = self.get('/prefix/change/{}?before={}'.format(self.prefix.id, self.after.isoformat()))
        self.assertEqual(len(data),0)        

    def test_prefix_change_by_id_after_time(self):
        data = self.get('/prefix/change/{}?after={}'.format(self.prefix.id, self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_id_after_time_empty(self):
        data = self.get('/prefix/change/{}?after={}'.format(self.prefix.id, self.before.isoformat()))
        self.assertEqual(len(data),0)        
    
    def test_prefix_change_by_id_range(self):
        data = self.get('/prefix/change/{}?before={}&after={}'.format(self.prefix.id, self.before.isoformat(), self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_id_range_empty(self):
        data = self.get('/prefix/change/{}?before={}&after={}'.format(self.prefix.id, self.after.isoformat(), self.before.isoformat()))
        self.assertEqual(len(data),0)        


class TestPrefixChangeByASN(tools.TestAPICall):
    
    def test_prefix_change_by_asn(self):
        data = self.get('/asn/change/{}'.format(self.asn.asn))
        self.assertEqual(data[0]['prefix_id'],1)        

    def test_prefix_change_by_asn_before_time(self):
        data = self.get('/asn/change/{}?before={}'.format(self.asn.asn, self.before.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_asn_before_time_empty(self):
        data = self.get('/asn/change/{}?before={}'.format(self.asn.asn, self.after.isoformat()))
        self.assertEqual(len(data),0)        

    def test_prefix_change_by_asn_after_time(self):
        data = self.get('/asn/change/{}?after={}'.format(self.asn.asn, self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_asn_after_time_empty(self):
        data = self.get('/asn/change/{}?after={}'.format(self.asn.asn, self.before.isoformat()))
        self.assertEqual(len(data),0)        
    
    def test_prefix_change_by_asn_range(self):
        data = self.get('/asn/change/{}?before={}&after={}'.format(self.asn.asn, self.before.isoformat(), self.after.isoformat()))
        self.assertEqual(data[0]['prefix_id'],1)        
    
    def test_prefix_change_by_asn_range_empty(self):
        data = self.get('/asn/change/{}?before={}&after={}'.format(self.asn.asn, self.after.isoformat(), self.before.isoformat()))
        self.assertEqual(len(data),0)        

#class TestPrefixChangeByTenant(tools.NawasTestCase):


if __name__ == '__main__':
    unittest.main()

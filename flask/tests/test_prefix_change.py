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


class TestPrefixChangeById(tools.NawasTestCase):
    ## generate a change to find
    def setUp(self):
        super().setUp()
        self.tenant = self.create_tenant(commit=False)
        self.asn = self.create_asn(self.tenant, commit=False)
        self.prefix = self.create_prefix(self.asn)

        self.before = datetime.now() + timedelta(hours=1)
        self.after = datetime.now() - timedelta(hours=1)
        

    def test_prefix_change_by_id(self):
        response = self.app.get('/prefix/change/{}'.format(self.prefix.id))

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        data = json.loads(response.data)
        self.assertEqual(data[0]['prefix_id'],1)        

    def test_prefix_change_by_id_before_time_empty(self):
        print("Empty test")
        response = self.app.get('/prefix/change/{}?before={}'.format(self.prefix.id, self.after.isoformat()))

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        data = json.loads(response.data)
        self.assertEqual(len(data),0)
    
    def test_prefix_change_by_id_before_time(self):
        response = self.app.get('/prefix/change/{}?before={}'.format(self.prefix.id, self.before.isoformat()))

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        data = json.loads(response.data)
        self.assertEqual(data[0]['prefix_id'],1)        

    def test_prefix_change_by_id_after_time(self):
        response = self.app.get('/prefix/change/{}?after={}'.format(self.prefix.id, self.after.isoformat()))

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        data = json.loads(response.data)
        self.assertEqual(data[0]['prefix_id'],1)        

    
    def test_prefix_change_by_id_between_time(self):
        response = self.app.get('/prefix/change/{}?before={}&after={}'.format(self.prefix.id, self.before.isoformat(), self.after.isoformat()))

        # check if request was succesfull
        self.assertEqual(response.status_code, 200)

        # check data
        data = json.loads(response.data)
        self.assertEqual(data[0]['prefix_id'],1)        


#class TestPrefixChangeByASN(tools.NawasTestCase):


#class TestPrefixChangeByTenant(tools.NawasTestCase):


if __name__ == '__main__':
    unittest.main()

from django.test import TestCase, Client

import time
from datetime import datetime
import json

from birdspotter.accounts.tests import (create_testuser)
from .models import Dataset

def create_test_dataset(owner):
    dataset = Dataset.objects.create(name=str(time.time()).replace('.', ''),
                                    owner=owner, date_collected=datetime.now().date())
    return dataset


class ShareDatasetTests(TestCase):
    """
    Tests for the sharing of datasets using dataio.views.share_dataset
    """

    def  create_session(self):
        """
        Set up the test client with what will be the current user
        """
        user, creds = create_testuser()
        self.client = Client()
        logged_in = self.client.login(username=creds['username'], password=creds['password'])
        self.assertTrue(logged_in)
        return user


    def test_verify_users(self):
        """
        Verify that making a get request to /share/<dataset_id>/ reuturns
        a json object of all users
        """
        owner = self.create_session()
        users = []
        for _ in range(10):
            users.append(create_testuser()[0])
        dataset = create_test_dataset(owner)
        url = f'/share/{dataset.dataset_id}/'
        # get request should return a json object with a list of users
        resp = self.client.get(url)
        resp_usernames = [u['username'] for u in json.loads(resp.content)['users']]
        # check that the users array and the returned users match (using usernames)
        self.assertEqual(len(list(filter(lambda u:u.username not in resp_usernames, users))), 0)

    def test_share_dataset(self):
        """
        Test that a dataset can be shared with another user
        """
        owner = self.create_session()
        dataset = create_test_dataset(owner)
        user2, _ = create_testuser()
        url = f'/share/{dataset.dataset_id}/'
        self.client.post(url, {"add_share[]": [user2.user_id]})
        self.assertTrue(dataset.shared_with.filter(username=user2.username).exists())

    def test_remove_share_dataset(self):
        """
        Test that removing a user for share works
        """
        owner = self.create_session()
        dataset = create_test_dataset(owner)
        user2, _ = create_testuser()
        # add user2 to dataset.shared_with
        dataset.shared_with.add(user2)
        dataset.save()
        # ensure that user2 is added to shared with
        self.assertTrue(dataset.shared_with.filter(username=user2.username).exists())
        url = f'/share/{dataset.dataset_id}/'
        self.client.post(url, {'remove_share[]': [user2.user_id]})
        self.assertFalse(dataset.shared_with.filter(username=user2.username).exists())

    def test_shared_json(self):
        """
        Test that sharing a dataset is reflected in the share GET request json data
        """
        owner = self.create_session()
        dataset = create_test_dataset(owner)
        user2, _ = create_testuser()
        # add user2 to dataset.shared_with
        dataset.shared_with.add(user2)
        self.assertTrue(dataset.shared_with.filter(username=user2.username).exists())
        url = f'/share/{dataset.dataset_id}/'
        # get share uses for dataset
        resp = self.client.get(url)
        data = json.loads(resp.content)
        # get json object for user
        user = list(filter(lambda u: u['username'] == user2.username, data['users']))[0]
        self.assertTrue(user['is_shared'])

class SharingPermissionTests(TestCase):
    """
    Tests related to a user who is shared a dataset and that user's permissions
    to perform different actions. Mainly ensuring that Editing, Sharing, and Queuing
    are disabled for the shared user
    """

    def create_session(self):
        """
        Create a dataset and owner, along with the test user to be used for the test
        """
        owner, _ = create_testuser()
        dataset = create_test_dataset(owner)
        test_user, creds = create_testuser()
        dataset.shared_with.add(test_user)
        dataset.save()
        self.client = Client()
        logged_in = self.client.login(username=creds['username'], password=creds['password'])
        self.assertTrue(logged_in)
        return test_user, dataset

    def test_share_permissions(self):
        """
        Test that the shared with user will not be able to share the dataset
        Check both GET and POST requests to the /share/<dataset_id> endpoint
        """
        _, dataset = self.create_session()
        url = f'/share/{dataset.dataset_id}/'
        resp = self.client.get(url)
        # 403 is status code for 'Forbidden'
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post(url, {'add_share[]': [create_testuser()[0].user_id],
                                        'remove_share[]': [create_testuser()[0].user_id]})
        self.assertEqual(resp.status_code, 403)

    def test_edit_permissions(self):
        """
        Test that a shared user cannot edit a dataset
        """
        _, dataset = self.create_session()
        url = f'/edit/{dataset.dataset_id}'
        resp = self.client.get(url)
        self.assertTrue('/accounts/login' in resp.url)
        resp = self.client.post(url, {'name': 'test', 'is_public': 'on'})
        self.assertTrue('/accounts/login' in resp.url)

    def test_queue_permissions(self):
        """
        Test that a shared user cannot queue a dataset for analysis
        """
        _, dataset = self.create_session()
        url = f'/queue/{dataset.dataset_id}'
        resp = self.client.get(url)
        self.assertTrue('/accounts/login' in resp.url)

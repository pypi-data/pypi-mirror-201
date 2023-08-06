import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
import datetime
from pkg_resources import resource_string

from ..models import Booklet, Annotation

from .data.target_url.realsites import real_sites

from .data.target_url.needlerealsites import needle_real_sites


class TestBookletList(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def buildUser(self, username):
        user = LDPUser(email=username + '@test.startinblox.com', first_name='Test', last_name='Mactest',
                       username=username,
                       password='glass onion')
        user.save()
        return user

    def test_booklet_list_as_owner(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        self.store_booklet([user1], [user2])
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 1)

    def test_booklet_list_as_contributor(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        self.store_booklet([user2], [user1])
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 1)


    def test_booklet_list_hide_as_non_owner(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        self.store_booklet([user2], [])
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 0)

    def test_booklet_list_hide_as_non_contributor(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        self.store_booklet([], [user2])
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 0)

    def test_booklet_list_hide_non_public_for_anonymous(self):
        user1 = self.buildUser('user1')
        self.store_booklet([user1], [])

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 0)

    def test_booklet_list_show_public_for_anonymous(self):
        user1 = self.buildUser('user1')
        self.store_booklet([user1], [], public=True)

        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 1)

    def test_booklet_list_show_collaboration_allowed_no_annotation(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        self.store_booklet([user1], [], collaboration=True)

        self.client.force_authenticate(user2)
        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 0)

    def test_booklet_list_show_collaboration_allowed_annotation_added(self):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        annotation = Annotation(creator=user2)
        annotation.save()

        booklet = self.store_booklet([user1], [], collaboration=True)
        booklet.annotations.add(annotation)

        self.client.force_authenticate(user2)
        response = self.client.get(
            "/booklets/",
            content_type='application/ld+json',
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_value['ldp:contains']), 1)

    def store_booklet(self, owners, contributors, public = False, collaboration = False):
        booklet = Booklet(
            title="title",
            abstract="",
            accessibility_public=public,
            collaboration_allowed=collaboration,
            cover=1,
        )
        booklet.save()
        for owner in owners:
            booklet.owners.add(owner)
        for contributor in contributors:
            booklet.contributors.add(contributor)

        return booklet

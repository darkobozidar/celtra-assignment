from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from rest_framework import status

from .base import RestViewTestBase
from ...models import Ad, Folder


class AdListViewTestBase():
    """Common class for AdListView test classes."""

    def setUp(self):
        self._request_url = reverse('ad-list')
        self._root_folder = mommy.make(Folder, parent=None)


class AdListViewReadTestBase(AdListViewTestBase, RestViewTestBase, TestCase):
    """Tests for view AdListView for operation Read."""

    def test_response_contains_expected_data(self):
        ad = mommy.make(Ad, folder=self._root_folder)
        _, response_data = self._get_request(self._request_url)

        self.assertEqual(ad.pk, response_data[0]['pk'])
        self.assertEqual(ad.name, response_data[0]['name'])
        self.assertEqual(ad.ad_url, response_data[0]['ad_url'])
        self.assertEqual(ad.folder.pk, response_data[0]['folder'])

    def test_response_returns_only_active_folders(self):
        mommy.make(Ad, folder=self._root_folder)
        mommy.make(Ad, folder=self._root_folder)
        mommy.make(Ad, folder=self._root_folder, is_active=False)

        _, response_data = self._get_request(self._request_url)

        self.assertEqual(2, len(response_data))


class AdListViewCreateTestBase(AdListViewTestBase, RestViewTestBase, TestCase):
    """Tests for view AdListView for operation Create."""

    def test_correctly_creates_new_ad(self):
        post_data = self._ad_data_dict({'folder': self._root_folder.pk})

        self._post_request(self._request_url, data=post_data)
        new_ad = Ad.objects.latest('time_created')

        self.assertEqual(post_data['name'], new_ad.name)
        self.assertEqual(post_data['ad_url'], new_ad.ad_url)
        self.assertEqual(post_data['folder'], new_ad.folder.pk)

    def test_creates_active_ad(self):
        post_data = self._ad_data_dict({'folder': self._root_folder.pk})

        self._post_request(self._request_url, data=post_data)
        new_ad = Ad.objects.latest('time_created')

        self.assertTrue(new_ad.is_active)

    def test_cannot_create_ad_with_inactive_folder(self):
        folder = mommy.make(Folder, is_active=False)
        post_data = self._ad_data_dict({'folder': folder.pk})

        response, response_data = self._post_request(request_url=self._request_url, data=post_data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

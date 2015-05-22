from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from model_mommy import mommy
from rest_framework import status

from .base import RestViewTestBase
from ...models import Ad, Folder


class FolderAdViewTest(RestViewTestBase, TestCase):
    """Tests for view FolderAdView."""

    def setUp(self):
        self._root_folder = mommy.make(Folder, parent=None)
        self._child_folder_1 = mommy.make(Folder, parent=self._root_folder)
        self._child_folder_2 = mommy.make(Folder, parent=self._root_folder)

        self._factory = RequestFactory()

    def _get_request_url(self, pk):
        return reverse('folder-ad-detail', args=(pk,))

    def test_returns_expected_data_about_current_folder(self):
        _, response_data = self._get_request(self._get_request_url(self._root_folder.pk))

        self.assertEqual(self._root_folder.pk, response_data['pk'])
        self.assertEqual(self._root_folder.name, response_data['name'])
        self.assertEqual(self._root_folder.parent, response_data['parent'])

    def test_doesnt_return_inactive_folder(self):
        self._child_folder_1.is_active = False
        self._child_folder_1.save()

        response, _ = self._get_request(self._get_request_url(self._child_folder_1.pk))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_returns_expected_data_about_child_folders(self):
        self._child_folder_2.is_active = False
        self._child_folder_2.save()

        request = self._factory.get(self._get_request_url(self._root_folder.pk))
        _, response_data = self._get_request(self._get_request_url(self._root_folder.pk))
        child_folder_1 = response_data['children'][0]
        expected_url = reverse('folder-ad-detail', args=(self._child_folder_1.pk,))
        expected_url = request.build_absolute_uri(expected_url)

        self.assertEqual(expected_url, child_folder_1['url'])
        self.assertEqual(self._child_folder_1.name, child_folder_1['name'])

    def test_returns_only_active_child_folders(self):
        mommy.make(Folder, parent=self._root_folder, is_active=False)
        _, response_data = self._get_request(self._get_request_url(self._root_folder.pk))

        self.assertEqual(2, len(response_data['children']))

    def test_returns_expected_data_about_ads(self):
        ad = mommy.make(Ad, folder=self._root_folder)

        _, response_data = self._get_request(self._get_request_url(self._root_folder.pk))
        ad_dict = response_data['ads'][0]

        self.assertEqual(ad.name, ad_dict['name'])
        self.assertEqual(ad.ad_url, ad_dict['ad_url'])

    def test_returns_only_active_ads(self):
        mommy.make(Ad, folder=self._root_folder)
        mommy.make(Ad, folder=self._root_folder)
        mommy.make(Ad, folder=self._root_folder, is_active=False)

        _, response_data = self._get_request(self._get_request_url(self._root_folder.pk))

        self.assertEqual(2, len(response_data['ads']))

from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from rest_framework import status

from .base import RestViewTestBase
from ...models import Folder, Ad


class AdDetailViewTestBase():
    """Common class for AdDetailView test classes."""

    def setUp(self):
        self._root_folder = mommy.make(Folder, parent=None)
        self._ad = mommy.make(Ad, folder=self._root_folder)

    def _get_request_url(self, pk):
        return reverse('ad-detail', args=(pk,))


class AdDetailViewReadTest(AdDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view AdDetailView for operation Read."""

    def test_response_contains_expected_data(self):
        _, response_data = self._get_request(self._get_request_url(self._ad.pk))

        self.assertEqual(self._ad.pk, response_data['pk'])
        self.assertEqual(self._ad.name, response_data['name'])
        self.assertEqual(self._ad.ad_url, response_data['ad_url'])
        self.assertEqual(self._ad.folder.pk, response_data['folder'])

    def test_doesnt_return_inactive_ads(self):
        self._ad.is_active = False
        self._ad.save()

        response, _ = self._get_request(self._get_request_url(self._ad.pk))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class AdDetailViewUpdateTest(AdDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view AdDetailView for operation Update."""

    def test_operation_put_updates_ad(self):
        another_folder = mommy.make(Folder, parent=self._root_folder)
        data = {'name': 'New name', 'ad_url': 'http://www.test.com', 'folder': another_folder.pk}

        self._put_request(self._get_request_url(self._ad.pk), data=data)
        ad_updated = Ad.objects.get(pk=self._ad.pk)

        self.assertEqual(data['name'], ad_updated.name)
        self.assertEqual(data['ad_url'], ad_updated.ad_url)
        self.assertEqual(data['folder'], ad_updated.folder.pk)

    def test_operation_patch_updates_only_provided_data(self):
        data = {'name': 'New name', 'folder': self._root_folder.pk}
        self._patch_request(self._get_request_url(self._ad.pk), data=data)
        ad_updated = Ad.objects.get(pk=self._ad.pk)

        self.assertEqual('New name', ad_updated.name)
        self.assertEqual(self._ad.folder.pk, ad_updated.folder.pk)
        # Checks if other data stays the same, because it wasn't provided
        self.assertEqual(self._ad.ad_url, ad_updated.ad_url)

    def test_cannot_update_inactive_ad(self):
        self._ad.is_active = False
        self._ad.save()

        response, _ = self._patch_request(self._get_request_url(self._ad.pk), data={'name': 'Name'})

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_cannot_set_inactive_folder(self):
        child_folder = mommy.make(Folder, parent=self._root_folder, is_active=False)
        data = {'folder': child_folder.pk}

        response, _ = self._patch_request(self._get_request_url(self._ad.pk), data=data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class AdDetailViewDeleteTest(AdDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view AdDetailView for operation Delete."""

    def test_cannot_delete_ad(self):
        mommy.make(Ad, folder=self._root_folder)
        num_ads = Ad.objects.count()

        self._delete_request(self._get_request_url(self._ad.pk))

        self.assertEqual(num_ads, Ad.objects.count())

    def test_deactivates_ad(self):
        self._delete_request(self._get_request_url(self._ad.pk))
        ad_deactivated = Ad.objects.get(pk=self._ad.pk)

        self.assertFalse(ad_deactivated.is_active)


from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import NON_FIELD_ERRORS

from model_mommy import mommy
from rest_framework import status

from .base import RestViewTestBase
from ... import const
from ...models import Folder, Ad


class FolderDetailViewTestBase():
    """Common class for FolderDetailView test classes."""

    def setUp(self):
        self._root_folder = mommy.make(Folder)
        self._child_folder = mommy.make(Folder, parent=self._root_folder)

    def _get_request_url(self, pk):
        return reverse('folder-detail', args=(pk,))


class FolderDetailViewReadTest(FolderDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view FolderDetailView for operation Read."""

    def test_response_contains_expected_data(self):
        _, response_data = self._get_request(self._get_request_url(self._child_folder.pk))

        self.assertEqual(self._child_folder.pk, response_data['pk'])
        self.assertEqual(self._child_folder.name, response_data['name'])
        self.assertEqual(self._child_folder.parent.pk, response_data['parent'])

    def test_doesnt_return_inactive_folders(self):
        self._child_folder.is_active = False
        self._child_folder.save()

        response, _ = self._get_request(self._get_request_url(self._child_folder.pk))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class FolderDetailViewUpdateTest(FolderDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view FolderDetailView for operation Update."""

    def test_operation_put_updates_folder(self):
        new_child = mommy.make(Folder, parent=self._root_folder)
        data = {'name': 'New Name', 'parent': new_child.pk}

        self._put_request(self._get_request_url(self._child_folder.pk), data)
        new_child_updated = Folder.objects.get(pk=self._child_folder.pk)

        self.assertEqual('New Name', new_child_updated.name)
        self.assertEqual(new_child.pk, new_child_updated.parent.pk)

    def test_operation_patch_updates_only_provided_data(self):
        self._patch_request(
            self._get_request_url(self._child_folder.pk), data={'name': 'New Name'}
        )
        folder_updated = Folder.objects.get(pk=self._child_folder.pk)

        self.assertEqual('New Name', folder_updated.name)
        # Checks if parent stays the same, because it wasn't provided in request
        self.assertEqual(self._child_folder.parent.pk, folder_updated.parent.pk)

    def test_can_update_root_folder(self):
        data_dict = {'name': 'New Name', 'parent': None}

        self._put_request(self._get_request_url(self._root_folder.pk), data=data_dict)
        root_updated = Folder.objects.get(pk=self._root_folder.pk)

        self.assertEqual('New Name', root_updated.name)
        self.assertEqual(None, root_updated.parent)

    def test_cannot_update_non_root_folder_to_root_folder(self):
        response, response_data = self._patch_request(
            self._get_request_url(self._child_folder.pk), data={'parent': None}
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(const.MSG_ONLY_ONE_ROOT_FOLDER, response_data[NON_FIELD_ERRORS][0])

    def test_cannot_update_folder_parent_to_self(self):
        response, response_data = self._patch_request(
            self._get_request_url(self._child_folder.pk), data={'parent': self._child_folder.pk}
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(const.MSG_FOLDER_CANT_BE_PARENT_TO_ITSELF, response_data['parent'][0])

    def test_cannot_set_folder_parent_to_inactive_folder(self):
        inactive_folder = mommy.make(Folder, parent=self._child_folder, is_active=False)

        response, _ = self._patch_request(
            self._get_request_url(self._child_folder.pk), data={'parent': inactive_folder.pk}
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_cannot_update_inactive_folder(self):
        self._child_folder.is_active = False
        self._child_folder.save()

        response, _ = self._patch_request(
            self._get_request_url(self._child_folder.pk), data={'name': 'New Name'}
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class FolderDetailViewDeleteTest(FolderDetailViewTestBase, RestViewTestBase, TestCase):
    """Tests for view FolderDetailView for operation Delete."""

    def test_cannot_delete_folder(self):
        num_folders = Folder.objects.count()
        self._delete_request(self._get_request_url(self._child_folder.pk))

        self.assertEqual(num_folders, Folder.objects.count())

    def test_deactivates_folder(self):
        self._delete_request(self._get_request_url(self._child_folder.pk))
        folder_deactivated = Folder.objects.get(pk=self._child_folder.pk)

        self.assertFalse(folder_deactivated.is_active)

    def test_cannot_deactivate_root_folder(self):
        response, response_data = self._delete_request(self._get_request_url(self._root_folder.pk))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(const.MSG_ROOT_FOLDER_CANT_DELETE, response_data[NON_FIELD_ERRORS][0])

    def test_deactivates_ads_in_current_folder(self):
        ad = mommy.make(Ad, folder=self._child_folder)
        self._delete_request(self._get_request_url(self._child_folder.pk))
        ad_deactivated = Ad.objects.get(pk=ad.pk)

        self.assertFalse(ad_deactivated.is_active)

    def test_recursively_deactivates_sub_folders(self):
        sub_folder = mommy.make(Folder, parent=self._child_folder)
        sub_sub_folder = mommy.make(Folder, parent=sub_folder)

        self._delete_request(self._get_request_url(self._child_folder.pk))
        sub_folder_deactivated = Folder.objects.get(pk=sub_folder.pk)
        sub_sub_folder_deactivated = Folder.objects.get(pk=sub_sub_folder.pk)

        self.assertFalse(sub_folder_deactivated.is_active)
        self.assertFalse(sub_sub_folder_deactivated.is_active)

    def test_recursively_deactivates_ads_in_sub_folders(self):
        sub_folder = mommy.make(Folder, parent=self._child_folder)
        sub_sub_folder = mommy.make(Folder, parent=sub_folder)
        ad_1, ad_2 = mommy.make(Ad, folder=sub_folder), mommy.make(Ad, folder=sub_sub_folder)

        self._delete_request(self._get_request_url(self._child_folder.pk))
        ad_deactivated_1, ad_deactivated_2 = Ad.objects.get(pk=ad_1.pk), Ad.objects.get(pk=ad_2.pk)

        self.assertFalse(ad_deactivated_1.is_active)
        self.assertFalse(ad_deactivated_2.is_active)

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.exceptions import NON_FIELD_ERRORS

from model_mommy import mommy
from rest_framework import status

from .base import RestViewTestBase
from ...import const
from ...models import Folder


class FolderListViewTestBase():
    """Common class for FolderListView test classes."""

    def setUp(self):
        self._request_url = reverse('folder-list')


class FolderListViewReadTest(FolderListViewTestBase, RestViewTestBase, TestCase):
    """Tests for view FolderListView for operation Read."""

    def test_response_contains_expected_data(self):
        root_folder = mommy.make(Folder)
        _, response_data = self._get_request(self._request_url)

        self.assertEqual(root_folder.pk, response_data[0]['pk'])
        self.assertEqual(root_folder.name, response_data[0]['name'])
        self.assertEqual(root_folder.parent, response_data[0]['parent'])

    def test_returns_only_active_folders(self):
        root_folder = mommy.make(Folder, name='Root', is_active=True)
        mommy.make(Folder, is_active=True, parent=root_folder)
        mommy.make(Folder, is_active=False, parent=root_folder)

        _, response_data = self._get_request(self._request_url)

        self.assertEqual(2, len(response_data))


class FolderListViewCreateTest(FolderListViewTestBase, RestViewTestBase, TestCase):
    """Tests for view FolderListView for operation Create."""

    def test_correctly_creates_new_folder(self):
        root_folder = mommy.make(Folder)
        post_data = self._folder_data_dict({'parent': root_folder.pk})

        self._post_request(self._request_url, data=post_data)
        new_folder = Folder.objects.latest('time_created')

        self.assertEqual(post_data['name'], new_folder.name)
        self.assertEqual(post_data['parent'], new_folder.parent.pk)

    def test_creates_active_folder(self):
        self._post_request(self._request_url, data=self._folder_data_dict())
        new_folder = Folder.objects.latest('time_created')

        self.assertTrue(new_folder.is_active)

    def test_can_create_root_folder(self):
        self._post_request(self._request_url, data=self._folder_data_dict())

        self.assertEqual(1, Folder.objects.count())

    def test_can_create_root_folder_if_other_root_folders_are_inactive(self):
        mommy.make(Folder, parent=None, is_active=False)
        self._post_request(self._request_url, data=self._folder_data_dict())

        self.assertEqual(2, Folder.objects.count())

    def test_cannot_create_root_folder_if_active_root_folder_already_exists(self):
        mommy.make(Folder, parent=None)
        response, response_data = self._post_request(
            self._request_url, data=self._folder_data_dict()
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(const.MSG_ONLY_ONE_ROOT_FOLDER, response_data[NON_FIELD_ERRORS][0])
        self.assertEqual(1, Folder.objects.count())

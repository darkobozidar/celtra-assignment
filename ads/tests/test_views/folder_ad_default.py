from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy
from rest_framework import status

from ...models import Folder
from ... import const


class FolderAdDefaultTest(TestCase):
    """Tests for folder_ad_default."""

    def _get_request_url(self, pk=None):
        return reverse('folder-ad-detail', args=(pk,)) if pk else reverse('folder-ad-detail')

    def test_redirects_to_root_folder(self):
        root_folder = mommy.make(Folder, parent=None)

        response = self.client.get(self._get_request_url())
        expected_url = self._get_request_url(root_folder.pk)

        self.assertRedirects(response, expected_url, status_code=status.HTTP_302_FOUND)

    def test_returns_message_root_folder_doesnt_exist_if_no_root_folder_is_in_database(self):
        response = self.client.get(self._get_request_url())

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(const.MSG_ROOT_FOLDER_DOESNT_EXIST, str(response.content)[2:-1])

    def test_returns_message_root_folder_doesnt_exist_if_all_root_folders_are_inactive(self):
        mommy.make(Folder, parent=None, is_active=False)
        response = self.client.get(self._get_request_url())

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(const.MSG_ROOT_FOLDER_DOESNT_EXIST, str(response.content)[2:-1])

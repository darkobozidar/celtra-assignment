from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from ...models import Folder


class FolderModelTest(TestCase):
    def test_default_value_for_field_is_active(self):
        folder = mommy.make(Folder)
        self.assertTrue(folder.is_active)

    def test_field_name_is_mandatory(self):
        with self.assertRaises(ValidationError):
            mommy.make(Folder, name='')

    def test_field_parent_is_not_mandatory_if_no_other_folder_exist(self):
        # Shouldn't raise any errors. Needed for insertion of initial root folder.
        mommy.make(Folder, parent=None)

    def test_cannot_insert_two_active_root_folders(self):
        mommy.make(Folder)
        # Subsequently tests that field parent is mandatory for non-root folders.
        with self.assertRaises(ValidationError):
            mommy.make(Folder)

    def test_can_insert_root_folder_if_other_root_folders_are_inactive(self):
        mommy.make(Folder, is_active=False)
        # Shouldn't raise any errors
        mommy.make(Folder)

    def test_can_insert_inactive_root_folder_if_active_root_folder_already_exists(self):
        mommy.make(Folder)
        # Shouldn't raise any errors
        mommy.make(Folder, is_active=False)

    def test_cannot_update_child_folder_to_root_folder(self):
        root_folder = mommy.make(Folder)
        child_folder = mommy.make(Folder, parent=root_folder)

        with self.assertRaises(ValidationError):
            child_folder.parent = None
            child_folder.save()

    def test_cannot_deactivate_root_folder(self):
        root_folder = mommy.make(Folder)

        with self.assertRaises(ValidationError):
            root_folder.is_active = False
            root_folder.save()

    def test_cannot_delete_folder(self):
        root_folder = mommy.make(Folder)
        child_folder = mommy.make(Folder, parent=root_folder)

        with self.assertRaises(Exception):
            child_folder.delete()

    def test_property_is_root_returns_true_if_folder_is_root(self):
        folder_root = mommy.make(Folder, parent=None)
        folder_child = mommy.make(Folder, parent=folder_root)

        self.assertTrue(folder_root.is_root)
        self.assertFalse(folder_child.is_root)

    def test_property_is_active_root_returns_true_if_folder_is_active_root(self):
        folder_root_active = mommy.make(Folder, parent=None)
        folder_root_inactive = mommy.make(Folder, parent=None, is_active=False)
        folder_child = mommy.make(Folder, parent=folder_root_active)

        self.assertTrue(folder_root_active.is_active_root)
        self.assertFalse(folder_root_inactive.is_active_root)
        self.assertFalse(folder_child.is_active_root)

    def test_manager_method_active_returns_only_active_records(self):
        root_folder = mommy.make(Folder, parent=None, is_active=True)
        mommy.make(Folder, parent=root_folder, is_active=True)
        mommy.make(Folder, parent=root_folder, is_active=False)

        self.assertEqual(2, Folder.objects.active().count())

    def test_manager_method_inactive_returns_only_inactive_records(self):
        root_folder = mommy.make(Folder, is_active=False)
        mommy.make(Folder, parent=root_folder, is_active=False)
        mommy.make(Folder, parent=root_folder, is_active=True)

        self.assertEqual(2, Folder.objects.inactive().count())

    def test_ordering(self):
        root_folder = folder_3 = mommy.make(Folder, name='Test 3')
        folder_1 = mommy.make(Folder, name='Test 1', parent=root_folder)
        folder_2 = mommy.make(Folder, name='Test 2', parent=root_folder)

        self.assertEqual([folder_1, folder_2, folder_3], list(Folder.objects.all()))

    def test_string_representation(self):
        folder = mommy.make(Folder, name='Test name')
        self.assertEqual('Test name', str(folder))

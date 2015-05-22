from django.db import transaction
from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from ...models import Ad, Folder


class AdModelTest(TestCase):
    def test_default_value_for_field_is_active(self):
        ad = mommy.make(Ad)
        self.assertTrue(ad.is_active)

    def test_field_name_is_mandatory(self):
        with self.assertRaises(ValidationError):
            mommy.make(Ad, name='')

    def test_field_url_is_mandatory(self):
        with self.assertRaises(ValidationError):
            mommy.make(Ad, ad_url='')

    def test_field_folder_is_mandatory(self):
        with self.assertRaises(ValueError):
            mommy.make(Ad, folder=None)

    def test_filed_url_accepts_only_valid_url(self):
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                mommy.make(Ad, ad_url='invalid_url')

        # Shouldn't raise error
        mommy.make(Ad, ad_url='http://www.valid.com')

    def test_cannot_delete_ad(self):
        ad = mommy.make(Ad)
        with self.assertRaises(Exception):
            ad.delete()

    def test_folder_has_to_be_active(self):
        root_folder = mommy.make(Folder)
        child_folder = mommy.make(Folder, parent=root_folder, is_active=False)

        with self.assertRaises(ValidationError):
            mommy.make(Ad, folder=child_folder)

    def test_manager_method_active_returns_only_active_records(self):
        root_folder = mommy.make(Folder)
        mommy.make(Ad, is_active=True, folder=root_folder)
        mommy.make(Ad, is_active=True, folder=root_folder)
        mommy.make(Ad, is_active=False, folder=root_folder)

        self.assertEqual(2, Ad.objects.active().count())

    def test_manager_method_inactive_returns_only_inactive_records(self):
        root_folder = mommy.make(Folder)
        mommy.make(Ad, is_active=False, folder=root_folder)
        mommy.make(Ad, is_active=False, folder=root_folder)
        mommy.make(Ad, is_active=True, folder=root_folder)

        self.assertEqual(2, Ad.objects.inactive().count())

    def test_ordering(self):
        root_folder = mommy.make(Folder)
        ad_3 = mommy.make(Ad, name='Test 3', folder=root_folder)
        ad_1 = mommy.make(Ad, name='Test 1', folder=root_folder)
        ad_2 = mommy.make(Ad, name='Test 2', folder=root_folder)

        self.assertEqual([ad_1, ad_2, ad_3], list(Ad.objects.all()))

    def test_string_representation(self):
        ad = mommy.make(Ad, name='Test name')
        self.assertEqual('Test name', str(ad))

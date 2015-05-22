from django.test import TestCase
from django.core.urlresolvers import reverse


class AdCreatorTemplateViewTest(TestCase):
    """Tests for view AdCreatorTemplateView."""

    def setUp(self):
        self._request_url = reverse('ad-creator')

    def test_uses_correct_template(self):
        response = self.client.get(self._request_url)
        self.assertTemplateUsed(response, 'ads/ad_creator.html')

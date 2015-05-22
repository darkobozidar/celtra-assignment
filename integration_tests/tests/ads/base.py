from django.core.urlresolvers import reverse

from selenium import webdriver
from model_mommy import mommy

from ads.models import Ad, Folder


class IntegrationBaseTest():
    """Base class for integration tests for django app "ads"."""

    def setUp(self):
        # Instantiates browser
        self._browser = webdriver.Firefox()
        self._browser.implicitly_wait(3)

        # Root folder
        self._root_folder = mommy.make(Folder, name="Root")
        # Sub-folders
        self._sub_folder_1 = mommy.make(Folder, name="SubFolder 1", parent=self._root_folder)
        self._sub_folder_2 = mommy.make(Folder, name="SubFolder 2", parent=self._root_folder)
        mommy.make(Folder, parent=self._root_folder, is_active=False)
        # Sub-sub-folders
        self._sub_sub_folder = mommy.make(Folder, name="SubSubFolder", parent=self._sub_folder_1)
        mommy.make(Folder, parent=self._root_folder, is_active=False)

        # Root folder ads
        self._ad_root_folder_1 = mommy.make(
            Ad, folder=self._root_folder, name="Ad Root 1", ad_url="https://www.google.si/"
        )
        self._ad_root_folder_2 = mommy.make(
            Ad, folder=self._root_folder, name="Ad Root 2", ad_url="http://www.celtra.com/"
        )
        mommy.make(Ad, folder=self._root_folder, is_active=False)
        # Sub-folder 1 ads
        self._ad_sub_folder_1 = mommy.make(
            Ad, folder=self._sub_folder_1, name="Ad subFolder 1", ad_url="https://www.yahoo.com/"
        )
        mommy.make(Ad, folder=self._sub_folder_1, is_active=False)

    def tearDown(self):
        # Removes error of closing browser to early
        self._browser.refresh()
        self._browser.quit()

    def _get_request_url(self, pk=''):
        """Generates url for home page."""

        return '%s%s%s' % (self.live_server_url, reverse('ad-creator'), "#/%s" % pk if pk else '')

    def _get_current_folder_name(self):
        """Returns the name of the currently selected folder."""

        return self._browser.find_element_by_id('current-folder-name').text

    def _get_sub_folders(self):
        """Returns list of sub-folder buttons of currently selected folder."""

        folder_choices = self._browser.find_element_by_class_name('folder-choices')
        return folder_choices.find_elements_by_tag_name('button')

    def _get_sub_folder_names(self):
        """Returns a list of sub-folder names of currently selected folder."""

        return [f.text for f in self._get_sub_folders()]

    def _click_sub_folder(self, index):
        """Performs a click action on current folder."""

        self._get_sub_folders()[index].click()

    def _get_current_ads(self):
        """Returns a list of ads for currently selected folder."""

        ads = self._browser.find_element_by_class_name('ad-choices')
        return ads.find_elements_by_tag_name('a')

    def _get_current_ad_names(self):
        """Returns a list of ad names for currently selected folder."""

        return [a.text for a in self._get_current_ads()]

    def _click_ad(self, index):
        """Performs a click on ad."""

        self._get_current_ads()[index].click()

    def _get_empty_folder_message(self):
        """Return a message, which appears if current folder is empty."""

        return self._browser.find_element_by_id('empty-folder-msg').text

    def _get_error_message(self):
        """Returns a error message (typically for 404 or 500)."""

        return self._browser.find_element_by_class_name('error').text

    def _get_button_back(self):
        """Returns a "back" button, which mover user to parent folder."""

        return self._browser.find_element_by_class_name('btn-back')

    def _click_button_back(self):
        """Clicks on button "back", which causes a move to parent folder."""

        return self._get_button_back().click()

    def _switch_tab(self, index):
        """
        Performs a tab switch. The newer the tab is, the greater it's index is. Index first tab is
        zero.
        """

        self._browser.switch_to.window(self._browser.window_handles[index])

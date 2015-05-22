import time

from django.test import LiveServerTestCase

from .base import IntegrationBaseTest


class OperationReadTest(IntegrationBaseTest, LiveServerTestCase):
    """Integration tests for operation read."""

    def test_folder_tree(self):
        """Tests walk across folder tree."""

        # User opens browser on default page.
        self._browser.get(self._get_request_url())
        time.sleep(1)

        # There he sees root folder name.
        self.assertEqual(self._root_folder.name, self._get_current_folder_name())

        # He also notices two sub-folders. Also none of inactive folders are displayed.
        sub_folders = self._get_sub_folder_names()
        self.assertEqual(2, len(sub_folders))
        self.assertIn(self._sub_folder_1.name, sub_folders)
        self.assertIn(self._sub_folder_2.name, sub_folders)

        # He looks for button "back", but it is hidden, because he is in a root folder.
        self.assertEqual('', self._get_button_back().text)

        # He decides to click on first sub-folder.
        self._click_sub_folder(0)
        time.sleep(1)

        # He first notices that the name of the current folder changed.
        self.assertEqual(self._sub_folder_1.name, self._get_current_folder_name())

        # He also sees one sub-sub-folder. Also none of inactive folders are displayed.
        sub_sub_folders = self._get_sub_folder_names()
        self.assertEqual(1, len(sub_sub_folders))
        self.assertIn(self._sub_sub_folder.name, sub_sub_folders)

        # He sees that button "back" appeared.
        self.assertEqual('<', self._get_button_back().text)

        # He decides to click on sub-sub-folder again.
        self._click_sub_folder(0)
        time.sleep(1)

        # Again he sees that the name of the current folder changed
        self.assertEqual(self._sub_sub_folder.name, self._get_current_folder_name())

        # A message informs him, that the folder is empty and he cannot see any folders.
        self.assertEqual('This folder is empty.', self._get_empty_folder_message())
        self.assertEqual([], self._get_sub_folders())

        # He sees that the button "back" is still there and he clicks it.
        self._click_button_back()
        time.sleep(1)

        # He is back to sub-folder 1.
        self.assertEqual(self._sub_folder_1.name, self._get_current_folder_name())

        # All the children of sub-folder 1 are still there.
        sub_sub_folders = self._get_sub_folder_names()
        self.assertEqual(1, len(sub_sub_folders))
        self.assertIn(self._sub_folder_1.name, sub_folders)

        # He clicks button "back" again to come back to root folder.
        self._click_button_back()
        time.sleep(1)

        # He sees that the name of the current folder changed to root folder.
        self.assertEqual(self._root_folder.name, self._get_current_folder_name())

        # All the sub folders of root folder are still there.
        sub_folders = self._get_sub_folder_names()
        self.assertEqual(2, len(sub_folders))
        self.assertIn(self._sub_folder_1.name, sub_folders)
        self.assertIn(self._sub_folder_2.name, sub_folders)

        # Finally he sees that the button "back" disappeared and that everything is working OK.
        self.assertEqual('', self._get_button_back().text)

    def test_ads_in_folder_tree(self):
        """Tests displaying and clicking ads in folder tree."""

        # User opens browser on default page.
        self._browser.get(self._get_request_url())
        time.sleep(1)

        # He sees two ads in root folder. Also none of inactive ads are displayed.
        ads = self._get_current_ad_names()
        self.assertEqual(2, len(ads))
        self.assertIn(self._ad_root_folder_1.name, ads)
        self.assertIn(self._ad_root_folder_2.name, ads)

        # He decides to click on first ad.
        self._click_ad(0)

        # He sees that new tab opened with ad url.
        self._switch_tab(1)
        self.assertEqual(self._ad_root_folder_1.ad_url, self._browser.current_url)

        # He closes the tab and returns back to primary tab.
        self._browser.close()
        self._switch_tab(0)

        # He decides to go to first sub-folder.
        self._click_sub_folder(0)
        time.sleep(1)

        # There he sees one ad. Also none of inactive ads are displayed.
        ads = self._get_current_ad_names()
        self.assertEqual(1, len(ads))
        self.assertIn(self._ad_sub_folder_1.name, ads)

        # He decides to click on it.
        self._click_ad(0)

        # He sees that new tab opened with ad url.
        self._switch_tab(1)
        self.assertEqual(self._ad_sub_folder_1.ad_url, self._browser.current_url)

        # He closes the tab and returns back to primary tab.
        self._browser.close()
        self._switch_tab(0)

        # He decides to go back to root folder.
        self._click_button_back()
        time.sleep(1)

        # Both ads are still there.
        ads = self._get_current_ad_names()
        self.assertEqual(2, len(ads))
        self.assertIn(self._ad_root_folder_1.name, ads)
        self.assertIn(self._ad_root_folder_2.name, ads)

        # This time he clicks on second ad.
        self._click_ad(1)

        # He sees that new tab opened with ad url.
        self._switch_tab(1)
        self.assertEqual(self._ad_root_folder_2.ad_url, self._browser.current_url)

        # He closes the tab and returns back to primary tab.
        self._browser.close()
        self._switch_tab(0)

    def test_browser_url_for_folder_tree(self):
        """Tests browser url during walk across folder tree."""

        # User opens browser on default page.
        self._browser.get(self._get_request_url())
        time.sleep(1)

        # He notices that the url path changed to root folder pk.
        self.assertEqual(self._get_request_url(self._root_folder.pk), self._browser.current_url)

        # He goes into first sub folder.
        self._click_sub_folder(0)
        time.sleep(1)

        # He sees that url updated again to sub-folder pk.
        self.assertEqual(self._get_request_url(self._sub_folder_1.pk), self._browser.current_url)

        # He goes again into first sub folder.
        self._click_sub_folder(0)
        time.sleep(1)

        # He notes that url updated again to sub-sub-folder pk.
        self.assertEqual(self._get_request_url(self._sub_sub_folder.pk), self._browser.current_url)

        # He decides to go back to sub-folder 1.
        self._click_button_back()
        time.sleep(1)

        # He sees that url updates again to sub-folder pk.
        self.assertEqual(self._get_request_url(self._sub_folder_1.pk), self._browser.current_url)

        # He decides to go back to root folder.
        self._click_button_back()
        time.sleep(1)

        # He sees that url updates again to root folder pk.
        self.assertEqual(self._get_request_url(self._root_folder.pk), self._browser.current_url)

        # He decides to get sneaky and types url of sub-sub-folder.
        self._get_request_url(self._sub_sub_folder.pk)
        self._browser.get(self._get_request_url(self._sub_sub_folder.pk))
        self._browser.refresh()
        time.sleep(1)

        # He sees that current folder name updates.
        self.assertEqual(self._sub_sub_folder.name, self._get_current_folder_name())

        # He wants to make sure that button "back" will bring him back to sub-folder 1.
        self._click_button_back()
        time.sleep(1)

        # He sees that url updates to sub-folder 1.
        self.assertEqual(self._get_request_url(self._sub_folder_1.pk), self._browser.current_url)

    def test_error_message_404(self):
        """Tests if user enters id of non-existing folder."""

        # User opens browser on default page. He enters an id of non-existing folder.
        self._browser.get(self._get_request_url(1000))
        time.sleep(1)

        # He sees an error message.
        self.assertIn("Not found.", self._get_error_message())

        # He also doesn't see any folders
        self.assertEqual(0, len(self._get_sub_folders()))

        # Also no of the ads are displayed
        self.assertEqual(0, len(self._get_current_ads()))

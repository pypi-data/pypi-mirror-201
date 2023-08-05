"""Module: browser_manipulation
This module contains functions and classes related to manipulation of browser. such as get html source code,
fill_input_on_webpage, write_in_input_box, click_on_button.
To do: change the exceptions to selenium exceptions by importing the selenium exceptions from selenium.common.exceptions
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from browser_automation import browser_setup
from browser_automation import os_json_utils
from browser_automation import locate_elements


class Interactions(browser_setup.Setup):
    """
    This is class for doing manipulations with web elements using selenium drivers.
    """
    def __init__(self, custom_browser_options_json_path=None):
        """
        Inherit from browser_setup.Setup and get the driver object for manipulation.
        """
        super().__init__(custom_browser_options_json_path)

    def driver_wait(self, time_duration: float):
        """This makes the driver idle for time_duration.

        Parameters
        ----------
        time_duration : float
            This is the time for which we want out driver to stay idle to minimize load on web server.

        Returns
        -------
        function
            Returns wait time of time_duration

        """
        return WebDriverWait(self.driver, time_duration)

    def change_window(self):
        """
        It changes the current window to last window in browser

        Returns
        -------
        None

        """
        # Store the ID of the original window
        original_window = self.driver.current_window_handle
        # ID of all windows
        all_windows = self.driver.window_handles
        needed_window = all_windows[-1]
        # move to the last window
        if needed_window != original_window:
            self.driver.switch_to.window(needed_window)

    def scroll_page(self, scroll_until: int = 4000, scroll_height: int = 200):
        """
        this scroll the page to load all of details

        Parameters
        ----------
        scroll_until : int
            This is the total amount of scrolling.
        scroll_height : int
            This is how much scroll is happen in one go.

        Returns
        -------
        None

        """
        scroll = 0
        while scroll < scroll_until:
            self.driver.execute_script("window.scrollTo(0," + str(scroll) + " );")
            scroll += scroll_height

    def get_current_webpage(self):
        """
        html_source_code: complete html of page

        Returns
        -------
        str
            It is html source code of current webpage.

        """
        html_source_code = self.driver.page_source
        return html_source_code

    def fill_input_on_webpage(self, word_seen_in_website: str, element_name: str, input_answer: str):
        """
        this function fill the input box on webpage with the help of wordSeenInWebsite, with the inputAnswer.

        Parameters
        ----------
        word_seen_in_website : str
            word that you see in input box on website
        element_name : str
            ID, Name, Class etc. of html element
        input_answer : str
            answer that you want to put in the input box of webpage

        Returns
        -------
        None

        """
        element_value = locate_elements.LocateElements(self.get_current_webpage()).get_element_value_from_html(
            word_seen_in_website, element_name)
        for value in element_value:
            try:
                print(value)
                print(type(value))
                input_box = self.driver.find_element(By.ID, str(value))
                input_box.clear()
                input_box.send_keys(input_answer)
                print("executed")
            except Exception:
                print('passing')
                pass

    def input_box_by_name(self, name: str, answer: str):
        """
        Input answer in input box by searching element Name

        Parameters
        ----------
        name : str
            This is element locator Name, visit - https://selenium-python.readthedocs.io/
        answer : str
            This is the input string you want to put in input box on webpage.

        Returns
        -------
        None

        """
        try:
            user_field = self.driver.find_element(By.NAME, name)
            user_field.clear()
            user_field.send_keys(answer)
        except Exception:
            print(Exception)

    def input_box_by_xpath(self, xpath_element: str, answer: str):
        """
        Input answer in input box by searching element Name

        Parameters
        ----------
        xpath_element : str
            This is the address in xpath format, visit - https://selenium-python.readthedocs.io/
        answer : str
            This is the input string you want to put in input box on webpage.

        Returns
        -------
        None

        """
        try:
            input_box = self.driver.find_element(By.XPATH, xpath_element)
            input_box.clear()
            input_box.send_keys(answer)
        except Exception:
            print(Exception)

    def write_in_input_box(self, element_locator_type: str, element_locator_path: str, input_answer: str):
        """
        Input answer in input box by searching element_locator_path

        Parameters
        ----------
        element_locator_type : str
            these by selenium methods to locate web element. This function contains
            CLASS_NAME, CSS_SELECTOR, ID, LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME, XPATH.
        element_locator_path : str
            path of above given element_locator_type
        input_answer : str
            This is the input string you want to put in input box on webpage.

        Returns
        -------
        None

        """
        try:
            if element_locator_type.upper() == "CLASS_NAME":
                input_box = self.driver.find_element(By.CLASS_NAME, element_locator_path)
            elif element_locator_type.upper() == "CSS_SELECTOR":
                input_box = self.driver.find_element(By.CSS_SELECTOR, element_locator_path)
            elif element_locator_type.upper() == "ID":
                input_box = self.driver.find_element(By.ID, element_locator_path)
            elif element_locator_type.upper() == "LINK_TEXT":
                input_box = self.driver.find_element(By.LINK_TEXT, element_locator_path)
            elif element_locator_type.upper() == "NAME":
                input_box = self.driver.find_element(By.NAME, element_locator_path)
            elif element_locator_type.upper() == "PARTIAL_LINK_TEXT":
                input_box = self.driver.find_element(By.PARTIAL_LINK_TEXT, element_locator_path)
            elif element_locator_type.upper() == "TAG_NAME":
                input_box = self.driver.find_element(By.TAG_NAME, element_locator_path)
            elif element_locator_type.upper() == "XPATH":
                input_box = self.driver.find_element(By.XPATH, element_locator_path)
            else:
                print(
                    "This function doesn't implement your element_locator_type, please try modifying this function or "
                    "write separately!")
                return
            input_box.clear()
            input_box.send_keys(input_answer)
        except Exception:
            print("element locator path can not be found")

    def click_on_button(self, element_locator_type: str, element_locator_path: str):
        """
        click on button on web by searching element_locator_path. exceptions silenced

        Parameters
        ----------
        element_locator_type : str
            these by selenium methods to locate web element. This function contains CLASS_NAME, CSS_SELECTOR, ID,
            LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME, XPATH.
        element_locator_path : str
            path of above given element_locator_type

        Returns
        -------
        None

        """
        try:
            if element_locator_type.upper() == "CLASS_NAME":
                button = self.driver.find_element(By.CLASS_NAME, element_locator_path)
            elif element_locator_type.upper() == "CSS_SELECTOR":
                button = self.driver.find_element(By.CSS_SELECTOR, element_locator_path)
            elif element_locator_type.upper() == "ID":
                button = self.driver.find_element(By.ID, element_locator_path)
            elif element_locator_type.upper() == "LINK_TEXT":
                button = self.driver.find_element(By.LINK_TEXT, element_locator_path)
            elif element_locator_type.upper() == "NAME":
                button = self.driver.find_element(By.NAME, element_locator_path)
            elif element_locator_type.upper() == "PARTIAL_LINK_TEXT":
                button = self.driver.find_element(By.PARTIAL_LINK_TEXT, element_locator_path)
            elif element_locator_type.upper() == "TAG_NAME":
                button = self.driver.find_element(By.TAG_NAME, element_locator_path)
            elif element_locator_type.upper() == "XPATH":
                button = self.driver.find_element(By.XPATH, element_locator_path)
            else:
                print(
                    "This function doesn't implement your element_locator_type, please try modifying this function or "
                    "write separately!")
                return
            button.click()
        except Exception:
            print("element locator path can not be found")

    def website_login(self, url: str,
                      username_element_locator_type: str, username_element_locator_path: str, username: str,
                      password_element_locator_type: str, password_element_locator_path: str, password: str,
                      login_button_element_locator_type: str, login_button_element_locator_path: str,
                      login_option_element_locator_type=None, login_option_element_locator_path: str = None):
        """
        login into website using these arguments Args: driver: url: username_element_name: username: this
        is the username of person already sign up on website password: password for above username of account

        Parameters
        ----------
        url : str
            This is link for website.
        username_element_locator_type : str
            This is locator type for username_element for username.
        username_element_locator_path : str
            This is the address of locator type.
        username : str
            This is the input username for given website.
        password_element_locator_type : str
            This is locator type for password_element.
        password_element_locator_path : str
            This is address of locator type for password.
        password : str
            This is the input password for given website.
        login_button_element_locator_type : str
            This is locator type for login button_element.
        login_button_element_locator_path: str
            This is the address of locator type for login_button.
        login_option_element_locator_type : str
            This is locator type for login_option button_element.
        login_option_element_locator_path: str
            This is the address of locator type for login_option.

        Returns
        -------
        None

        """
        print(f"Going to website: {url}")
        self.driver.get(url)
        os_json_utils.RandomSleep().sleep_for_random_time()
        if login_option_element_locator_path is not None:
            self.click_on_button(login_option_element_locator_type, login_option_element_locator_path)
        self.write_in_input_box(username_element_locator_type, username_element_locator_path, username)
        os_json_utils.RandomSleep().sleep_for_random_time()
        self.write_in_input_box(password_element_locator_type, password_element_locator_path, password)
        self.click_on_button(login_button_element_locator_type, login_button_element_locator_path)
        os_json_utils.RandomSleep().sleep_for_random_time()

    def button_click_by_xpath(self, button_element_xpath: str):
        """
        ButtonElementXpath used to find and click on the button

        Parameters
        ----------
        button_element_xpath : str
            This is the address of locator type 'XPATH' for button element.

        Returns
        -------
        None

        """
        try:
            button = self.driver.find_element(By.XPATH, button_element_xpath)
            button.click()
        except Exception:
            print(Exception)

    def articles_gathering_loop(self, articles_name_list: list, initial_search_link: str,
                                pdf_button_locator_element_xpath: str,
                                destination_folder_path: str, scroll: bool = False, open_button: bool = False):
        """This is a sample loop for gathering the data(research articles).

        Parameters
        ----------
        articles_name_list : list
            This list contains the name of search argument in website search box.
        initial_search_link : str
            This is the link where we have to get data.
        pdf_button_locator_element_xpath : str
            This is the xpath address of the element of data download button.
        destination_folder_path : str
            This is the path of the folder where we want to move our downloaded data.
        scroll : bool
            This is the option to switch on scroll on the page.
        open_button : bool
            This is the additional dialogue box after clicking on download button.

        Returns
        -------
        None

        """
        for article_name in articles_name_list:
            self.create_article_weblink_and_browse(initial_search_link, article_name)
            os_json_utils.RandomSleep().sleep_for_random_time()
            if scroll:
                self.scroll_page(400, 300)
            self.click_on_button("xpath", pdf_button_locator_element_xpath)
            os_json_utils.RandomSleep().sleep_for_random_time()
            if open_button:
                open_pdf_button_link = locate_elements.LocateElements(self.get_current_webpage()).get_link_via_regex()
                self.driver.get(open_pdf_button_link)
            print("file downloaded")
            os_json_utils.DownloadUtil(self.download_dir).file_rename_and_moving(destination_folder_path, article_name)

    def create_article_weblink_and_browse(self, initial_search_link: str, search_argument: str):
        """Some website can directly take search argument after their link. so this function put the search argument
        after initial_search_link.

        Parameters
        ----------
        initial_search_link : str
            This is the web link that can be used to append search argument and return required data page.
        search_argument : str
            This can be any search string such as article name in research database.

        Returns
        -------
        None

        """
        full_search_site_link = initial_search_link + search_argument
        print(f"trying to download article: {search_argument}")
        self.driver.get(full_search_site_link)

    def web_element_multiple_try_to_click_or_write(self, list_of_element_locator_types_with_addresses: list,
                                                   write_something=None):
        """
        This function takes list of element_locator types with addresses to click or write in input_box.
        Note - This is worst case of finding different addresses for same web element on website

        Parameters
        ----------
        list_of_element_locator_types_with_addresses : str
            This is the list with element_locator_types such as CLASS_NAME,CSS_SELECTOR, ID, LINK_TEXT, NAME,
            PARTIAL_LINK_TEXT, TAG_NAME, XPATH with respective addresses. example- ["id", "result-header-1", "xpath",
            "//h3[@id='result-header-1']"]
        write_something : str
            default is None which signify that click() function will be executed. if you want to write something in
            found web element, please replace None to your input string.

        Returns
        -------
        None

        """
        assert (type(write_something) == str)
        web_element = self.multiple_try_to_find_web_element(list_of_element_locator_types_with_addresses)
        if web_element is None:
            print("web_element is not found: please revisit your strategy or create a new function")
            return
        if write_something is None:
            web_element.click()
        else:
            web_element.clear()
            web_element.send_keys(write_something)

    def multiple_try_to_find_web_element(self, list_of_element_locator_types_with_addresses: list) -> object:
        """
        This functions uses multiple try statements to find_web_element

        Parameters
        ----------
        list_of_element_locator_types_with_addresses : str
            This is the list with element_locator_types such as CLASS_NAME,CSS_SELECTOR, ID, LINK_TEXT, NAME,
            PARTIAL_LINK_TEXT, TAG_NAME, XPATH with respective addresses. example- ["id", "result-header-1", "xpath",
            "//h3[@id='result-header-1']"]

        Returns
        -------
        object
            The web_element object from selenium driver. selenium.webdriver.remote.webelement.WebElement

        """
        length_of_list_of_element_locator_types_with_addresses = len(list_of_element_locator_types_with_addresses)
        assert (length_of_list_of_element_locator_types_with_addresses >= 2) and (
                length_of_list_of_element_locator_types_with_addresses % 2 == 0)
        web_element_found = False
        element_locator_types_index = 0
        while not web_element_found:
            element_locator_path_index = element_locator_types_index + 1
            print(element_locator_types_index, element_locator_path_index)
            result = self.try_element_address(list_of_element_locator_types_with_addresses[element_locator_types_index],
                                              list_of_element_locator_types_with_addresses[element_locator_path_index])
            web_element_found, web_element = result[0], result[1]
            element_locator_types_index += 2
            if element_locator_types_index > length_of_list_of_element_locator_types_with_addresses - 1:
                print("this stops")
                return web_element

    def try_element_address(self, element_locator_type: str, element_locator_path: str):
        """
        This is try except block for searching element via element_locator_type, element_locator_path

        Parameters
        ----------
        element_locator_type : str
            These by selenium methods to locate web element. This function contains
                CLASS_NAME, CSS_SELECTOR, ID, LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME, XPATH.
        element_locator_path : str
            This is the address of given element_locator_type.

        Returns
        -------
        tuple
            This is bool representing if web_element found or not.
            object - web element from selenium. selenium.webdriver.remote.webelement.WebElement

        """
        try:
            print("trying")
            web_element = self.find_web_element(element_locator_type, element_locator_path)
            web_element_found = True
        except Exception:
            web_element_found = False
            web_element = None
        return web_element_found, web_element

    def find_web_element(self, element_locator_type: str, element_locator_path: str):
        """
        click on button on web by searching element_locator_path

        Parameters
        ----------
        element_locator_type : str
            these by selenium methods to locate web element. This function contains
                CLASS_NAME, CSS_SELECTOR, ID, LINK_TEXT, NAME, PARTIAL_LINK_TEXT, TAG_NAME, XPATH.
        element_locator_path : str
            This is the address of given element_locator_type.

        Returns
        -------
        object
            selenium.webdriver.remote.webelement.WebElement, It could be input_box or button etc.

        """
        if element_locator_type.upper() == "CLASS_NAME":
            web_element = self.driver.find_element(By.CLASS_NAME, element_locator_path)
        elif element_locator_type.upper() == "CSS_SELECTOR":
            web_element = self.driver.find_element(By.CSS_SELECTOR, element_locator_path)
        elif element_locator_type.upper() == "ID":
            web_element = self.driver.find_element(By.ID, element_locator_path)
        elif element_locator_type.upper() == "LINK_TEXT":
            web_element = self.driver.find_element(By.LINK_TEXT, element_locator_path)
        elif element_locator_type.upper() == "NAME":
            web_element = self.driver.find_element(By.NAME, element_locator_path)
        elif element_locator_type.upper() == "PARTIAL_LINK_TEXT":
            web_element = self.driver.find_element(By.PARTIAL_LINK_TEXT, element_locator_path)
        elif element_locator_type.upper() == "TAG_NAME":
            web_element = self.driver.find_element(By.TAG_NAME, element_locator_path)
        elif element_locator_type.upper() == "XPATH":
            web_element = self.driver.find_element(By.XPATH, element_locator_path)
        else:
            raise ValueError("This function doesn't implement your element_locator_type, please try modifying this "
                             "function or write separately!")
        return web_element


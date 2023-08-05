"""Module: browser_setup
This is the sole of the python package. It helps setup the required browser and with custom options.
"""

from selenium.webdriver.chrome.options import Options
from browser_automation import os_json_utils


class CustomOptions:
    def __init__(self, custom_browser_options_json_path=None):
        """This sets and gets the custom browser options.

        Parameters
        ----------
        custom_browser_options_json_path : dict
            This is the dictionary of browser options.
        """
        self.browser_custom_dict = {"browser_type": "Chrome as default",
                                    "browser_custom_options": [{"add_extension": None},
                                                               {"add_argument": ["iterate", "--start-maximized",
                                                                                 "--ignore-certificate-errors",
                                                                                 "--disable-blink-features",
                                                                                 "--disable-blink-features=AutomationControlled"]},
                                                               {"add_experimental_option": ["unpack", "prefs",
                                                                                            {"download.default_directory": None,
                                                                                             "download.prompt_for_download": False,
                                                                                             "download.directory_upgrade": True,
                                                                                             "plugins.always_open_pdf_externally": True}]}]}

        self.custom_browser_options_json_path = custom_browser_options_json_path
        if self.custom_browser_options_json_path is None:
            self.browser_custom_options = self.browser_custom_dict
        else:
            self.browser_custom_options = os_json_utils.read_json_file_from_path(self.custom_browser_options_json_path)

    def get_default_custom_options_json(self, output_file_path: str = "custom_options.json"):
        """This function write a sample json file for the user to edit for custom options.

        Parameters
        ----------
        output_file_path : str
            This is the path for writing the sample json file.

        Returns
        -------
        None

        """
        os_json_utils.write_json_file_with_dict(output_file_path, self.browser_custom_dict)

    def get_browser_custom_options_dict(self):
        """returns browser custom options dict.

        Returns
        -------
        dict
            This provide the list of current browser options.

        """
        return self.browser_custom_dict


class Setup:

    def __init__(self, custom_browser_options_json_path=None):
        """This install the default browser with default options unless custom_browser_options_json_path is not None.
        This contains many choices of browsers. Example - Chromium, Firefox, IE , Edge, Opera.

        Parameters
        ----------
        custom_browser_options_json_path : str
            This is the path of the json file edited by user to get some custom options of browser.
        """
        self.download_dir = os_json_utils.get_download_location_path()
        self.options = Options()
        self.custom_browser_options_json_path = custom_browser_options_json_path
        browser_custom_options = CustomOptions(self.custom_browser_options_json_path).get_browser_custom_options_dict()
        if "browser_custom_options" in browser_custom_options:
            for method_name_argument_value_dict in browser_custom_options["browser_custom_options"]:
                for method_name, argument_value in method_name_argument_value_dict.items():
                    if argument_value is None:
                        continue
                    elif type(argument_value) is list:
                        if argument_value[0] == "iterate":
                            for argument in argument_value:
                                getattr(self.options, method_name)(argument)
                        elif argument_value[0] == "unpack":
                            if method_name == "add_experimental_option" and \
                                    argument_value[2]["download.default_directory"] is not None:
                                self.download_dir = argument_value[2]["download.default_directory"]
                            getattr(self.options, method_name)(*argument_value[1:])
                        else:
                            getattr(self.options, method_name)(argument_value)
                    else:
                        getattr(self.options, method_name)(argument_value)

        if "browser_type" in browser_custom_options:
            if browser_custom_options["browser_type"] == "Chromium":
                # Use with Chromium:
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.utils import ChromeType
                self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                                               options=self.options)

            elif browser_custom_options["browser_type"] == "FireFox":
                # Use with FireFox:
                from selenium import webdriver
                from webdriver_manager.firefox import GeckoDriverManager
                self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)

            elif browser_custom_options["browser_type"] == "IE":
                # Use with IE
                from selenium import webdriver
                from webdriver_manager.microsoft import IEDriverManager
                self.driver = webdriver.Ie(IEDriverManager().install(), self.options)

            elif browser_custom_options["browser_type"] == "Edge":
                # Use with Edge
                from selenium import webdriver
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                # pip install msedge-selenium-tools
                # from msedge.selenium_tools import EdgeOptions
                # self.options = EdgeOptions()
                # self.options.use_chromium = True
                self.driver = webdriver.Edge(EdgeChromiumDriverManager().install(), self.options)

            elif browser_custom_options["browser_type"] == "Opera":
                # Use with Opera
                from selenium import webdriver
                from webdriver_manager.opera import OperaDriverManager
                self.driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=self.options)

            else:
                # Use with Chrome:
                from selenium import webdriver
                from webdriver_manager.chrome import ChromeDriverManager
                self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)


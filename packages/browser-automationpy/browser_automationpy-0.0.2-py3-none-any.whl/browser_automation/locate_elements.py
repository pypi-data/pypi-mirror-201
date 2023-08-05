"""Module: locate_element
This module help in getting the address for selenium.webdriver.remote.webelement.WebElement
Note - Try using the extension for finding the web elements rather than this module. Use this as the last resort.
Examples - My favorite https://selectorshub.com/ This website contains full documentation and videos. Just provide the
extension filepath in browser setup options. Other example - https://www.ranorex.com/selocity/browser-extension/,
'chropath' https://chrome.google.com/webstore/detail/chropath/ljngjbnaijcbncmcnjfhigebomdlkcjo
"""

import re


def get_element_value(element_name_value: str) -> list:
    """
    This function uses regex patter to find the element value from element name and value

    Parameters
    ----------
    element_name_value : str
        element name and element value ex: id="ember51"
    Returns
    -------
    list
        get element value ex: ember51
    """
    regex = '"[\w-]+"'
    element_value = re.findall(regex, element_name_value)
    element_value = str(element_value)
    regex1 = '[\w-]+'
    element_value = re.findall(regex1, element_value)

    return element_value


class LocateElements:
    def __init__(self, html_source_code):
        """This class try to use regex to find elements types with addresses.

        Parameters
        ----------
        html_source_code : str
            This is the source code of the html.
        """
        self.html_source_code = html_source_code

    def snippet_html(self, word_seen_in_website: str) -> str:
        """Get the important chunk of html source code

        Parameters
        ----------
        word_seen_in_website : str
            word that you see in input box on website

        Returns
        -------
        str
            snippet of Html which has your element Name

        """
        word_seen_in_website = str(word_seen_in_website)
        regex = "<.+" + word_seen_in_website + ".+>"
        snippet_html_text = re.findall(regex, self.html_source_code)
        snippet_html_text = str(snippet_html_text)
        return snippet_html_text

    def get_element_name_value_regex(self, element_name: str, word_seen_in_website: str):
        """This get element locator type and its value or address.

        Parameters
        ----------
        element_name : str
            ID, Name, Class etc. of html element
        word_seen_in_website : str
            snippet of Html which has your element Name

        Returns
        -------
        list
            This contains list of element type and address.

        """
        element_name = element_name.lower()
        regex = str(element_name) + '="[\w-]+"'
        element_name_and_value = re.findall(regex, self.snippet_html(word_seen_in_website))

        return element_name_and_value

    def get_element_value_from_html(self, word_seen_in_website: str, element_name: str) -> list:
        """This return only the address of web element of required element type.

        Parameters
        ----------
        word_seen_in_website : str
            word that you see in input box on website
        element_name : str
            ID, Name, Class etc. of html element

        Returns
        -------
        list
            get element value ex: ember51

        """
        element_name_value = self.get_element_name_value_regex(element_name, self.snippet_html(word_seen_in_website))
        value = get_element_value(str(element_name_value))
        return value

    def get_link_via_regex(self):
        """
        Specific function for IEEE xplore pdf open button

        Returns
        -------
        str
            link of some sort from website

        """
        regex = r'src="([^"]*)'
        element_name_and_value = re.findall(regex, self.html_source_code)
        link = str(element_name_and_value[-1])
        return link


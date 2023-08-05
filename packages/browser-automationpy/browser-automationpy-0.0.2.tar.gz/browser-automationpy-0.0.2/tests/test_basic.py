# -*- coding: utf-8 -*-

from browser_automation.browser_manipulation import Interactions
"""import unittest


class BasicTestSuite(unittest.TestCase):
    #Basic test cases
    pass"""

def main():
    fire = Interactions()
    fire.driver.get("https://www.selenium.dev/documentation/getting_started/")

if __name__ == '__main__':
    main()

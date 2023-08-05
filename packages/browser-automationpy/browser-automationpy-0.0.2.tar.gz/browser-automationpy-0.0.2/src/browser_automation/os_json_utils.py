"""Module: os_json_utils
This module contains functions related to getting or writing files from os. This also include json read and write
functions for use in browser options. This also contains sleeping and waiting for the file to be downloaded.
"""

import json
import os
import platform
import shutil
import time
import random


def finding_grandparent_dir_from_cwd():
    """This provide the grand parent directory from current working directory.

    Returns
    -------
    str
        grand parent directory name

    """
    present_dir = os.getcwd()
    parent_dir = os.path.dirname(present_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    return grandparent_dir


def config_file_path(config_name: str = "config.json"):
    """This is useful if config file is in grandparent directory.

    Parameters
    ----------
    config_name : str
        This is the name of json config file.

    Returns
    -------
    str
        path of the config file at grandparent directory.

    """
    grandparent_dir = finding_grandparent_dir_from_cwd()
    config_path = os.path.join(grandparent_dir, config_name)
    return config_path


def write_json_file_with_dict(output_file_path: str, input_dict: dict):
    """Write json file at output_file_path with the help of input dictionary.

    Parameters
    ----------
    output_file_path : str
        This is the path of output file we want, if only name is provided then it will export json to the script path.
    input_dict : dict
        This is the python dictionary which we want to be saved in json file format.

    Returns
    -------
    None
        Function doesn't return anything but write a json file at output_file_path.

    """
    with open(output_file_path, "w") as outfile:
        json.dump(input_dict, outfile)


def read_json_file_from_path(json_file_path: str) -> dict:
    """Read the json file from the path given. Convert json file data to the python dictionary.

    Parameters
    ----------
    json_file_path : str
        This is the json file path which is needed to be converted.

    Returns
    -------
    dict
        This is the data in dict format converted from json file.

    """
    with open(json_file_path, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
        return json_object


def avoid_lock():
    """
    this uses mouse and keyboard to act human is using the computer

    Returns
    -------
    None

    """
    try:
        import pyautogui
    except ImportError:
        print("This function requires pyautogui library. Please install it using 'pip install PyAutoGUI' "
              "visit https://pypi.org/project/PyAutoGUI/ for more information.")
        return ""

    x, _ = pyautogui.position()
    pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
    pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('esc')
    pyautogui.keyUp('ctrl')
    pyautogui.press('esc')


def sleep(time_duration: float):
    """
    this function sleep for given Time

    Parameters
    ----------
    time_duration : float
        This is the duration of time, you want script to sleep.

    Returns
    -------
    None

    """
    print(f"Sleeping for {round(time_duration, 1)}")
    time.sleep(time_duration)


def get_download_location_path() -> str:
    """Get the default download location based on operating system. Written for chrome.

    Returns
    -------
    str
        default download location of browser.

    """
    current_os = platform.system()
    username = os.getlogin()
    if current_os == "Linux":
        default_download_path = f"/home/{username}/Downloads"
    elif current_os == "Darwin":
        default_download_path = f"/Users/{username}/Downloads"
    elif current_os == "Windows":
        default_download_path = f"\\Users\\{username}\\Downloads"
    else:
        default_download_path = input("please provide the default download location of your browser")
    return default_download_path


class RandomSleep:
    def __init__(self, lower_time_limit: float = 5, upper_time_limit: float = 15.3):
        """This class contains methods related to make programme sleep for some exact or random time.

        Parameters
        ----------
        lower_time_limit : float
            This is the least amount of duration we want programme to sleep.
        upper_time_limit : float
            This is the maximum amount of duration we want programme to sleep.

        """
        self.lower_time_limit = lower_time_limit
        self.upper_time_limit = upper_time_limit

    def random_time(self):
        """
        this gives random_time between lower_time_limit and upper_time_limit.

        Returns
        -------
        float
            This contains random value between lower and upper time limit.

        """
        random_out_time = random.uniform(self.lower_time_limit, self.upper_time_limit)
        return random_out_time

    def sleep_for_random_time(self):
        """
        this sleep for some time

        Returns
        -------
        None

        """
        random_time_duration = self.random_time()
        print(f"Sleeping for {round(random_time_duration, 1)}")
        time.sleep(random_time_duration)

    def sleep_after_n_monotonous_work(self, n: int, monotonous_work: int, random_sleep_multiple: float = 15):
        """
        sleep every n applications

        Parameters
        ----------
        n : int
            This signify number of loop or repetitive tries.
        monotonous_work : int
            temporary variable to count the repetitive tries.
        random_sleep_multiple : float
            This is the value by which you want to multiply the random time.

        Returns
        -------
        None

        """
        if monotonous_work != 0 and monotonous_work % n == 0:
            time.sleep(random_sleep_multiple * self.random_time())


class DownloadUtil:
    def __init__(self, download_dir: str):
        """This help in moving the downloaded data to destination folder and waiting unto data is downloaded.

        Parameters
        ----------
        download_dir : str
            This is the address of download location.
        """
        self.download_dir = download_dir

    def download_completion_wait(self, timeout: int = 300, files_counts: int = None):
        """
        Wait for downloads to finish with a specified timeout.
        author: https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed

        Parameters
        ----------
        timeout : int
            How many seconds to wait until timing out.
        files_counts : str
            If provided, also wait for the expected number of files.

        Returns
        -------
        None

        """
        seconds = 0
        waiting = True
        while waiting and seconds < timeout:
            time.sleep(1)
            waiting = False
            files = os.listdir(self.download_dir)
            if files_counts and len(files) != files_counts:
                waiting = True

            for filename in files:
                if filename.endswith('.crdownload'):
                    waiting = True

            seconds += 1

    def file_rename_and_moving(self, destination_folder_path: str, new_name: str = None):
        """
        This function waits with timeout option until file is downloaded in origin folder. then
        rename and move it to destination folder.

        Parameters
        ----------
        destination_folder_path : str
            This is the address of destination folder where we want to move files from download location.
        new_name : str
            This is the new name of file we just downloaded and want to change previous name.

        Returns
        -------
        None

        """
        self.download_completion_wait()
        filename = max([self.download_dir + "/" + f for f in os.listdir(self.download_dir)], key=os.path.getctime)
        if new_name:
            name_with_extension = replace_symbols_with_space(str(new_name)) + ".pdf"
            shutil.move(filename, os.path.join(destination_folder_path, str(name_with_extension)))
        else:
            shutil.move(filename, os.path.join(destination_folder_path, str(os.path.basename(filename))))
        print("file renamed and moved")


def replace_symbols_with_space(string: str) -> str:
    """replace symbols in string with spaces. Example - 'df%$df' -> 'df  df'

    Parameters
    ----------
    string : str
        This is input word string which contains unwanted symbols.

    Returns
    -------
    str
        This is cleaned string from symbols and contains only alpha characters and all lowercase character string.

    """
    alpha = ""
    for character in string:
        if character.isalpha():
            alpha += character
        elif character == " ":
            alpha += character
        else:
            alpha += " "
    return alpha


def list_to_text_file(filename: str, list_name: str, permission: str = "w"):
    """This converts list to text file and put each element in new line.

    Parameters
    ----------
    filename : str
        This is the name to be given for text file.
    list_name : list
        This is the python data structure list which contains some data.
    permission : str
        These are the os permissions given for the file. check more lemma_info on python library 'os'.

    Returns
    -------
    None

    """
    with open(filename, permission) as file:
        for i in list_name:
            file.write(str(i))
            file.write("\n")


def load_text_file_to_list(file_path: str, permission: str = "r"):
    """This converts text file to list and put each line in list as single element. get first line of text file by
    list[0].

    Parameters
    ----------
    file_path : str
        This is the name to be given for text file.
    permission : str
        These are the os permissions given for the file. check more lemma_info on python library 'os'.

    Returns
    -------
    list
        This contains all lines loaded into list with one line per list element. [first line, second line,.... ]

    """
    with open(file_path, permission) as file:
        file_object = file.read()

    return file_object.split("\n")

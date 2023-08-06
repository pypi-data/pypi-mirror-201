#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import warnings
import sys
import re
import osta.__utils as utils
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from os import listdir
from os.path import isfile, isdir, join
from osta.__utils_imports import read_file, change_names


def searchData(
        search_words="ostolasku", log_file=False, verbose=True, **args):
    """
    Fetch the URL addresses of downloadable datasets of Avoindata.fi.

    Arguments:
        `search_words`: A string specifying search words used to search
        datasets from the database. (By default: "ostolasku")

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function does a search to Avoindata.fi
        (https://www.avoindata.fi/data/fi/dataset) based on provided search
        words. The returned value contains URL addresses of files that can be
        loaded from the website.

    Examples:
        ```
        # Search all purchase data
        df = searchData("ostolasku")
        # Search only purchase data of Turku
        df = searchData("ostolasku Turku")
        ```

    Output:
        pandas.DataFrame with URL addresses.

    """
    # INPUT CHECK
    if not (isinstance(search_words, str) or isinstance(search_words, list)):
        raise Exception(
            "'search_words' must be a string or a list."
            )
    if not (isinstance(log_file, str) or isinstance(log_file, bool)):
        raise Exception(
            "'log_file' must be a boolean value or a string specifying a path."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # If user wants to create a logger file
    if log_file:
        # Create a logger with file
        logger = utils.__start_logging(__name__, log_file)
    # Initialize result df
    df = pd.DataFrame()
    # If search_words is a list, search word will be just "osta" and results
    # are subsetted later
    word = "osto" if isinstance(search_words, list) else search_words
    # Get query for searching pages that contain data
    url = "https://www.avoindata.fi"
    query = url + "/data/fi/" + "dataset?q=" + word
    # Search
    r = requests.get(query)
    # If the search was succesful
    if r.ok:
        # Parse dataset and find pages / individual search results
        soup = BeautifulSoup(r.content, "html.parser")
        pages = soup.find_all("div", {"class": "dataset-item"})
        # Find how many pages there are in total in the search results
        page_nums = soup.find_all("ul", {"class": "pagination"})
        if len(page_nums) > 0:
            page_nums = page_nums[0]
            page_nums = page_nums.findAll("a")  # type: ignore
            pattern = re.compile(r"page=")
            page_nums = [int(x.get("href").split("page=")[1])  # type: ignore
                         for x in page_nums if
                         bool(pattern.findall(x.get("href")))]
            max_page = max(page_nums)
        else:
            max_page = 1
        # Find how many results there are in total
        tot_num_res = soup.find(
            "h3", {"class": "m-0 search-form__result-text"}
            ).text  # type: ignore
        tot_num_res = re.findall(r'[0-9]+', tot_num_res)
        tot_num_res = int(tot_num_res[len(tot_num_res)-1])
        i = 1
        # For progress bar, specify the width of it
        progress_bar_width = 50
        for num in range(1, max_page+1):
            # If not the first page (which is already loaded), load the page
            # specified by num (if only one page, this goes through only once)
            if num != 1:
                query = (url + "/data/fi/" + "dataset?q=" +
                         word + "&page=" + str(num))
                # Search
                r = requests.get(query)
                # Parse dataset and find pages / individual search results
                soup = BeautifulSoup(r.content, "html.parser")
                pages = soup.find_all("div", {"class": "dataset-item"})
            # Loop through individual search results in the page
            for page in pages:
                # Update the progress bar
                if verbose:
                    percent = 100*((i)/tot_num_res)
                    i += 1
                    sys.stdout.write('\r')
                    sys.stdout.write("Completed: [{:{}}] {:>3}%"
                                     .format('='*int(
                                         percent/(100/progress_bar_width)),
                                             progress_bar_width, int(percent)))
                    sys.stdout.flush()
                # Get url to the search result page
                title_element = page.find(
                    "h3", class_="dataset-heading dataset-title")
                page_url = title_element.find(
                    "a", href=True)['href']
                # Create a new query to the individual page
                query_temp = url + page_url
                page_data = requests.get(query_temp)
                # Parse and get json script
                soup = BeautifulSoup(page_data.content, "html.parser")
                text = soup.find("script", type="application/ld+json")
                text = json.loads(text.text)  # type: ignore
                # Extract graph data from the script
                text = text["@graph"]  # type: ignore

                # Initialize lists
                id_list = []
                url_list = []
                format_list = []
                info_list = []
                # Loop thourh dataset info
                for dataset in text:  # type: ignore
                    # If the information is about data
                    if dataset["@type"  # type: ignore
                               ] == 'schema:DataDownload':
                        # Add info to lists
                        id_list.append(dataset["@id"])  # type: ignore
                        url_list.append(dataset["schema:url"])  # type: ignore
                        info_list.append(
                            dataset["schema:name"])  # type: ignore
                        if ("schema:encodingFormat" in
                            dataset.keys(  # type: ignore
                                )):
                            format_list.append(dataset[
                                "schema:encodingFormat"])  # type: ignore
                        else:
                            format_list.append(None)

                # Extract title
                name = soup.find("head").find("title").string  # type: ignore
                # Create temporary DataFrame
                df_temp = pd.DataFrame({"name": [str(name)]*len(id_list),
                                        "page": [str(query_temp)]*len(id_list),
                                        "url": url_list,
                                        "id": id_list,
                                        "format": format_list,
                                        "info": info_list})

                # Add data to main DataFrame
                df = pd.concat([df, df_temp])
        # If user wanted to search based on municipalities, subset the data
        if isinstance(search_words, list):
            # Match "osto" and municipality
            pattern = r"(?=.*(" + word + ").*)"  # type: ignore
            r = re.compile(pattern)  # type: ignore
            dfs = df.astype(str, copy=True, errors="raise")
            # Find search word ("osta") and municipalities
            # (with loose match - 80%)
            scorer = fuzz.partial_ratio
            ind = dfs.applymap(lambda x: bool(
                r.match(x.lower()) and process.extractOne(  # type: ignore
                    x, search_words, scorer=scorer)[1] > 80)).sum(
                axis=1) > 0
            # Subset the data; take only those rows that had correct results
            df = df.loc[ind, :]
        # Reset index
        df = df.reset_index(drop=True)
        # Stop progress bar
        if verbose:
            sys.stdout.write("\n")
    else:
        warnings.warn(
            message="Retrieving URL addresses was not successful.",
            category=Warning
            )
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging(logger)
    return df


def getData(file_path, as_df=True, log_file=False, verbose=True, **args):
    """
    Read single CSV or Excel file to pandas.DataFrame.

    Arguments:
        `file_path`: A string specifying the path or URL address to the file.

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

        `**args`: Additional arguments passes into other functions:

        'save_dir': A string specifying to which directory fetched files are
        stored. If None, files are not stored. (By default: save_dir=None)

    Details:
        This function reads files to pd.DataFrame.

    Examples:
        ```
        df_urls = searchData("ostolasku")
        df_list = getData(df_urls.loc[:, "url"])
        ```

    Output:
        pandas.DataFrame or list of pd.DataFrames if file path specifies
        zipped directory with multiple files.

    """
    # INPUT CHECK
    if not (isinstance(file_path, list) or isinstance(file_path, pd.Series)
            or isinstance(file_path, str)):
        raise Exception(
            "'file_path' must be a list of strings."
            )
    if isinstance(file_path, str):
        file_path = [file_path]
    if not isinstance(as_df, bool):
        raise Exception(
            "'as_df' must be a boolean value."
            )
    if not (isinstance(log_file, str) or isinstance(log_file, bool)):
        raise Exception(
            "'log_file' must be a boolean value or a string specifying a path."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # If user wants to create a logger file
    if log_file:
        # Create a logger with file
        logger = utils.__start_logging(__name__, log_file)
    # If the file_path contains only one path, create a list from it
    if isinstance(file_path, str):
        file_path = [file_path]
    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop through file paths
    df_list = []
    for i, path_temp in enumerate(file_path):
        # Update the progress bar
        if verbose:
            percent = 100*((i+1)/len(file_path))
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Get the name of the file (or the element number)
        # and add info to log file
        if log_file:
            logger.info(f'File: {path_temp}')
        # Try to load, give a warning if not success
        try:
            df = read_file(path_temp, **args)
            # Convert to list if it is not already
            if not isinstance(df, list):
                df = [df]
            # Add to results
            df_list.extend(df)
        except Exception:
            warnings.warn(
                message=f"Error while loading the following path. "
                f"It is excluded from the output: \n {path_temp}",
                category=UserWarning)
    # Merge list to one DF
    if as_df and len(df_list) > 0:
        res = pd.concat(df_list)
    else:
        res = df_list
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging()
    return res


def detectFields(
        df_list, save_dir=None, log_file=False, verbose=True, **args):
    """
    Change column names of pandas.DataFrame

    This function is used to change column names of pandas.DataFrame.
    The column names are changed into standardized format that all other
    functions in osta package require.

    Arguments:
        `df`: pandas.DataFrame containing invoice data or list of pd.DataFrames
        or paths to files.

        `guess_names`: A boolean value specifying whether to guess column names
        that did not have exact matches or not. (By default: guess_names=True)

        `make_unique`: A boolean value specifying whether to add a suffix to
        duplicated column names. (By default: make_unique=True)

        `fields`: A pandas.DataFrame or a dictionary containing
        matches between existing column names (key) and
        standardized names (value), a string specifying a path
        to such CSV file or None. When fields=None,function's
        default dictionary is used. (By default: fields=None)

        `**args`: Additional arguments passes into other functions:

        `pattern_th`: A numeric value [0,1] specifying the threshold of
        enough good match. Value over threshold have enough strong
        pattern and it is interpreted to be a match.
        (By default: pattern_th=0.9)

        `scorer`: A scorer function passed into fuzzywuzzy.process.extractOne
        function. (By default: scorer=fuzz.token_sort_ratio)

        `match_th`: A numeric value [0,1] specifying the strength of
        pattern in the data. The observation specifies the portion of
        observations where the pattern must be present to conclude that
        column includes specific type of data. (By default: match_th=0.2)

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        Disabled when 'df' is a single pd.DataFrame. (By default: verbose=True)

        'change_optional': A boolean value specifying whteher to change column
        names of fields that are not required in municipality reporting.
        (By default: change_optional=True)

    Details:
        This function changes the column names to standardized names that are
        required in other functions in osta package. If the names are already
        in standardized format, the function works as checker as it gives
        warnings if certain name was not detected or it has been changed with
        non-exact match.

        First, the function checks if exact match is found between existing
        column names and names in dictionary. If the natch was found, certain
        column name is replaced with standardizd name.

        Secondly, if there are column names that did not have exact match, user
        can specify whether matches are checked more loosely. The function
        checks if a pattern of values of undetected column matches with pattern
        of certain data types that are expected to be in invoice data. The
        checking is done with "fail-safe" principle to be sure that matches are
        found with the highest possible accuracy.

        If a match is not detected, the function tries to find if
        the column name resembles one of the names in dictionary.
        If the signal is strong enough, the column name is is changed.
        Otherwise, the column name stays unmodified.

    Examples:
        ```
        # Create a dummy data
        data = {"name1": ["FI", "FI", "FI"],
                "päivämäärä": ["02012023", "2-1-2023", "1.1.2023"],
                "name3": [1, 2, 2],
                "org_name": ["Turku", "Turku", "Turku"],
                "supplier": ["Myyjä", "Supplier Oy", "Myyjän tuote Oy"],
                "summa": [100.21, 10.30, 50.50],
                }
        df = pd.DataFrame(data)
        # Change those column names that are detected based on column name
        # and pattern of the data.
        df = change_names(df)

        # To disable name guessing, use guess_names=False
        df = change_names(df, guess_names=False)

        # To control name matching, feed arguments
        df = change_names(df, guess_names=True, make_unique=True,
                          pattern_th=0.6, match_th=1)
        ```

    Output:
        pandas.DataFrame with standardized column names or a list of
        pd.DataFrames.

    """
    # INPUT CHECK
    if not (isinstance(df_list, list) or isinstance(df_list, str) or
            isinstance(df_list, pd.DataFrame)):
        raise Exception(
            "'df_list' must be a list of pd.DataFrames, single " +
            "pd.DataFrame or paths to files."
            )
    if isinstance(df_list, pd.DataFrame):
        df_list = [df_list]
        verbose = False
    if not (isinstance(save_dir, str) or save_dir is None):
        raise Exception(
            "'save_dir' must be None or string specifying directory to where ",
            "result files will be stored."
            )
    if not (isinstance(log_file, str) or isinstance(log_file, bool)):
        raise Exception(
            "'log_file' must be a boolean value or a string specifying a path."
            )
    # If df_list is directory, check that it is correct directory
    if isinstance(df_list, str) and not isdir(df_list):
        raise Exception(
            "Directory specified by 'df_list' not found."
            )
    elif isinstance(df_list, str) and isdir(df_list):
        # If it is directory, get all the files inside it
        df_list = [join(df_list, f) for f in listdir(df_list)
                   if isfile(join(df_list, f))]
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # If user wants to create a logger file
    if log_file:
        # Create a logger with file
        logger = utils.__start_logging(__name__, log_file)

    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop over list elements
    res = []
    for i, x in enumerate(df_list):
        # Update the progress bar if specified
        if verbose:
            percent = 100*((i+1)/len(df_list))
            # i += 1
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(
                                 percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Get the name of the file (or the element number)
        # and add info to log file
        if log_file:
            msg = x if isinstance(x, str) else ("element " + str(i))
            logger.info(f'File: {msg}')
        # Check if it is pd.DataFrame. Otherwise try to load it as a local file
        df_is_DF = True
        if not isinstance(x, pd.DataFrame):
            # Try to load it
            try:
                df = utils.__detect_format_and_open_file(
                    x, only_first=True, **args)
            except Exception:
                df_is_DF = False
                warnings.warn(
                    message="Failed to open the file.",
                    category=UserWarning
                    )
        else:
            df = x
        # If the file is not DF and it was not possible to load
        if df_is_DF:
            # Change names from individual file
            df = change_names(df, **args)
            # Add to result list
            res.append(df)
            # Save file if list contained paths or if specified
            if isinstance(x, str) or save_dir is not None:
                # Get correct path
                x = x if isinstance(x, str) else join(str(save_dir), x)
                df.to_csv(x, index=False)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging()
    # If result contains only one element, give only the element
    if len(res) == 1:
        res = res[0]
    return res

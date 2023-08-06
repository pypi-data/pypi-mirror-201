#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import tempfile
import urllib.request
from zipfile import ZipFile
import shutil
import os
import filetype
import osta.__utils as utils
import pandas as pd
import warnings
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pkg_resources


def read_file(file_path, temp_dir=None, **args):
    """
    Read single CSV or Excel file to pandas.DataFrame.

    Arguments:
        `file_path`: A string specifying the path or URL address to the file.

    Details:
        This function reads files to pd.DataFrame.

    Examples:
        ```
        ```

    Output:
        pandas.DataFrame or list of pd.DataFrames if file path specifies
        zipped directory with multiple files.

    """
    # INPUT CHECK
    if not isinstance(file_path, str):
        raise Exception(
            "'file_path' must be a string."
            )
    if not (isinstance(temp_dir, str) or temp_dir is None):
        raise Exception(
            "'temp_dir' must be None or string specifying temporary directory."
            )
    # INPUT CHECK END
    # If the file is not located in the local machine
    if not os.path.exists(file_path):
        # Store the file_path to url variable
        url = file_path
        # If user has not specified temporary directory, get the default
        if temp_dir is None:
            # Get the name of higher level tmp directory
            temp_dir_path = tempfile.gettempdir()
            temp_dir = temp_dir_path + "/osta"
        # Check if spedicified directory exists. If not, create it
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        # Get file path were final file will be stored
        save_file_name = file_path.split("/")
        save_file_name = save_file_name[-1]  # type: ignore
        # Get temporary file path
        file_path = file_path.replace("/", "_")
        file_path = os.path.join(temp_dir, file_path)
        # Try to access the file based on url address if it is not already
        # laoded in cache
        if not os.path.exists(file_path):
            try:
                urllib.request.urlretrieve(url, file_path)
            except Exception:
                raise ValueError(
                    "'file_name' is not a correct path to local file "
                    "and it was not possible to retrieve file based "
                    "on URL address specified by 'file_name'.")

    # Test if the data is in zip format
    file_type = filetype.guess(file_path)
    if file_type is not None and file_type.extension == "zip":
        # Path for extracted files
        extract_path = os.path.join(tempfile.gettempdir(),
                                    "invoice_tempfile_ext.tmp")
        # Remove files from the dir if it already exists
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        # Extract files
        with ZipFile(file_path, 'r') as zip:
            zip.extractall(extract_path)
        # Get all the file paths in extracted folder
        file_path = []
        for path, subdirs, files in os.walk(extract_path):
            for name in files:
                file_path.append(os.path.join(path, name))

    # If the file_path contains only one path, create a list from it
    if isinstance(file_path, str):
        file_path = [file_path]

    # Loop over file paths
    dfs = []
    for path_temp in file_path:
        # Open file as DataFrame
        df = __open_and_save_file(
            path_temp, save_file_name=save_file_name, **args)
        # Convert to list if it is not already
        # (there can be excel file with multiple sheets)
        if not isinstance(df, list):
            df = [df]
        # Add to results
        dfs.extend(df)
    # If there is only one DF in list, return only the DF
    if len(dfs) == 1:
        dfs = dfs[0]
    return dfs


def __open_and_save_file(
        file_path, save_dir=None, save_file_name=None,
        encoding=None, guess_encoding=True,
        delimiter=None, guess_delimiter=True,
        polish_data=True, change_colnames=False,
        **args):
    """
    This function is a helper function to load and detect the format of the
    file that cab be found from the disk and that is not zipped.
    The returned value is pandas.DataFrame.
    """
    # INPUT CHECK
    if not (isinstance(save_dir, str) or save_dir is None):
        raise Exception(
            "'save_dir' must be None or string specifying temporary directory."
            )
    if not (isinstance(save_file_name, str) or save_file_name is None):
        raise Exception(
            "'save_file_name' must be None or string specifying temporary ",
            "directory."
            )
    if not isinstance(polish_data, bool):
        raise Exception(
            "'polish_data' must be a boolean value."
            )
    # INPUT CHECK END
    # Open the file
    df_list = utils.__detect_format_and_open_file(file_path, **args)
    # Convert to list if it is not already
    # (there can be excel file with multiple sheets)
    if not isinstance(df_list, list):
        df_list = [df_list]
    # Loop through DataFrames
    res = []
    for df in df_list:
        # Polish data, i.e., remove empty rows and columns
        if polish_data:
            # Remove spaces from beginning and end of the value
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            # Replace empty strings with None
            df = df.replace(r'^\s*$', None, regex=True)
            # Drop empty rows
            df.dropna(axis=0, how='all', inplace=True)
            # Drop empty columns
            df.dropna(axis=1, how='all', inplace=True)

            # If the first row contained empty values, there are columns named
            # "Unnamed". Replace column names with the values of the first row
            if any([True if x.find('Unnamed') != -1 else False
                    for x in df.columns]):
                df.columns = df.iloc[0, :].values
                df = df.iloc[1:, :]

            # If there are columns with only spaces
            bools = [all(df.iloc[:, x[0]].astype(str).str.isspace())
                     for x in enumerate(df.columns)]
            if any(bools):
                df = df.loc[:, [not x for x in bools]]
        # Change colnames if specified
        if change_colnames:
            df = change_names(df, **args)
        # If save_dir is not None, save the file to specified folder
        if save_dir is not None:
            # Check if spedicified directory exists. If not, create it
            if not os.path.isdir(save_dir):
                os.makedirs(save_dir)
            # Get file_name if not provided
            if save_file_name is not None:
                file_path = save_file_name
            else:
                file_path = file_path.split("/")
                file_path = file_path[-1]
            file_path = re.split(r".csv|.xls|.xlsx", file_path)
            file_path = file_path[0]
            file_path = os.path.join(save_dir, file_path)
            # Save file, do not overwrite
            if os.path.exists(file_path + ".csv"):
                i = 2
                while os.path.exists(f"{file_path} ({str(i)}).csv"):
                    i += 1
                file_path = file_path + " (" + str(i) + ")"
            file_path = file_path + ".csv"
            df.to_csv(file_path, index=False)
        # Store file to result variable
        res.append(df)
    # Give only the DF if list contains only one
    if len(res) == 1:
        res = res[0]
    return df


# detectFields


def change_names(df, guess_names=True, make_unique=True, fields=None, **args):
    """
    Change column names of pandas.DataFrame

    This function is used to change column names of pandas.DataFrame.
    The column names are changed into standardized format that all other
    functions in osta package require.

    Arguments:
        `df`: pandas.DataFrame containing invoice data.

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
        pandas.DataFrame with standardized column names.

    """
    # INPUT CHECK
    # df must be pandas DataFrame
    if not utils.__is_non_empty_df(df):
        raise Exception(
            "'df' must be non-empty pandas.DataFrame."
            )
    # guess_names must be boolean
    if not isinstance(guess_names, bool):
        raise Exception(
            "'guess_names' must be bool."
            )
    # make_unique must be boolean
    if not isinstance(make_unique, bool):
        raise Exception(
            "'make_unique' must be bool."
            )
    # fields must be DataFrame or None
    if not (utils.__is_non_empty_df(fields) or
            isinstance(fields, dict) or isinstance(fields, str)
            or fields is None):
        raise Exception(
            "'fields' must be pd.DataFrame, dict, string or None."
            )
    # INPUT CHECK END
    # Get fields / matches between column names and standardized names
    fields = __get_fields_df(fields, **args)
    # Initialize lists for column names
    colnames = []
    colnames_not_found = []
    colnames_not_found_i = []
    # Loop over column names
    for i, col in enumerate(df.columns):
        # Column name to lower case and remove spaces from beginning and end
        # Get matching value from the dictionary
        col_name = fields.get(col.lower().strip())
        # If exact match was not found
        if col_name is None:
            # Do not change the colum name,
            # and add it to not-found column names list
            col_name = col
            colnames_not_found.append(col_name)
            colnames_not_found_i.append(i)
        # Append the list of column names
        colnames.append(col_name)

    # If there are column names that were not detected and user wants them
    # to be guessed
    if len(colnames_not_found) > 0 and guess_names:
        # Initialize list for new and old column names for warning message
        colnames_old = []
        colnames_new = []
        for i in colnames_not_found_i:
            col = df.columns[i]
            name = __guess_name(df=df,
                                col_i=i,
                                colnames=colnames,
                                fields=fields, **args)
            # if the column name was changed
            if col != name:
                # Change name
                colnames[i] = name
                # Append old and new column name list
                colnames_old.append(col)
                colnames_new.append(name)
        # If there are columns that were changed, give warning
        if len(colnames_new) > 0:
            warnings.warn(
                message=f"The following column names... \n {colnames_old}\n"
                f"... were replaced with \n {colnames_new}",
                category=UserWarning
                )
        # Update not-found column names
        colnames_not_found = [i for i in colnames_not_found
                              if i not in colnames_old]
    # Replace column names with new ones
    df.columns = colnames

    # Give warning if there were column names that were not identified
    if len(colnames_not_found) > 0:
        warnings.warn(
            message=f"The following column names were not detected. "
            f"Please check them for errors.\n {colnames_not_found}",
            category=UserWarning
            )

    # Check that the format of the values are correct
    df = __check_format_of_values(df, **args)

    # If there are duplicated column names and user want to make them unique
    if len(set(df.columns)) != df.shape[1] and make_unique:
        # Initialize a list for new column names
        colnames = []
        colnames_old = []
        colnames_new = []
        # Loop over column names
        for col in df.columns:
            # If there are already column that has same name
            if col in colnames:
                # Add old name to list
                colnames_old.append(col)
                # Add suffix to name
                col = col + "_" + str(colnames.count(col)+1)
                # Add new column name to list
                colnames_new.append(col)
            # Add column name to list
            colnames.append(col)
        # Give warning
        warnings.warn(
            message=f"The following duplicated column names... \n"
            f"{colnames_old}\n... were replaced with \n {colnames_new}",
            category=UserWarning
            )
        # Replace column names with new ones
        df.columns = colnames
    return df


# HELP FUNCTIONS


def __get_fields_df(fields, change_optional=True, **args):
    """
    Fetch dictionary that contains fields and create a dictionary from it.
    Input: A DataFrame or dictionary of fields or nothing.
    Output: A dictionary containing which column names are meaning the same
    """
    # INPUT CHECK
    # make_unique must be boolean
    if not isinstance(change_optional, bool):
        raise Exception(
            "'change_optional' must be bool."
            )
    # INPUT CHECK END
    # If fields was not provided, open files that include fields
    if fields is None:
        # Load data from /resources of package osta
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "fields_mandatory.csv")
        mandatory_fields = pd.read_csv(path
                                       ).set_index("key")["value"].to_dict()
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "fields_optional.csv")
        optional_fields = pd.read_csv(path
                                      ).set_index("key")["value"].to_dict()
        # Combine fields into one dictionary
        fields = {}
        fields.update(mandatory_fields)
        # If user wants also to update optinal fields
        if change_optional:
            fields.update(optional_fields)
        # Add field values as a key
        add_fields = pd.DataFrame(fields.values(), fields.values())
        add_fields = add_fields[0].to_dict()
        fields.update(add_fields)
    elif isinstance(fields, pd.DataFrame):
        # If fields does not include key and values
        if not all([i in fields.columns for i in ["key", "value"]]):
            raise Exception(
                "'fields' must include columns 'key' and 'value'."
                )
        # Convert DF to dict
        fields = fields.set_index("key")["value"].to_dict()
    elif isinstance(fields, str):
        # Read data based on path
        fields = pd.read_csv(fields, **args)
        # If fields does not include key and values
        if not all([i in fields.columns for i in ["key", "value"]]):
            raise Exception(
                "'fields' must include columns 'key' and 'value'."
                )
        # Convert DF to dict
        fields = fields.set_index("key")["value"].to_dict()
    # The search is case insensitive --> make keys lowercase
    # The key will be matched to value that is made lowercase
    fields = {k.lower(): v for k, v in fields.items()}
    return fields


def __guess_name(df, col_i, colnames, fields, pattern_th=0.9, match_th=0.8,
                 **args):
    """
    Guess column names based on pattern.
    Input: DataFrame, index of column being guesses,
    current column names, match
    between column names and standardized names.
    Output: A guessed column name
    """
    # INPUT CHECK
    # Types of all other arguments are fixed
    # pattern_th must be numeric value 0-1
    if not utils.__is_percentage(pattern_th):
        raise Exception(
            "'pattern_th' must be a number between 0-1."
            )
    # match_th must be numeric value 0-100
    if not utils.__is_percentage(match_th):
        raise Exception(
            "'match_th' must be a number between 0-1."
            )
    # INPUT CHECK END
    # Remove spaces from beginning and end of the values
    df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # Get the name of the column
    col = df.columns[col_i]

    # Try strict loose match (0.95) if pattern_th is smaller than 0.95
    pattern_th_strict = 0.95 if pattern_th <= 0.95 else pattern_th
    res = __test_if_loose_match(col=col, fields=fields,
                                pattern_th=pattern_th_strict, **args)
    # If there were match, column is renamed
    if res != col:
        col = res
    # Try if column is ID column (hard-coded since the column should contain
    # BIDs if at least one is found...)
    elif __test_if_BID(df=df, col_i=col_i, match_th=0.1):
        # BID can be from organization or supplier
        col = __org_or_suppl_BID(df=df, col_i=col_i, colnames=colnames,
                                 match_th=match_th)
    # Test if date
    elif utils.__test_if_date(df=df.iloc[:, col_i]):
        col = "doc_date"
    # Test if column includes suppl_land codes
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_land.csv",
                         test="suppl_land", match_th=match_th,
                         **args):
        col = "suppl_land"
    # Test if column includes VAT numbers
    elif __test_if_vat_number(df=df, col_i=col_i, colnames=colnames,
                              match_th=match_th):
        col = "suppl_vat_number"
    # Test if org_name
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_municipality.csv",
                         test="name", match_th=match_th,
                         cols_not_match=["suppl_name", "suppl_code"],
                         cols_to_match=["org_code", "org_bid"],
                         datatype=["object"],
                         **args):
        col = "org_name"
    # Test if service_code
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_service.csv",
                         test="code", match_th=match_th,
                         do_not_match=["account_code", "account_name"],
                         datatype=["int64"],
                         **args):
        col = "service_code"
    # Test if service_name
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_service.csv",
                         test="name", match_th=match_th,
                         do_not_match=["account_code", "account_name"],
                         datatype=["object"],
                         **args):
        col = "service_name"
    # Test if account_code
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_account.csv",
                         test="code", match_th=match_th,
                         do_not_match=["service_code", "service_name"],
                         datatype=["int64"],
                         **args):
        col = "account_code"
    # Test if account_name
    elif __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                         db_file="data_account.csv",
                         test="name", match_th=match_th,
                         do_not_match=["service_code", "service_name"],
                         datatype=["object"],
                         **args):
        col = "account_name"
    # # Test if org_code
    elif __test_match_between_colnames(df=df, col_i=col_i, colnames=colnames,
                                       cols_match=["org_name", "org_bid"],
                                       datatype=["int64"]
                                       ):
        col = "org_code"
    # Test if suppl_name
    elif __test_match_between_colnames(df=df, col_i=col_i, colnames=colnames,
                                       cols_match=["suppl_bid"],
                                       datatype=["object"]
                                       ):
        col = "suppl_name"
    # test if price_ex_vat
    elif __test_if_sums(df=df, col_i=col_i, colnames=colnames,
                        test_sum="price_ex_vat",
                        match_with=["price_total", "price_vat"],
                        datatype="float64"
                        ):
        col = "price_ex_vat"
    # test if total
    elif __test_if_sums(df=df, col_i=col_i, colnames=colnames,
                        test_sum="price_total",
                        match_with=["price_vat", "price_ex_vat"],
                        datatype="float64"
                        ):
        col = "price_total"
    # test if price_vat
    elif __test_if_sums(df=df, col_i=col_i, colnames=colnames,
                        test_sum="price_vat",
                        match_with=["price_total", "price_ex_vat"],
                        datatype="float64"
                        ):
        col = "price_vat"
    # Test if doc_id
    elif utils.__test_if_voucher(df=df, col_i=col_i, colnames=colnames):
        col = "doc_id"
    else:
        # Get match from partial matching
        col = __test_if_loose_match(col=col, fields=fields,
                                    pattern_th=pattern_th, **args)
    return col


def __test_if_loose_match(col, fields, pattern_th,
                          scorer=fuzz.token_sort_ratio,
                          **args):
    """
    Guess column names based on pattern on it.
    Input: Column name and names that are tried to be match with it
    Output: A guessed column name
    """
    # If column is not empty
    if col.strip():
        # Try partial match, get the most similar key value
        res = process.extract(col.strip(), fields.keys(), scorer=scorer)
        col_name_part = res[0]
        col_name_part2 = res[1]
        # Value [0,1] to a number between 0-100
        pattern_th = pattern_th*100
        # If the matching score is over threshold and second match is not close
        if col_name_part[1] >= pattern_th and (col_name_part[1] >
                                               col_name_part2[1]):
            # Get only the key name
            col_name_part = col_name_part[0]
            # Based on the key, get the value
            col = fields.get(col_name_part)
    return col


def __test_if_BID(df, col_i, match_th):
    """
    This function checks if the column defines BIDs (y-tunnus)
    Input: DataFrame, index of the column, found final column names
    Output: Boolean value
    """
    # Initialize result as False
    res = False
    # Test if pattern found
    patt_found = utils.__are_valid_bids(df.iloc[:, col_i])
    patt_found = patt_found.value_counts()/df.shape[0]
    # If Trues exist in both, get the smaller portion. Otherwise, True was not
    # found and the result is 0 / not found
    if True in patt_found.index:
        # Get portion of Trues and take only value
        patt_found = patt_found[patt_found.index][0]
    else:
        patt_found = 0
    # Check if over threshold
    if patt_found >= match_th:
        res = True
    return res


def __org_or_suppl_BID(df, col_i, colnames, match_th):
    """
    This function checks if the column defines BID of organization or supplier
    Input: DataFrame, index of the column, found final column names
    Output: The final colname of BID column
    """
    # If BID can be found from the database
    if __test_if_in_db(df=df, col_i=col_i, colnames=colnames,
                       db_file="data_municipality.csv",
                       test="bid", match_th=match_th):
        res = "org_bid"
    else:
        # Initialize result as supplier ID
        res = "suppl_bid"
        # List of columns that are matched
        cols_match = ["org_code", "org_name"]
        # Loop over columns that should be matched
        for col_match in cols_match:
            # If the column is in colnames
            if col_match in colnames:
                # Subset the data by taking only specified columns
                temp = df.iloc[:, [col_i, colnames.index(col_match)]]
                # Drop rows with blank values
                temp = temp.dropna()
                # Number of unique combinations
                n_uniq = temp.drop_duplicates().shape[0]
                # If there are as many combinations as there are
                # individual values these columns match
                if n_uniq == df.iloc[:, colnames.index(col_match)].nunique():
                    res = "org_bid"
        # If all the identifiers are missing, give "bid", because we
        # cannot be sure
        if all(list(name not in colnames for name in ["org_code", "org_name",
                                                      "org_bid", "suppl_name",
                                                      "suppl_bid"])):
            res = "bid"
        # If there are supplier IDs already, try if they are differemt
        if "suppl_bid" in colnames and all(df.iloc[:, col_i] !=
                                           df.iloc[:, colnames.index(
                                               "suppl_bid")]):
            res = "org_bid"
        # If there are organization IDs already, try if they are differemt
        if "org_bid" in colnames and all(df.iloc[:, col_i] ==
                                         df.iloc[:, colnames.index(
                                             "org_bid")]):
            res = "org_bid"
        # If there are not many unique values (less than 2%),
        # it might be organization ID
        if df.iloc[:, col_i].nunique()/df.shape[0] < 0.02:
            res = "org_bid"
    return res


def __test_match_between_colnames(df, col_i, colnames, cols_match, datatype):
    """
    This function checks if the column defines extra information of
    another column / if the column is related to that
    Input: DataFrame, index of the column, found final column names
    Output: Boolean value
    """
    # Initialize results as False
    res = False
    # Test the data type
    if df.dtypes[col_i] in datatype:
        # Loop over columns that should be matched
        for col_match in cols_match:
            # If the column is in colnames
            if col_match in colnames:
                # Subset the data by taking only specified columns
                temp = df.iloc[:, [col_i, colnames.index(col_match)]]
                # Drop rows with blank values
                temp = temp.dropna()
                # Number of unique combinations
                n_uniq = temp.drop_duplicates().shape[0]
                # If there are as many combinations as there are
                # individual values these columns match
                if (n_uniq == df.iloc[:, colnames.index(col_match)].nunique()
                    and n_uniq == df.iloc[
                        :, col_i].nunique()):
                    res = True
    return res


def __test_if_sums(df, col_i, colnames, test_sum, match_with, datatype):
    """
    This function checks if the column defines total, net, or VAT sum,
    the arguments defines what is searched
    Input: DataFrame, index of the column, found final column names
    Output: Boolean value
    """
    # Initialize results as False
    res = False
    # If all columns are available
    if all(mw in colnames for mw in match_with):
        # Take only specific columns
        ind = list(colnames.index(mw) for mw in match_with)
        ind.append(col_i)
        # Preserve the order of indices
        ind.sort()
        df = df.iloc[:, ind]
        # Drop empty rows
        df = df.dropna()
        # If the datatypes are correct
        if all(df.dtypes == datatype):
            # If VAT is tested and value is correct
            if test_sum == "price_vat" and\
                all(df.iloc[:, col_i] ==
                    df.iloc[:, colnames.index("price_total")] -
                    df.iloc[:, colnames.index("price_ex_vat")]):
                res = True
            # If total is tested and value is correct
            elif test_sum == "price_total" and\
                all(df.iloc[:, col_i] ==
                    df.iloc[:, colnames.index("price_ex_vat")] +
                    df.iloc[:, colnames.index("price_vat")]):
                res = True
            # If price_ex_vat is tested and value is correct
            elif test_sum == "price_ex_vat" and\
                all(df.iloc[:, col_i] ==
                    df.iloc[:, colnames.index("price_total")] -
                    df.iloc[:, colnames.index("price_vat")]):
                res = True
    return res


def __test_if_vat_number(df, col_i, colnames, match_th):
    """
    This function checks if the column defines VAT numbers
    Input: DataFrame, index of the column, found final column names
    Output: Boolean value
    """
    # Initialize result
    res = False
    # Get specific column and remove NaNs
    df = df.iloc[:, col_i]
    nrow = df.shape[0]
    df = df.dropna()
    # Check if values are VAT numbers
    res_patt = utils.__are_valid_vat_numbers(df)
    # How many times the pattern was found from values? If enough, then we
    # can be sure that the column includes VAT numbers
    if sum(res_patt)/nrow >= match_th:
        res = True
    return res


def __test_if_in_db(df, col_i, colnames, test, db_file, match_th,
                    datatype=None, cols_not_match=None, cols_to_match=None,
                    **args):
    """
    This function tests if the column includes account or service category info
    Input: DataFrame, index of the column, found final column names, account
    or service data type to search
    Output: Boolean value
    """
    # Initialize results as False
    res = False
    res2 = False
    res3 = False
    # Check that the column does not match with other specified columns
    if cols_not_match is not None:
        res2 = __test_match_between_colnames(df=df, col_i=col_i,
                                             colnames=colnames,
                                             cols_match=cols_not_match,
                                             datatype=datatype)
    # Check if other columns that specify same instance are found
    if cols_to_match is not None:
        if cols_to_match is not None:
            res3 = __test_match_between_colnames(df=df, col_i=col_i,
                                                 colnames=colnames,
                                                 cols_match=cols_to_match,
                                                 datatype=datatype)
    # Get specific column and remove NaNs
    df = df.iloc[:, col_i]
    df = df.dropna()
    df.drop_duplicates()
    # Does the column include integers
    res_list = df.astype(str).str.isdigit()
    if ((any(res_list) and test == "code") or (all(
            -res_list) and test != "code")):
        # Test if col values can be found from the table
        # Load codes from resources of package osta
        path = pkg_resources.resource_filename(
            "osta",
            "resources/" + db_file)
        db = pd.read_csv(path, index_col=0, dtype=str)
        # If countries, take whole data, otherwise get only specific column
        if test == "suppl_land":
            db = db.drop("code_num", axis=1)
        else:
            db = db[[test]]
        # Initialize a data frame
        df_res = pd.DataFrame()
        # Loop over columns of database
        for i, data in db.items():
            # Does the column include certain codes?
            temp = df.astype(str).str.lower().isin(
                data.astype(str).str.lower())
            df_res[i] = temp
        # How many times the value was found from the codes? If enough, then we
        # can be sure that the column includes land codes
        if df_res.shape[0] > 0 and \
            sum(df_res.sum(axis=1) > 0
                )/df_res.shape[0] >= match_th:
            res = True
    # Combine result
    if res2 is False and (res or res3):
        res = True
    else:
        res = False
    return res


def __check_format_of_values(df, match_th=0.8, **args):
    """
    This function tests if values of value-pairs
    (e.g., account name and number) are in correct format (numbers are int and
    names are str).
    Input: df
    Output: df with corrected column names
    """
    # INPUT CHECK
    # match_th must be numeric value 0-100
    if not utils.__is_percentage(match_th):
        raise Exception(
            "'match_th' must be a number between 0-1."
            )
    # INPUT CHECK END
    # Load variable pairs that will be matched
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_pairs.csv")
    df_var = pd.read_csv(path)
    # Create DF where all variables are in one column, their corresponding
    # variable in second column and type of variable 1 in third column
    df_num = pd.DataFrame({"var1": df_var["var_num"],
                           "var2": df_var["var_name"],
                           "type": ["int"] * df_var.shape[0]
                           })
    df_name = pd.DataFrame({"var1": df_var["var_name"],
                            "var2": df_var["var_num"],
                            "type": ["str"] * df_var.shape[0]
                            })
    df_var = pd.concat([df_num, df_name])
    df_var = df_var.reset_index(drop=True)
    # Loop over variable names
    colnames = df.columns.tolist()
    orig = []
    new = []
    for row_i, var in df_var.iterrows():
        # Get indices which tell what column is the variable if any
        ind = [i for i, x in enumerate(df.columns) if x == var["var1"]]
        # If the specified variable can be found from the column names
        if len(ind) > 0:
            # Loop over columns that are specified by the variable
            # (there might be duplicated column names, that is why for-loop)
            for i in ind:
                number_of_nums = sum(df.iloc[:, i].dropna().astype(
                    str).str.strip().str.isdigit())
                number_of_vals = len(df.iloc[:, i].dropna())
                prop_of_nums = number_of_nums/number_of_vals
                # If the variable must be integer or str and it is not
                if (var["type"] == "int" and
                    prop_of_nums < match_th) or (var["type"] == "str" and
                                                 1-prop_of_nums < match_th):
                    # Add to lists for warning message
                    orig.append(colnames[i])
                    new.append(var["var2"])
                    # Change the column name
                    colnames[i] = var["var2"]
    # Column names have been changed
    if len(orig) > 0:
        # Update column names
        df.columns = colnames
        # Give warning
        warnings.warn(
            message=f"Based on expected value types the following "
            f"column names... \n {orig}\n"
            f"... were replaced with \n {new}",
            category=UserWarning
            )
    return df

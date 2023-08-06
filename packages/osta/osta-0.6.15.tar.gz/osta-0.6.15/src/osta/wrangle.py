#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import osta.__utils as utils
import pandas as pd
import warnings
from os import listdir
from os.path import isfile, isdir, join
import sys
from osta.__utils_wrangle import clean_data


def clean(df_list, save_dir=None, log_file=False, verbose=True, **args):
    """
    Standardize data

    This function standardize the data that is in pandas.DataFrame. The
    function expects that columns are named in specific way. If the data
    does not meet requirements, the function gives a warning.

    Arguments:
        `df`: pandas.DataFrame containing invoice data or list of pd.DataFrames
        or paths to files.

        `**args`: Additional arguments passes into other functions:

        `date_format`: The format of date that will be in output data.
        (By default: date_format="%d-%m-%Y")

        `dayfirst`: Boolean value or None to specify the format of date
        in input data. 'If day comes before month in the date.'
        If None, function determines the format automatically.
        (By default: dayfirst=None)

        `yearfirst`: Boolean value or None to specify the format of date
        in input data. 'If year comes first in the date.'
        If None, function determines the format automatically.
        (By default: yearfirst=None)

        `country_format`: A string speciying the format of country in the
        output data. Must be one of the following options: 'name_fin',
        'name_en', "code_2char", 'code_3char', 'code_num', or 'code_iso'.
        (By default: country_format='code_2char')

        `pattern_th`: A numeric value [0,1] specifying the threshold of
        enough good match between names, e.g., 'org_name', and database.
        Value over threshold have enough strong pattern and it is
        interpreted to be a match. (By default: pattern_th=0.7)

        `scorer`: A scorer function passed into fuzzywuzzy.process.extractOne
        function that evaluates the match between names and database.
        (By default: scorer=fuzz.partial_ratio)

        `org_data`: pd.DataFrame or None. Database for organization data.
        Data must include on of the following columns: 'name', 'code', or
        'bid' specifying the name, code and business ID of organizations,
        respectively. If None, packages default database is used.
        (By default: org_data=None)

        `suppl_data`: pd.DataFrame or None. Database for supplier data.
        Data must include on of the following columns: 'name', 'code', or
        'bid' specifying the name, code and business ID of suppliers,
        respectively. If None, no database is used.
        (By default: org_data=None)

        `account_data`: pd.DataFrame or None. Database for account data.
        Data must include on of the following columns: 'name', or
        'code' specifying the name and number of accounts,
        respectively. If None, packages default database is used.
        (By default: account_data=None)

        `subset_account_data`: None or string to specify which database is
        used for account data. Available options are 'balance_sheet' and
        'income_statement'. If None, both databases are used and the result
        value will be the first occurence.
        (By default: subset_account_data=None)

        `service_data`: pd.DataFrame or None. Database for service data.
        Data must include on of the following columns: 'name', or
        'code' specifying the name and number of service categories,
        respectively. If None, packages default database is used.
        (By default: service_data=None)

        `db_year`: Integer value or None specifying the year (2021, 2021,
        or 2023) that will be used to match account and service data.
        If None, the most current information is used and duplicates from
        previous years are removed. (By default: db_year=None)

        `disable_*`: A boolean value specifying whether * data
        is checked. * can be one of the following options: 'org',
        'suppl', 'date', 'sums', 'country', 'voucher', 'account' or
        'service'. (By default: disable_*=False)

        `thresh`: An integer specifying the number of values each observation
        should contain to preserve it. Some datasets might have rows with
        additional information such as additional rows for price. These rows
        can be dropped by specifying thresh. For example, thresh=df.shape[0]-5
        removes all rows that have over 5 empty values. (By default: thresh=0)

        `check_na`: A boolean value specifying whether to notify if there are
        missing values in organization data. (By default: check_na=False)

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        Disabled when 'df' is a single pd.DataFrame. (By default: verbose=True)

    Details:
        This function standardize the data and checks that it is in correct
        format. If the data is not in expected format containing erroneous
        data that cannot be standardized, the function gives a warning.
        Moreover, empty rows and columns along with spaces before or after
        values are removed.

        The function expects that columns are in specific format.
        Not all the columns must be included in the data. Below is a
        list of columns and what type of data they should have.

        org_name: Organization name.

        org_code: Organization number.

        org_bid: Organization business ID.

        account_name: The name of account to where invoice is allocated.

        account_code: The number of account to where incoice is
        allocated.

        service_name: The name of service category to where invoice
        is allocated.

        service_code: The number of service category to where invoice is
        allocated.

        suppl_name: Supplier name.

        suppl_code: Supplier number.

        suppl_bid: Supplier business ID.

        suppl_vat_number: VAT number of supplier.

        suppl_land: Country of supplier.

        doc_id: Running identification of invoice.

        doc_date: Date of invoice.

        price_ex_vat: Price excluding VAT.

        price_vat: Amount of VAT.

        price_total: Price indluding VAT.

        Organization data (name, number, BID) is matched with database.
        Uncorrect values are replaced with correct values unless the
        specified organization matches with multiple organizations in the
        database. The user can also use own database.

        Supplier data (name, number, BID, VAT number) is not matched with
        database by default and replacements are not done. However, user
        can use own database. Like in case of organization data, the function
        checks that BID and VAT numbers are in correct format and that they
        duplicated meaning that each value specifies only one supplier.

        Account and service information. Account and service information is
        matched with database, and uncorrect values are replaced unless they
        match with multiple accounts / service categories. For account data,
        user can specify if balance sheet or income statement database is used.
        Otherwise, both are used and first occurence will be the result value.
        The user can also use own database.

        Country is identified with database containing all common land codes.
        (Finnish and English names, 2 and 3-character codes, along with
        numeric and ISO code). User can define the format of output from
        formats included in the database.

        Date is automatically identified unless user do not define the format.
        Dates are converted into format that user can specify.

        Price excluding and including VAT and VAT amount (abbreviated as sums
        in the function) are checked by calculating if values of them match
        between each other. If all three columns are not available, the
        the function only converts values in float type if possible.

    Examples:
        ```
        # Create a dummy data
        data = {"org_name": ["Turun kaupunki", "Turku", "Turku"],
                "org_code": [None, None, None],
                "doc_date": ["02.01.2023", "2-1-2023", "1.1.2023"],
                "suppl_name": ["Myyjä", "Supplier Oy", "Myyjän tuote Oy"],
                "suppl_land": ["FI", "FI", "FI"],
                "price_total": [100.21, 10.30, 50.50],
                }
        df = pd.DataFrame(data)
        df = clean_data(df, country_format="name_fin")
        ```

    Output:
        pandas.DataFrame with standardized data or list of pd.DataFrames.

    """
    # INPUT CHECK
    if not (isinstance(df_list, list) or isinstance(df_list, str) or
            isinstance(df_list, pd.DataFrame)):
        raise Exception(
            "'df_list' must be a list of pd.DataFrames, single pd.DataFrame " +
            "or paths to files."
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
        # Update the progress bar
        if verbose:
            percent = 100*((i+1)/len(df_list))
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
                dfs = utils.__detect_format_and_open_file(x, **args)
            except Exception:
                df_is_DF = False
                msg = x if isinstance(x, str) else ("element " + str(i))
                warnings.warn(
                    message="Failed to open the file.",
                    category=UserWarning
                    )
        else:
            dfs = x
        # If the file is DF and it was possible to load it
        if df_is_DF:
            # Convert to list if it is not already
            # (there can be excel file with multiple sheets)
            if not isinstance(dfs, list):
                dfs = [dfs]
            # Loop though individual DFs
            for df in dfs:
                # Change names from individual file
                df = clean_data(df, log_file=log_file, **args)
                # Save file if list contained paths or if specified
                if isinstance(x, str) or save_dir is not None:
                    # Get correct path
                    x = x if isinstance(x, str) else join(str(save_dir), x)
                    df.to_csv(x, index=False)
                # Append the result list
                res.append(df)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging()
    # If result contains only one element, give only it
    if len(res) == 1:
        res = res[0]
    return res


def merge(df_list, save_file=None, log_file=False, verbose=True, **args):
    """
    This function merges datasets into one.

    Arguments:
        `df_list`: A list of pandas.DataFrames or paths to files.

        `save_file`: None or a single character value specifying a file path
        where result will be stored. When None, result is not stored to file.
        (By default: save_file=None)

        `log_file`: A boolean value or a single character value for specifying
        where log file will be stored. If True, all the messages are stored to
        a log file that can be found from osta direcotry that is located
        in devices default temporary directory. When False, messages are
        printed to screen and log file is not created.
        (By default: log_file=False)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function can be used to merge multiple datasets into one.
        In detail, the function utilies pd.concat function to merge the data.
        The value of the function comes from the functionality that allows
        user to specify just a directory containing input data, and function
        automatically reads the data and merges individual datasets into one.

    Examples:
        ```
        combine_data("path/to/the/file.csv")

        ```

    Output:
        A pandas.DataFrame

    """
    # INPUT CHECK
    if not (isinstance(df_list, list) or isinstance(df_list, str)):
        raise Exception(
            "'df_list' must be a list of pd.DataFrames or paths to files."
            )
    if not (isinstance(save_file, str) or save_file is None):
        raise Exception(
            "'save_file' must be None or string specifying directory to ",
            "where result files will be stored."
            )
    if not (isinstance(log_file, str) or isinstance(log_file, bool)):
        raise Exception(
            "'log_file' must be a boolean value or a string specifying a path."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
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
    # INPUT CHECK END
    # If user wants to create a logger file
    if log_file:
        # Create a logger with file
        logger = utils.__start_logging(__name__, log_file)

    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop over list elements
    dfs = []
    for i, x in enumerate(df_list):
        # Update the progress bar
        if verbose:
            percent = 100*((i+1)/len(df_list))
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(
                                 percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Check if it is pd.DataFrame. Otherwise try to load it as a local file
        if not isinstance(x, pd.DataFrame):
            # Try to load it
            try:
                df = utils.__detect_format_and_open_file(x, **args)
            except Exception:
                msg = x if isinstance(x, str) else ("element " + str(i))
                warnings.warn(
                    message=f"Failed to open the file {msg}.",
                    category=UserWarning
                    )
        else:
            df = x
        # Convert to list if it is not already
        # (there can be excel file with multiple sheets)
        if not isinstance(df, list):
            df = [df]
        # Add to list
        dfs.extend(df)
    # Combine data to one DF
    df = pd.concat(dfs, ignore_index=True)
    # Check if there are duplicated values
    df = utils.__check_duplicated(df, log_file=log_file, **args)
    # Reset index
    df = df.reset_index(drop=True)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Save file if specified
    if save_file is not None:
        df.to_csv(save_file, index=False)
    # Reset logging; do not capture warnings anymore
    if log_file:
        utils.__stop_logging(logger)
    return df

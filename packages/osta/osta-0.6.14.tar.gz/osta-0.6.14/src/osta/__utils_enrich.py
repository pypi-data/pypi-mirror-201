#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import warnings
import pkg_resources
import requests
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as firefox_opt
from selenium.webdriver.chrome.options import Options as chrome_opt
from selenium.webdriver.ie.options import Options as ie_opt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile
import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import osta.__utils as utils


# THIS FILE INCLUDES HELPER FUNCTIONS FOR FOLLOWING METHODS:
# enrich, getMuni, getMuniFin, getMuniComp, getComp, getMap


# enrich

def __add_org_data(df, disable_org=False, org_data=None, **args):
    """
    This function adds organization data to dataset.
    Input: df (and dataset to be added)
    Output: enriched df
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(org_data) or org_data is None):
        raise Exception(
            "'org_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_org, bool):
        raise Exception(
            "'disable_org' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["org_bid", "org_vat_number", "org_code", "org_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_org or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Load default database
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_municipality.csv")
    org_data_def = pd.read_csv(path, index_col=0, dtype=str)
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["bid", "vat_number", "code", "name"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Add data from default database
    df = __add_data_from_db(df=df, df_db=org_data_def,
                            cols_to_check=cols_to_check,
                            cols_to_match=cols_to_match,
                            prefix="org")
    # If user has specified database, add it
    if org_data is not None:
        # Get columns that are added and matched
        cols_df = ["org_bid", "org_vat_number", "org_code", "org_name"]
        cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
        cols_to_match = ["bid", "vat_number", "code", "name"]
        cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                         if x in cols_to_check]
        # Add data
        df = __add_data_from_db(df=df, df_db=org_data,
                                cols_to_check=cols_to_check,
                                cols_to_match=cols_to_match,
                                prefix="org")
    return df


def __add_account_data(
        df, disable_account=False, account_data=None, subset_account_data=None,
        db_year=None, **args):
    """
    This function adds account data to dataset.
    Input: df (and dataset to be added)
    Output: enriched df
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(account_data) or account_data is None):
        raise Exception(
            "'account_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_account, bool):
        raise Exception(
            "'disable_account' must be True or False."
            )
    if not (subset_account_data in ["tase", "tuloslaskelma"] or
            subset_account_data is None):
        raise Exception(
            "'subset_account_data' must be 'tase' or 'tuloslaskelma'."
            )
    if not (db_year is None or isinstance(db_year, str) or
            isinstance(db_year, int) or isinstance(db_year, pd.Series)):
        raise Exception(
            "'db_year' must be None, string or integer specifying a year."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["account_code", "account_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_account or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Load default database
    subset_based_on_year = True
    if account_data is None:
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_account.csv")
        account_data = pd.read_csv(path, index_col=0)
        # Subset by taking only specific years
        if db_year is not None:
            account_data = utils.__subset_data_based_on_year(
                df, df_db=account_data, db_year=db_year, **args)
            subset_based_on_year = False
        # If user specified balance sheet or income statement,
        # get only specified accounts
        if subset_account_data is not None:
            account_data = account_data.loc[
                :, account_data["cat_1"] == subset_account_data]
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["code", "name"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Test if year can be fetched based on the data
    year = None
    if "doc_date" in df.columns and \
        "year" in account_data.columns and \
            subset_based_on_year:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                date = df["doc_date"].astype(str)
                year = pd.to_datetime(date).dt.year
        except Exception:
            pass
    # If the year was found, check data based on years
    year_not_found = []
    if year is not None:
        for y in year.drop_duplicates():
            temp_df = df.loc[year == y, :]
            temp_account = account_data.loc[account_data["year"] == y, :]
            # If year was found from the database
            if temp_account.shape[0] > 0:
                # Add data from database
                temp_df = __add_data_from_db(
                    df=temp_df, df_db=temp_account,
                    cols_to_check=cols_to_check,
                    cols_to_match=cols_to_match,
                    prefix="account")
                # Add data back
                df.loc[year == y, :] = temp_df
            else:
                year_not_found.append(y)
    else:
        # Add data without year information
        df = __add_data_from_db(
            df=df, df_db=account_data,
            cols_to_check=cols_to_check,
            cols_to_match=cols_to_match,
            prefix="account")
    # Give warning if year was not found
    if len(year_not_found) > 0:
        warnings.warn(
            message=f"'The following years were not found from the account "
            f"data and data from the years is not added: {year_not_found}",
            category=Warning
            )
    return df


def __add_service_data(
        df, disable_service=False, service_data=None, db_year=None, **args):
    """
    This function adds service data to dataset.
    Input: df (and dataset to be added)
    Output: enriched df
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(service_data) or service_data is None):
        raise Exception(
            "'org_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_service, bool):
        raise Exception(
            "'disable_service' must be True or False."
            )
    if not (db_year is None or isinstance(db_year, str) or
            isinstance(db_year, int) or isinstance(db_year, pd.Series)):
        raise Exception(
            "'db_year' must be None, string or integer specifying a year."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["service_code", "service_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_service or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Load default database
    subset_based_on_year = True
    if service_data is None:
        path = pkg_resources.resource_filename(
            "osta", "resources/" + "data_service.csv")
        service_data = pd.read_csv(path, index_col=0)
        # Subset by taking only specific years
        if db_year is not None:
            service_data = utils.__subset_data_based_on_year(
                df, df_db=service_data, db_year=db_year, **args)
            subset_based_on_year = False
    # Column of db that are matched with columns that are being checked
    # Subset to match with cols_to_check
    cols_to_match = ["code", "name"]
    cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                     if x in cols_to_check]
    # Test if year can be fetched based on the data
    year = None
    if "doc_date" in df.columns and "year" in \
        service_data.columns and \
            subset_based_on_year:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                date = df["doc_date"].astype(str)
                year = pd.to_datetime(date).dt.year
        except Exception:
            pass
    # If the year was found, check data based on years
    year_not_found = []
    if year is not None:
        for y in year.drop_duplicates():
            temp_df = df.loc[year == y, :]
            temp_service = service_data.loc[service_data["year"] == y, :]
            # If year was found from the database
            if temp_service.shape[0] > 0:
                # Add data from database
                temp_df = __add_data_from_db(
                    df=temp_df, df_db=temp_service,
                    cols_to_check=cols_to_check,
                    cols_to_match=cols_to_match,
                    prefix="service")
                # Add data back
                df.loc[year == y, :] = temp_df
            else:
                year_not_found.append(y)
    else:
        # Add data without year information
        df = __add_data_from_db(
            df=df, df_db=service_data,
            cols_to_check=cols_to_check,
            cols_to_match=cols_to_match,
            prefix="service")
    # Give warning if year was not found
    if len(year_not_found) > 0:
        warnings.warn(
            message=f"'The following years were not found from the service "
            f"data and data from the years is not added: {year_not_found}",
            category=Warning
            )
    return df


def __add_suppl_data(df, disable_suppl=False, suppl_data=None, **args):
    """
    This function adds supplier data to dataset.
    Input: df and dataset to be added
    Output: enriched df
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_df(suppl_data) or suppl_data is None):
        raise Exception(
            "'org_data' must be non-empty pandas.DataFrame or None."
            )
    if not isinstance(disable_suppl, bool):
        raise Exception(
            "'disable_suppl' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["suppl_bid", "suppl_vat_number", "suppl_code", "suppl_name"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_suppl or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    if suppl_data is not None:
        # Column of db that are matched with columns that are being checked
        # Subset to match with cols_to_check
        cols_to_match = ["bid", "vat_number", "code", "name", "land"]
        cols_to_match = [cols_to_match[i] for i, x in enumerate(cols_df)
                         if x in cols_to_check]
        # Add data from database
        df = __add_data_from_db(df=df, df_db=suppl_data,
                                cols_to_check=cols_to_check,
                                cols_to_match=cols_to_match,
                                prefix="suppl")
    return df


def __add_data_from_db(df, df_db, cols_to_check, cols_to_match, prefix):
    """
    This function is a general function for adding data from a file
    to dataset.
    Input: df and dataset to be added
    Output: enriched df
    """
    # Which column are found from df and df_db SIIRRÄ UTILSIIN
    cols_df = [x for x in cols_to_check if x in df.columns]
    cols_df_db = [x for x in cols_to_match if x in df_db.columns]
    # Drop those columns that do not have match in other df
    if len(cols_df) > len(cols_df_db):
        cols_to_check = [cols_df[cols_to_match.index(x)] for x in cols_df_db]
        cols_to_match = cols_df_db
    else:
        cols_to_match = [cols_df_db[cols_to_check.index(x)] for x in cols_df]
        cols_to_check = cols_df
    # If identification coluns were not found
    if len(cols_to_check) == 0 or len(cols_to_match) == 0:
        warnings.warn(
            message=f"'{prefix}_data' should include at least one of the "
            "following columns: 'name' (name), 'code' "
            "(number), and 'bid' (business ID for organization and "
            f"supplier data).",
            category=Warning
            )
        return df
    # Get columns that will be added to data/that are not yet included
    cols_to_add = [x for x in df_db.columns if x not in cols_to_match]
    # Get only the first variable
    col_to_check = cols_to_check[0]
    col_to_match = cols_to_match[0]
    # If there are columns to add
    if len(cols_to_add) > 0:
        # Remove duplicates if database contains multiple values
        # for certain information.
        df_db = df_db.drop_duplicates(subset=col_to_match)
        # Create temporary columns which are used to merge data
        temp_x = df.loc[:, col_to_check]
        temp_y = df_db.loc[:, col_to_match]
        # Subset database and add prefix tp column names
        df_db = df_db.loc[:, cols_to_add]
        df_db.columns = prefix + "_" + df_db.columns
        # If variables can be converted into numeric, do so.
        # Otherwise convert to object if datatypes are not equal
        if (all(temp_x.dropna().astype(str).str.isnumeric()) and all(
                temp_y.dropna().astype(str).str.isnumeric())):
            temp_x = pd.to_numeric(temp_x)
            temp_y = pd.to_numeric(temp_y)
        elif temp_x.dtype != temp_y.dtype:
            temp_x = temp_x.astype(str)
            temp_y = temp_y.astype(str)
        # Add temporary columns to data
        df.loc[:, "temporary_X"] = temp_x
        df_db.loc[:, "temporary_Y"] = temp_y
        # Merge data
        df = pd.merge(df, df_db, how="left",
                      left_on="temporary_X", right_on="temporary_Y")
        # Remove temproary columns
        df = df.drop(columns=["temporary_X", "temporary_Y"])
    return df


def __add_sums(df, disable_sums=False, **args):
    """
    This function adds sums (price_total, price_vat or price_ex_vat) if
    some is missing.
    Input: df
    Output: enriched df
    """
    # INPUT CHECK
    if not isinstance(disable_sums, bool):
        raise Exception(
            "'disable_sums' must be True or False."
            )
    # Check if column(s) is found as non-duplicated
    cols_df = ["price_total", "price_vat", "price_ex_vat"]
    cols_to_check = utils.__not_duplicated_columns_found(df, cols_df)
    if disable_sums or len(cols_to_check) == 0:
        return df
    # INPUT CHECK END
    # Get columns that are missing from the data
    col_missing = [x for x in cols_df if x not in cols_to_check]

    # If there were only one column missing, calculate them
    if len(col_missing) == 1 and all(
            x in ["float64", "int64"] for x in df.loc[
                :, cols_to_check].dtypes):
        # If price_total is missing
        if "price_total" in col_missing:
            df["price_total"] = df["price_ex_vat"] + df["price_vat"]
        # If price_ex_vat is missing
        elif "price_ex_vat" in col_missing:
            df["price_ex_vat"] = df["price_total"] - df["price_vat"]
        # If price_vat is missing
        elif "price_vat" in col_missing:
            df["price_vat"] = df["price_total"] - df["price_ex_vat"]
    return df


# getComp

def __search_website(search_website=False, **args):
    """
    This function is for enabling search from PRH website. Must not be used!
    Input: boolean value if any
    Output: boolean value
    """
    # INPUT CHECK
    if not isinstance(search_website, bool):
        raise Exception(
            "'search_website' must be True or False."
            )
    # INPUT CHECK END
    if search_website:
        warnings.warn(
            message=("You have enabled search from YTJ website. However, " +
                     "it is strictly prohibited. See more information from " +
                     "\nhttps://www.ytj.fi/en/index/companysearch/" +
                     "rules_for_bis_company_search.html"),
            category=Warning
            )
    return search_website


def __fetch_company_based_on_bid(
        bid, name, lan, language, search_website, **args):
    path = "https://avoindata.prh.fi/bis/v1/" + str(bid)
    r = requests.get(path)
    # Convert to dictionaries
    text = r.json()
    # Get results only
    df_temp = pd.json_normalize(text["results"])
    # If results were found, continue
    if not df_temp.empty:
        # Add search_word to df
        df_temp["search_word"] = bid
        # Change names
        df_temp = df_temp.rename(columns={
            "businessId": "bid",
            "name": "name",
            "registrationDate": "registration_date",
            "companyForm": "company_form_short",
            "liquidations": "liquidation",
            "companyForms": "company_form",
            "businessLines": "business_line",
            "registedOffices": "muni",
            "businessIdChanges": "old_bid",
            })
        # Get certain data and convert into Series
        col_info = ["search_word", "bid", "name"]
        series = df_temp.loc[:, col_info]
        series = series.squeeze()
        # Loop over certain information columns
        info = [
            "liquidation",
            "company_form",
            "business_line",
            "muni",
            "old_bid",
                ]
        for col in info:
            # Get data
            temp = df_temp[col]
            temp = temp.explode().apply(pd.Series)
            # If information is included
            if len(temp.dropna(axis=0, how="all")) > 0:
                if any(x in col for x in ["company_form",
                                          "business_line",
                                          "muni"]):
                    # If certain data, capitalize and add column names
                    # with language
                    # Remove those values that are outdated
                    ind = temp["endDate"].isna()
                    if any(ind):
                        temp = temp.loc[ind, :]
                    # Get only specific language
                    ind = temp["language"].astype(str).str.lower() == lan
                    if any(ind):
                        temp_name = temp.loc[ind, "name"].astype(
                            str).str.capitalize()
                    else:
                        temp_name = temp.loc[:, "name"].astype(
                            str).str.capitalize()
                    # Ensure that there is only one value
                    temp_name = temp_name.iloc[[0]]
                    temp_name.index = [col]
                elif any(x in col for x in ["liquidation"]):
                    # If certain data, get name and date with
                    # specific language
                    ind = temp["language"].astype(str).str.lower() == lan
                    if any(ind):
                        temp_name = temp.loc[ind, "description"].astype(
                            str).str.capitalize()
                        temp_date = temp.loc[ind, "registrationDate"]
                    else:
                        temp_name = temp.loc[:, "description"].astype(
                            str).str.capitalize()
                        temp_date = temp.loc[:, "registrationDate"]
                    # Ensure that there is only one value
                    temp_name = temp_name.iloc[[0]]
                    temp_date = temp_date.iloc[[0]]
                    # Add names
                    temp_name.index = [col]
                    temp_date.index = [col + "_date"]
                    # Combine results
                    temp_name = pd.concat([temp_name, temp_date])
                elif any(x in col for x in ["old_bid"]):
                    # If certain data, capitalize and add
                    # column names with numbers
                    temp_name = temp["oldBusinessId"]
                    temp_col = [col]
                    if len(temp_name) > 1:
                        temp_col.extend([col + "_" + str(x) for x in
                                         range(2, len(temp_name)+1)])
                    temp_name.index = temp_col
                # Add to final data
                series = pd.concat([series, temp_name])
        # Convert Series to DF and transpose it to correct format
        res = pd.DataFrame(series).transpose()
    elif search_website:
        # If BID was not found from the database, try to find
        # with web search
        try:
            # Try to find based on BID
            res = __fetch_company_data_from_website(bid, language, **args)
            # Add search_word to df
            res["search_word"] = bid
        except Exception:
            if name is not None:
                try:
                    # Try to find data based on name
                    res = __fetch_company_data_from_website(
                        name, language, **args)  # type: ignore
                    # Add search_word to df
                    res["search_word"] = name
                except Exception:
                    res = pd.DataFrame(
                        [bid], index=["search_word"]).transpose()
            else:
                res = pd.DataFrame([bid], index=["search_word"]).transpose()
    else:
        # If user want only ltd info and data was not found
        res = pd.DataFrame([bid], index=["search_word"]).transpose()
    return res


def __get_driver():
    """
    Get selenium driver/browser.
    Input: -
    Output: driver
    """
    # Create a driver
    for browser in ["firefox", "chrome", "ie"]:
        # Try to use if these browsers are available
        try:
            if browser == "firefox":
                options_ff = firefox_opt()
                options_ff.add_argument("--headless")
                # Ignore errors of mypy (if certain browser is not installed
                # it gives error related to expression vs variable type
                # missmatch)
                driver = webdriver.Firefox(
                    options=options_ff)  # type: ignore
            elif browser == "chrome":
                options_ch = chrome_opt()
                options_ch.add_argument("--headless")
                # Ignore errors of mypy
                driver = webdriver.Chrome(
                    options=options_ch)  # type: ignore
            elif browser == "ie":
                options_ie = ie_opt()
                options_ie.add_argument("--headless")
                # Ignore errors of mypy
                driver = webdriver.Ie(
                    options=options_ie)  # type: ignore
            # Set implicit wait time
            driver.implicitly_wait(5)
        except Exception:
            driver = None
            pass
        else:
            break
    return driver


def __fetch_company_data_from_website(bid, language, browser=None, **args):
    """
    This function fetch company data from PRH's website that includes
    all companies (not just limited company).
    Input: business ID or business name
    Output: df with company data
    """
    # Test if BID is business ID or name
    bid_option = utils.__are_valid_bids(pd.Series([bid])).all()
    # Get driver if not provided
    quit_driver = False
    if browser is None:
        browser = __get_driver()
        quit_driver = True
    # IF driver was found
    if browser is not None:
        # Get url
        url = "https://tietopalvelu.ytj.fi/"
        # Go to the web page
        browser.get(url)

        # Wait until specific element is available
        Wait = WebDriverWait(browser, 5)
        Wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@name='businessIdOrLEI']")))
        # Get language buttons
        button = browser.find_elements(
            "xpath", "//button[@class='btn btn-link false undefined']")
        # What buttons should be found
        find = "Suomeksi" if language == "fi" else "svenska" \
            if language == "sv" else "English"
        # If language button is found, press it. Otherwise the language is
        # already correct.
        ind = [i for i, x in enumerate(button) if
               re.search(find, x.get_attribute("innerHTML"), re.IGNORECASE)]
        if len(ind) == 1:
            # Click the button
            button[ind[0]].click()

        # Get results
        res = __search_companies_with_web_search(
            bid, bid_option, url, browser, language, **args)
        # Shut down driver if it was fired in this function
        if quit_driver:
            browser.quit()
    else:
        # If driver was not found
        res = [bid, None] if bid_option else [None, bid]
        res.extend([None for x in range(1, 13)])
    # Names of fields
    colnames = [
        "bid",
        "name",
        "company_form",
        "muni",
        "business_line",
        "liquidation",
        ]
    # Create series
    df = pd.DataFrame(res, index=colnames).transpose()
    # Remove Nones
    df = df.dropna(axis=1)
    return df


def __search_companies_with_web_search(
        bid, bid_option, url, browser, language, muni_name=False,
        **args):
    """
    Help function, this function fetch company data from PRH's website. Search
    is similar for different languages
    Input: business ID, url and driver
    Output: list including company data
    """
    # INPUT CHECK
    if not isinstance(muni_name, bool):
        raise Exception(
            "'muni_name' must be True or False."
            )
    # INPUT CHECK END
    # Go to the web page
    browser.get(url)
    # If search municipalities, add specification to search
    if muni_name:
        search_box = browser.find_element(
            "xpath", "//input[@role='combobox']")
        company_type = ("Kunta" if language == "fi" else "Kommun"
                        if language == "sv" else "Municipality")
        search_box.send_keys(company_type)
    # Search by BID or name
    if bid_option:
        search_box = browser.find_element(
            "xpath", "//input[@name='businessIdOrLEI']")
    else:
        search_box = browser.find_element(
            "xpath", "//input[@name='companyName']")
    # If municipality search, search only with first letters,
    # otherwise search with whole name.
    if muni_name:
        __search_municipalities(browser, search_box, bid)
    else:
        search_box.send_keys(bid)
        # Submit the text to search bar
        search_box.send_keys(Keys.RETURN)
    # If the search was made with name, the site does not direct automatically
    # to the result page like when the search was made with BID.
    if not bid_option:
        # Find the link for result web page (get first result)
        link = browser.find_elements("xpath", "//a[@class='link']")
        link = link[0].get_attribute("href")
        # For municipality name search, get all the partly matched names and
        # get correct one from the result table
        if link is not None and muni_name:
            link = __get_link_for_muni(browser, bid, language)
        # Go to the result web page
        if link is not None:
            # Go to the page
            browser.get(link)
    else:
        link = "found"
    # Scrape the data from the result page
    if link is not None:
        # Wait until the table is visible
        element = browser.find_elements(
            "xpath",
            "//table[@class='table table-sm table-stacked-md \
                company-details-table']")
        if len(element) > 0:
            pass
        # Get the table
        table = pd.read_html(browser.page_source)[0]
        table = table.dropna().reset_index(drop=True)
        table.index = table.iloc[:, 0]
        table = table.drop(columns=table.columns[0])
        # GEt fields based on language
        if language == "fi":
            fields = [
                "Y-tunnus", "Konkurssi", "Toiminimi", "Yritysmuoto",
                "Kotipaikka", "Päätoimiala", "LEI-tunnus"]
        elif language == "sv":
            fields = [
                "FO-nummer", "Konkurs", "Firma", "Företagsform",
                "Hemkommun", "Huvudsaklig bransch", "LEI-nummer"]
        else:
            fields = [
                "Business ID", "Bankruptcy", "Company name", "Company form",
                "Home municipality!", "Main line of business", "LEI code"]
        # Initialize result table and add data from the fetched table
        res_table = pd.DataFrame({"field": fields})
        res_table = res_table.merge(
            table, left_on="field", right_index=True, how="left"
            ).iloc[:, [0, 1]]
        # Find business ID
        bid = res_table.iloc[0, 1]
        # Find liquidation information
        liquidation = res_table.iloc[1, 1]
        # Find name
        name = res_table.iloc[2, 1]
        # Find company form
        company_form = res_table.iloc[3, 1]
        # Find home town
        registed_office = res_table.iloc[4, 1]
        # Find business line
        business_line = res_table.iloc[5, 1]
        # Combine result
        res = [bid, name, company_form, registed_office,
               business_line, liquidation]
    else:
        # Give list with Nones, if link to result page is not found
        res = [bid, None] if bid_option else [None, bid]
        res.extend([None for x in range(1, 5)])
    return res


def __search_municipalities(browser, search_box, bid):
    """
    Add partial names of municipalities to search box.

    Input: driver, search box element, name
    Output: None
    """
    # Try to search only with first 2 letters of name
    # Some municipalities are with Swedish names --> database search does
    # not find them. Try to search all results with minimum letters -->
    # try partial match with later step.
    try:
        search_box.send_keys(bid[:2])
        search_box.send_keys(Keys.RETURN)
    except Exception:
        search_box = browser.find_element(
            "xpath", "//input[@id='_ctl0_cphSisalto_hakusana']")
        search_box.clear()
        search_box.send_keys(bid[:3])
        search_box.send_keys(Keys.RETURN)
    return None


def __get_link_for_muni(browser, name, language):
    """
    This scrapes link for municipality data based on partial matching.

    Input: driver, name
    Output: url
    """
    # Load all search result by pressing button
    # Wait until specific element is available
    Wait = WebDriverWait(browser, 5)
    Wait.until(EC.presence_of_element_located((
        By.XPATH, "//button[@class='page-link btn-secondary']")))
    button = browser.find_elements(
        "xpath", "//button[@class='page-link btn-secondary']")
    # What buttons should be found
    find = "kaikki" if language == "fi" else "alla" \
        if language == "sv" else "all"
    # If language button is found, press it. Otherwise the language is
    # already correct.
    ind = [i for i, x in enumerate(button) if
           re.search(find, x.get_attribute("innerHTML"), re.IGNORECASE)]
    if len(ind) == 1:
        # Click the button
        button[ind[0]].click()
    # Wait until the table is visible
    element = browser.find_elements(
        "xpath", "//table[@class='table table-hover table-stacked-md']")
    if len(element) > 0:
        pass
    # Get table from page
    link_df = pd.read_html(browser.page_source)[0]
    # Polish dataframe since results contain column names in front of the value
    for x in link_df.columns:
        link_df.loc[:, x] = link_df.loc[:, x].astype(str).str[len(x):]
    # Get links
    elements = browser.find_elements("xpath", "//a[@class='link']")
    url = [x.get_attribute("href") for x in elements
           if re.search("https", str(x.get_attribute("href"))) and
           link_df.iloc[:, 0].isin([elements[0].get_attribute(
               "innerHTML")]).any()]
    link_df["url"] = url

    # Remove those results that do not have name (inpossible to match name)
    link_df = link_df.loc[link_df.iloc[:, 1].notna(), :]
    # Try partial match
    res = process.extract(name, link_df.iloc[:, 1], scorer=fuzz.partial_ratio)
    name_part = res[0]
    name_part2 = res[1] if len(res) > 1 else None
    # If there are multiple values that include same partial string
    # e.g. karvia and merikarvia, they both have equal good match.
    # Try other partial match approach
    if name_part2 is not None and name_part[1] == name_part2[1]:
        res = process.extract(
            name, link_df.iloc[:, 1], scorer=fuzz.token_set_ratio)
        name_part = res[0]
        name_part2 = res[1] if len(res) > 1 else None
        # If the best match was not found, return None
        if name_part2 is not None and name_part[1] == name_part2[1]:
            name_part = None
            return None
    # If the match was found
    if name_part is not None:
        # Get the index
        link = link_df.loc[link_df.iloc[:, 1] == name_part[0], "url"].values[0]
    else:
        link = None
    return link


# getMuniFin


def __search_fin_from_stats(df_org, subset):
    """
    This function search financial data from Statisctics Finland
    Input: df indlucinf year and BID
    Output: df including financial data
    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_municipality.csv")
    org_data = pd.read_csv(path, index_col=0, dtype="object")
    # Add code
    df_org = df_org.merge(
        org_data[["code", "bid"]], left_on="bid", right_on="bid", how="left")
    # Initialize result DF
    res = pd.DataFrame()
    for year in df_org["year"].unique():
        # Get correct address based on year
        if year == "2020" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/006_kta_11_2020.px"
        elif year == "2020" and subset:
            suffix = "9._Tunnusluvut/006_kta_19_2020.px"
        elif year == "2019" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/007_kta_11_2019.px"
        elif year == "2019" and subset:
            suffix = "9._Tunnusluvut/007_kta_19_2019.px"
        elif year == "2018" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/008_kta_11_2018.px"
        elif year == "2018" and subset:
            suffix = "9._Tunnusluvut/008_kta_19_2018.px"
        elif year == "2017" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/009_kta_11_2017.px"
        elif year == "2017" and subset:
            suffix = "9._Tunnusluvut/009_kta_19_2017.px"
        elif year == "2016" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/010_kta_11_2016.px"
        elif year == "2016" and subset:
            suffix = "9._Tunnusluvut/010_kta_19_2016.px"
        elif year == "2015" and not subset:
            suffix = "1._Ulkoiset_tilinpaatoslaskelmat/011_kta_11_2015.px"
        elif year == "2015" and subset:
            suffix = "9._Tunnusluvut/011_kta_19_2015.px"
        url = ("https://pxdata.stat.fi/PXWeb/api/v1/fi/Kuntien_talous_" +
               "ja_toiminta/kunnat/")
        url = url + suffix
        # Get results
        params = {
          "query": [],
          "response": {
            "format": "json-stat2"
          }
        }
        r = requests.post(url, json=params)
        text = r.json()
        # Get municipality and labels
        code = pd.DataFrame(text.get("dimension").get("Alue").get("category"))
        if subset:
            label = pd.DataFrame(text.get("dimension").get("Tunnusluku").get(
                "category"))
        else:
            label = pd.DataFrame(text.get("dimension").get(
                "Tilinpäätöserä").get("category"))
        code = code.index.tolist()
        label = label["label"].tolist()
        # Get values
        values = text.get("value")
        # Divide values based on mucipalities / from long format to wide format
        values_num = int(len(values)/len(code))
        df_temp = pd.DataFrame()
        for i in range(0, len(values), values_num):
            # Split based on organization
            temp = pd.Series(values[i:i+values_num])
            temp = pd.DataFrame(temp).transpose()
            df_temp = pd.concat([df_temp, temp], axis=0)
        # Add label, municipality and year
        df_temp.columns = label
        df_temp["code"] = code
        df_temp["year"] = year
        # Add to results
        res = pd.concat([res, df_temp], axis=0)
    # Subset the data sp that it includes only wanted codes and years
    res = res.loc[res["code"].isin(
        df_org["code"]) & res["year"].isin(df_org["year"])]
    # Add bid
    res = res.merge(
        org_data[["code", "bid"]], left_on="code", right_on="code", how="left")
    # Drop code column
    res = res.drop(columns="code")
    # Drop empty columns
    res = res.dropna(axis=1, how="all")
    return res


def __fetch_org_financial_data_help(org_bid, year, subset, language, **args):
    """
    Fetch financial data of municipalities (KKNR, KKTR, KKOTR).

    Input: business ID of municipality, year,
    whether to take only certain values
    Output: pd.DataFrame including financial data.
    """
    ready_col = "hyvaksymisvaihe"
    # Get the information on database, what data it includes?
    url = ("https://prodkuntarest.westeurope.cloudapp.azure.com/" +
           "rest/v1/json/aineistot")
    r = requests.get(url)
    r.status_code
    text = r.json()
    text = text.get("aineistot")
    df_info = pd.DataFrame(text)
    # Subset by taking only specific city
    df_info = df_info.loc[df_info["ytunnus"] == org_bid, :]
    # Sort data based on the readiness of the data
    order = ["Lopullinen", "Hyväksytty", "Alustava"]
    df_info[ready_col] = pd.Categorical(
        df_info[ready_col], categories=order)
    df_info = df_info.sort_values(ready_col)
    # Initialize result DF
    df = pd.DataFrame()
    # Get key figure names
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_financial.csv")
    df_key = pd.read_csv(path)
    # Get kknr data
    key_figs = df_key.loc[
        df_key["entrypoint"] == "KKNR", "tunnusluku"].tolist()
    df = __fetch_financial_data(
        df=df, df_info=df_info,
        datatype="KKNR", year=(str(year) + "C12"), key_figs=key_figs,
        subset=subset, language=language, **args)
    # Get kktr data
    key_figs = df_key.loc[
        df_key["entrypoint"] == "KKTR", "tunnusluku"].tolist()
    df = __fetch_financial_data(
        df=df, df_info=df_info,
        datatype="KKTR", year=year, key_figs=key_figs,
        subset=subset, language=language, **args)
    # Get kkotr data
    key_figs = df_key.loc[
        df_key["entrypoint"] == "KKOTR", "tunnusluku"].tolist()
    df = __fetch_financial_data(
        df=df, df_info=df_info,
        datatype="KKOTR", year=year, key_figs=key_figs,
        subset=subset, language=language, **args)
    # Get ktpe data including only tax rate
    key_figs = df_key.loc[
        df_key["entrypoint"] == "KTPE", "tunnusluku"].tolist()
    df = __fetch_financial_data(
        df=df, df_info=df_info,
        datatype="KTPE", year=year, key_figs=key_figs,
        subset=True, language=language, **args)
    # Reset index and return whole data
    df = df.reset_index(drop=True)
    return df


def __fetch_financial_data(df, df_info,
                           datatype, year, key_figs,
                           subset, language, **args):
    """
    Fetch certain financial data of municipalities.

    Input: DF to append, DF including URL, DF including labels of financial
    codes, which data is fetched, year, which values will be returned if
    subset is True.
    Output: pd.DataFrame including financial data.
    """
    # Specify columns where label and values can be found
    url_col = "tunnusluvut"
    label_col = "tunnusluku"
    field_lab = ("tunnusluku" if language == "fi" else
                 ("tunnusluku_" + language))
    field_id = "solutunniste"
    value_col = "arvo"
    datatype_col = "raportointikokonaisuus"
    data_year = "raportointikausi"
    # Initialize for results
    df_temp = pd.DataFrame()
    # Get specific data information
    ind = ((df_info[datatype_col] == datatype) &
           (df_info[data_year] == year))
    # If certain data can be found from the database
    if any(ind):
        # Get the data info based on index
        ind = ind[ind]
        ind = ind.first_valid_index()
        # Get the url and fetch the data
        url = df_info.loc[ind, url_col]
        r = requests.get(url)
        text = r.json()
        # Create DF from the data
        df_temp = pd.DataFrame(text)
        # Get labels
        fields = __fetch_financial_taxonomy(datatype=datatype, subset=subset,
                                            key_figs=key_figs, **args)
        # Add labels to data
        df_temp["tunnusluku_lab"] = df_temp[label_col].replace(
            to_replace=fields.loc[:, field_id].astype(str).tolist(),
            value=fields.loc[:, field_lab].astype(str).tolist())
        # Values to float
        df_temp[value_col] = df_temp[value_col].astype(float)
        # If certain datatype, there are multiple rows with same label.
        # Sum them together
        if datatype == "KKNR":
            # Get summed-up values
            values = df_temp.groupby("tunnusluku_lab").aggregate(
                {value_col: "sum"})
            # Remove additional rows
            df_temp = df_temp.drop_duplicates(subset="tunnusluku_lab")
            # Add summed values
            df_temp = df_temp.drop(value_col, axis=1)
            df_temp = pd.merge(df_temp, values, on="tunnusluku_lab")
        # Subset
        if subset:
            df_temp = df_temp.loc[df_temp[label_col] !=
                                  df_temp["tunnusluku_lab"], :]
    # Add fetched data to results
    df = pd.concat([df, df_temp])
    return df


def __fetch_financial_taxonomy(datatype, subset, key_figs,
                               use_cache=True, temp_dir=None,
                               **args):
    """
    Fetch taxonomy of financial data.

    Input: Datatype, wheter to use on-disk cache, the name of temp_dir.
    Output: pd.DataFrame including taxonomy.
    """
    # INPUT CHECK
    if not isinstance(use_cache, bool):
        raise Exception(
            "'use_cache' must be True or False."
            )
    if not (isinstance(temp_dir, str) or temp_dir is None):
        raise Exception(
            "'temp_dir' must be None or string specifying temporary directory."
            )
    # INPUT CHECK END
    download_from_web = True
    label_col = "tunnusluku"
    # If cache is used, check if file can be found from temp directory
    if use_cache:
        if temp_dir is None:
            # Get the name of higher level tmp directory
            temp_dir_path = tempfile.gettempdir()
            temp_dir = temp_dir_path + "/osta"
        # Check if spedicified directory exists. If not, create it
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        # Check if file can be found
        if (datatype + ".json") in os.listdir(temp_dir):
            download_from_web = False
    # Download from web or use cache
    # https://api.tutkihallintoa.fi/kuntatalous/v1/taksonomia
    if download_from_web:
        url = ("https://tkdpprodjrpstacc02.blob.core.windows.net" +
               "/kuntataloudentaksonomia/" +
               datatype + ".json")
        r = requests.get(url)
        text = r.json()
        # Save the file to temporary directory if cache is used
        if use_cache:
            with open((temp_dir + "/" + datatype + ".json"), "w") as f:
                json.dump(text, f)
    else:
        # Load the data from cache
        with open((temp_dir + "/" + datatype + ".json")) as f:
            text = json.load(f)
    # Create a DF from the data
    df = pd.DataFrame(text)
    # Subset the data if only specific values are wanted
    if subset:
        ind = [x in key_figs for x in df[label_col]]
        df = df.loc[ind, :]
    return df


# getOrgComp


def __fetch_org_company_data_help(org_bid, year, datatype):
    """
    Fetch data about companies of municipality.

    Input: business ID of municipality, year, datatype.
    Output: pd.DataFrame including company data.
    """
    # Specify columns of the data
    bid_col = "ytunnus"
    ready_col = "hyvaksymisvaihe"
    data_year = "raportointikausi"
    datatype_col = "raportointikokonaisuus"
    url_col = "tolt_tiedot"
    tolt_col = "tolt_yksiköt"
    # Get the information on database, what data it includes?
    url = ("https://prodkuntarest.westeurope.cloudapp.azure.com/" +
           "rest/v1/json/tolt-aineistot")
    r = requests.get(url)
    text = r.json()
    text = text.get("tolt_aineisto")
    df_info = pd.DataFrame(text)
    # Sort data based on the readiness of the data
    order = ["Lopullinen", "Hyväksytty", "Alustava"]
    df_info[ready_col] = pd.Categorical(
        df_info[ready_col], categories=order)
    df_info = df_info.sort_values(ready_col)
    # Get specific data information
    ind = ((df_info[datatype_col] == datatype) &
           (df_info[data_year] == year) &
           (df_info[bid_col] == org_bid))
    # If certain data can be found from the database
    if any(ind):
        # Get the data info based on index
        ind = ind[ind]
        ind = ind.first_valid_index()
        # Get the url and fetch the data
        url = df_info.loc[ind, url_col]
        r = requests.get(url)
        text = r.json()
        text = text.get(tolt_col)
        # Create DF from the data
        df = pd.DataFrame(text)
    else:
        df = pd.DataFrame()
    return df

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import osta.__utils as utils
import pandas as pd
import warnings
import pkg_resources
import requests
import sys
import re
import tempfile
import os
import numpy as np
import xmltodict
import geopandas as gpd
import pyproj
from osta.__utils_enrich import __add_org_data, __add_account_data,\
    __add_service_data, __add_suppl_data, __add_sums,\
    __fetch_org_company_data_help, __fetch_org_financial_data_help,\
    __fetch_company_based_on_bid, __fetch_company_data_from_website,\
    __get_driver, __search_website, __search_fin_from_stats


def enrich(df, **args):
    """
    This function adds external data to dataset.

    Arguments:
        `df`: pandas.DataFrame containing invoice data.

        `**args`: Additional arguments passes into other functions:

        `org_data`: None or non-empty pandas.DataFrame containing
        organization data. It must include a column named "bid"
        (business ID), "vat_number" (VAT number), "code"
        (organization code), or "name" (name) which is used to
        match data with df. Business ID takes precedence, and
        match based on name is checked last if other matches
        are not found. If None, only general information,
        such as business ID and province, from package's
        database is added. (By default: org_data=None)

        `suppl_data`: None or non-empty pandas.DataFrame containing
        supplier data. It must include a column named "bid"
        (business ID), "vat_number" (VAT number), "code"
        (organization code), or "name" (name) which is used to
        match data with df. Business ID takes precedence, and
        match based on name is checked last if other matches
        are not found. (By default: suppl_data=None)

        `service_data`: None or non-empty pandas.DataFrame containing
        service category data. It must include a column named "code"
        (code) or "name" (name) which is used to match data with df.
        Number takes precedence, and match based on name is checked
        last if other matches are not found. If None, information from
        package's own database is added. (By default: service_data=None)

        `account_data`: None or non-empty pandas.DataFrame containing
        account data. It must include a column named "code"
        (code) or "name" (name) which is used to match data with df.
        Number takes precedence, and match based on name is checked
        last if other matches are not found. If None, information from
        package's own database is added. (By default: account_data=None)

        `disable_org`: A boolean value specifying whether to add organization
        data to the dataset (df). (By default: disable_org=False)

        `disable_suppl`: A boolean value specifying whether to add supplier
        data to the dataset (df). (By default: disable_suppl=False)

        `disable_service`: A boolean value specifying whether to add service
        data to the dataset (df). (By default: disable_service=False)

        `disable_account`: A boolean value specifying whether to add account
        data to the dataset (df). (By default: disable_account=False)

        `disable_sums`: A boolean value specifying whether to calculate
        possible missing value (total, VAT amount or price excluding VAT)
        based on other two values. (By default: disable_sums=False)

        `subset_account_data`: None or a string value ("tase" or
        "tuloslaskelma") specifying whether to use account data from
        package's database from balance sheet ("tase") or income statement
        ("tuloslaskelma"). If None, unique values are taken where balance
        sheet takes the precedence. (By default: subset_account_data=None)

        `db_year`: An integer value specifying the year of service and
        account database. If None, unique values are taken where the most
        present values take the precedence (By default: df_year=None)


    Details:
        This function enriches the dataset. The package includes some
        basic information, e.g., on organization, but you get more out of it
        by feeding more sophisticated and detailed data to the function with
        arguments. The datasets that are added must include specific columns.
        More detailed information is given in desciptions of each argument.

        Furthermore, the function is used to complement the data if one of
        the values descriping price, VAT and total price is missing.

    Examples:
        ```
        df = enrich(df, org_data=org_data, suppl_data=suppl_data)

        ```

    Output:
        A pandas.DataFrame including enriched dataset.

    """
    # INPUT CHECK
    # df must be pandas DataFrame
    if not utils.__is_non_empty_df(df):
        raise Exception(
            "'df' must be non-empty pandas.DataFrame."
            )
    # INPUT CHECK END

    # Add organization data
    df = __add_org_data(df, **args)
    # Add supplier data
    df = __add_suppl_data(df, **args)
    # Add account data
    df = __add_account_data(df, **args)
    # Add service data
    df = __add_service_data(df, **args)
    # Add missing total, vat_amount or price_ex_vat
    df = __add_sums(df, **args)
    return df


def getComp(
        bid=None, language="en", merge_bid=True,
        use_cache=True, temp_dir=None, verbose=True, name=None, **args):
    """
    Fetch company data from databases.

    Arguments:
        `bid`: A string or a list-like object including business IDs. If None,
        please provide 'name'. (By default: bid=None)

        `language`: A string specifying the language of fetched data. Must be
        "en" (English), "fi" (Finnish), or "sv" (Swedish).

        `merge_bid`: A boolean value specifying whether to combine all old BIDs
        to one column. If False, each BID is its own columns named
        'old_bid_*'. (By default: old_bid=True)

        `use_cache`: A boolean value specifying whether to store results to
        on-disk cache. (By default: use_cache=True)

        `temp_dir`: None or a string specifying path of temporary directory
        to store cache. If None, device's default temporary directory is used.
        (By default: temp_dir=None)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function fetches company data from Finnish Patent and Registration
        Office (Patentti- ja Rekisterihallitus, PRH) and The Business
        Information System (Yritystietojärjestelmä, YTJ). Resources of
        services are limited. Please use the function only when needed, and
        store the results if possible. Search in smaller batches to prevent
        problems with resource allocation. The function requires working
        internet connection.

    Examples:
        ```
        bids = pd.Series(["1458359-3", "2403929-2"])
        df = getComp(bids)
        ```

    Output:
        df with company data
    """
    # INPUT CHECK
    if not (bid is None or utils.__is_non_empty_list(bid) or
            isinstance(bid, str)):
        raise Exception(
            "'bid' must be a string non-empty pandas.Series or None."
            )
    if not (name is None or utils.__is_non_empty_list(name) or
            isinstance(name, str)):
        raise Exception(
            "'name' must be a string non-empty pandas.Series or None."
            )
    if bid is None and name is None:
        raise Exception(
            "Either 'bid' or 'name' must be non-empty pandas.Series."
            )
    # Ensure that both bid and name are pd.Series if they are not None
    bid = bid if bid is None else pd.Series(bid)
    name = name if name is None else pd.Series(name)
    if bid is not None and name is not None and len(bid) != len(name):
        raise Exception(
            "The lengths of 'bid' and 'name' must match."
            )
    if not (isinstance(language, str) and language in ["fi", "en", "sv"]):
        raise Exception(
            "'language' must be 'en', 'fi', or 'sv'."
            )
    if not isinstance(merge_bid, bool):
        raise Exception(
            "'merge_bid' must be True or False."
            )
    if not isinstance(use_cache, bool):
        raise Exception(
            "'use_cache' must be True or False."
            )
    if not (isinstance(temp_dir, str) or temp_dir is None):
        raise Exception(
            "'temp_dir' must be None or string specifying temporary directory."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # Get language in right format for database
    lan = "se" if language == "sv" else language
    # Create a DF that has both BIDs and names
    # Remove None values and duplicates
    df_bid = pd.DataFrame()
    df_bid["bid"] = bid
    df_bid["name"] = name
    df_bid = df_bid.dropna(axis=0, how="all")
    df_bid = df_bid.drop_duplicates()

    # Get True or False to specify whether search is done from the website
    search_from_website = __search_website(**args)
    # Initialize driver
    if search_from_website:
        driver = __get_driver()
    else:
        driver = None

    # Initialize result DF
    df = pd.DataFrame()
    # If cache is used, check if file can be found from temp directory
    filename = "company_data_from_prh_cache.csv"
    if use_cache:
        if temp_dir is None:
            # Get the name of higher level tmp directory
            temp_dir_path = tempfile.gettempdir()
            temp_dir = temp_dir_path + "/osta"
        # Check if spedicified directory exists. If not, create it
        if not os.path.isdir(temp_dir):
            os.makedirs(temp_dir)
        # Check if file can be found and load it
        if filename in os.listdir(temp_dir):
            df = pd.read_csv(
                (temp_dir + "/" + filename), dtype=object)
            # Remove those business ids that can be already found in cache
            if "bid" in df.columns:
                df_bid = df_bid.loc[~df_bid["bid"].isin(df["bid"]), :]

    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop though BIDs
    df_bid = df_bid.reset_index(drop=True)
    for row_i, row in df_bid.iterrows():
        # Update the progress bar
        if verbose:
            percent = 100*((row_i+1)/df_bid.shape[0])
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Get data from database
        bid = row["bid"]
        name = row["name"]
        if not pd.isna(bid):
            try:
                res = __fetch_company_based_on_bid(
                    bid, name, lan, language, browser=driver,
                    search_from_website=search_from_website, **args)
            except requests.exceptions.ConnectionError:
                warnings.warn(
                    message="Connection error. Max retries exceeded. \
                        Please try again later.",
                    category=Warning
                    )
                break
        elif search_from_website:
            try:
                # Try to find data based on name
                res = __fetch_company_data_from_website(
                    name, language, browser=driver, **args)  # type: ignore
                # Add search word
                res["search_word"] = name
            except Exception:
                res = pd.DataFrame([name], index=["search_word"]).transpose()
        else:
            res = pd.DataFrame([name], index=["search_word"]).transpose()
        # Add to DataFrame
        if df.empty:
            df = res
        else:
            df = pd.concat([df, res], join="outer")
        # In every 10 BID, save the result to cache
        if use_cache and row_i % 10 == 0:
            df.to_csv((temp_dir + "/" + filename), index=False)

    # Combine BID columns into one
    if merge_bid and "old_bid" in df.columns:
        regex = re.compile(r"old_bid")
        ind = [True if regex.search(x) else False for x in df.columns]
        bid_cols = df.loc[:, ind]
        bid_col = bid_cols.apply(lambda x: ', '.join(x.dropna(
            ).astype(str)), axis=1)
        # Remove additional BID columns, keep only one
        ind = [False if regex.search(x) else True for x in df.columns]
        df = df.loc[:, ind]
        df["old_bid"] = bid_col
    # Convert column names into right language if Finnish or Swedish
    if language == "fi":
        columns = {
            "registration_date": "rekisteröintipäivä",
            "company_form_short": "yhtiömuoto_lyhyt",
            "liquidation": "konkurssitiedot",
            "company_form": "yhtiömuoto",
            "business_line": "päätoimiala",
            "muni": "kotipaikka",
            "old_bid": "vanha_bid",
            }
        df = df.rename(columns=columns)
        df.columns = [re.sub("old_bid_", "vanha_bid_", str(x))
                      for x in df.columns.tolist()]
    elif language == "sv":
        columns = {
            "registration_date": "registrering_dag",
            "company_form_short": "företags_form_kort",
            "liquidation": "konkurs_info",
            "company_form": "företags_form",
            "business_line": "päätoimiala",
            "muni": "hemkommun",
            "old_bid": "gamla_bid",
            }
        df = df.rename(columns=columns)
        df.columns = [re.sub("old_bid_", "gamla_bid_", str(x))
                      for x in df.columns.tolist()]
    # Reset index
    df = df.reset_index(drop=True)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    # Wuit driver session
    if search_from_website:
        driver.quit()
    return df


def getMuni(code, year, language="en", add_bid=True):
    """
    Fetch municipality data from databases.

    Arguments:
        `code`: A string or a list-like object including municipality codes.

        `year`: A string or a list-like object including year specifying the
        year of data that will be fetched. The length must be equal with
        'code'.

        `language`: A string specifying the language of fetched data. Must be
        "en" (English), "fi" (Finnish), or "sv" (Swedish).
        (By default: language="en")

        `add_bid`: A boolean value specifying whether to add business ID of
        organization so that the returned table has a common identifier that
        matches with returned table of other interfaces.
        (By default: add_bid=True)

    Details:
        This function fetches municipality key figures from the database of
        Statistics Finland (Tilastokeskus). The function requires working
        internet connection.

    Examples:
        ```
        codes = pd.Series(["005", "020"])
        year = pd.Series(["02.05.2021", "20.10.2020"])
        df = fetch_org_data(codes, year, language="fi")
        ```

    Output:
        pd.DataFrame including municipality data.
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_list(code) or isinstance(code, str)):
        raise Exception(
            "'code' must be a string non-empty pandas.Series"
            )
    if not (utils.__is_non_empty_list(year) or isinstance(year, str)):
        raise Exception(
            "'year' must be a string non-empty pandas.Series."
            )
    # Ensure that inputs are as pd.Series; works with pd.Series, list or single
    # values
    code = pd.Series(code)
    year = pd.Series(year)
    # If year is only one value, repeat it
    if len(year) == 1:
        year = year.repeat(len(code))
    if len(code) != len(year):
        raise Exception(
            "The lengths of 'code' and 'year' must match."
            )
    if not (isinstance(language, str) and language in ["fi", "en", "sv"]):
        raise Exception(
            "'language' must be 'en', 'fi', or 'sv'."
            )
    if not isinstance(add_bid, bool):
        raise Exception(
            "'add_bid' must be True or False."
            )
    # INPUT CHECK END
    # Check that years are in correct format
    try:
        # Test if year can be detected, convert to str because integers are
        # interpreted as days
        year = year.astype(str)
        year = pd.to_datetime(year).dt.year
        year = year.astype(str)
    except Exception:
        raise Exception(
            "'year' were not detected."
            )
    # Find the most recent data
    url = "https://statfin.stat.fi/PXWeb/api/v1/fi/Kuntien_avainluvut"
    r = requests.get(url)

    # If the call was not succesfull, return empty DF
    df = pd.DataFrame()
    if not r.ok:
        return df

    text = r.json()
    available_years = [x.get("id") for x in text]
    year_max = max(available_years)
    if year is None:
        year = [year_max for x in range(0, len(code))]
    # Check which years are in time series database
    url = ("https://statfin.stat.fi/PXWeb/api/v1/fi/Kuntien_avainluvut/" +
           year_max)
    r = requests.get(url)
    text = r.json()
    # Find available years based on pattern in id
    found_year = [x.get("text") for x in text if x.get("id") ==
                  "kuntien_avainluvut_" + year_max + "_aikasarja.px"][0]
    p = re.compile("\\d\\d\\d\\d-\\d\\d\\d\\d")
    found_year = p.search(found_year)
    if found_year is not None:
        found_year = found_year.group().split("-")
    # Getn only years that are available
    years_temp = [x if int(x) in
                  list(range(int(found_year[0]), int(found_year[1])+1))
                  else None for x in year]
    years_not_found = [x for i, x in enumerate(year)
                       if x != years_temp[i]]
    if len(years_not_found):
        warnings.warn(
            message=f"The following 'years' were not found from the "
            f"database: {np.unique(years_not_found).tolist()}",
            category=Warning
            )
    # Check which municipalties are found from the database / are correct
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_municipality.csv")
    org_data = pd.read_csv(path, index_col=0, dtype="object")
    # Get only correct municipality codes
    codes_temp = [x if x in org_data["code"].tolist() else
                  None for x in code]
    codes_not_found = [x for i, x in enumerate(code)
                       if x != codes_temp[i]]
    if len(codes_not_found):
        warnings.warn(
            message=f"The following 'codes' were not found from the database: "
            f"{np.unique(codes_not_found).tolist()}",
            category=Warning
            )
    # Create DF, drop duplicates, and remove incorrect years and codes
    df = pd.DataFrame({"code": codes_temp, "year": years_temp})
    df = df.drop_duplicates()
    df = df.dropna()
    # Get URL and correct parameters of the time series database
    url = ("https://pxdata.stat.fi:443/PxWeb/api/v1/" + language +
           "/Kuntien_avainluvut/" + year_max + "/kuntien_avainluvut_" +
           year_max + "_aikasarja.px")
    params = {"query": [{"code": "Alue " + year_max,
                         "selection": {"filter": "item", "values":
                                       df["code"].drop_duplicates(
                                           ).tolist()}},
                        {"code": "Vuosi",
                         "selection": {"filter": "item", "values":
                                       df["year"
                                          ].drop_duplicates().tolist()}}],
              "response": {"format": "json-stat2"}
              }
    # Find results
    r = requests.post(url, json=params)
    if r.ok:
        text = r.json()
        # Find labels, code, years and values
        label = list(text.get("dimension").get("Tiedot").get(
            "category").get("label").values())
        code = list(text.get("dimension").get("Alue 2021").get(
            "category").get("label").keys())
        years = list(text.get("dimension").get("Vuosi").get(
            "category").get("label").values())
        values = text.get("value")
        # Divide values based on mucipalities
        values_num = int(len(values)/len(code))
        df_temp = pd.DataFrame()
        for i in range(0, len(values), values_num):
            # Split based on organization
            temp = pd.Series(values[i:i+values_num])
            # Split based on year
            temp = [temp[i::len(years)].tolist() for i in range(len(years))]
            temp = pd.DataFrame(temp).transpose()
            df_temp = pd.concat([df_temp, temp], axis=1)
        # Add label and code
        df_temp.index = label
        df_temp.loc["code", :] = [x for x in code for i in range(len(years))]
        df_temp = df_temp.transpose()
        df = pd.merge(df, df_temp)
    # If specified, add business ID
    if add_bid and not df.empty:
        df = pd.merge(df, org_data.loc[:, ["code", "bid"]],
                      how="left", left_on="code", right_on="code")
    elif df.empty:
        df = None
    return df


def getMuniFin(
        bid, year, subset=True, wide_format=True, language="en",
        rename_cols=True, verbose=True, **args):
    """
    Fetch financial data of municipalities.

    Arguments:
        `bid`: A string or a list-like object including business IDs of
        municipalities.

        `year`: A string or a list-like object including year specifying the
        year of data that will be fetched.

        `subset`: a boolean value specifying whether only certain key figures
        are returned. (By default: subset=True)

        `wide_format`: a boolean value specifying whether result is returned as
        wide format. When wide format is specified, the returned table contains
        only columns with financial values and corresponding organization
        without report metadata. (By default: wide_format=True)

        `language`: A string specifying the language of fetched data. Must be
        "en" (English), "fi" (Finnish), or "sv" (Swedish).

        `rename_cols`: A boolean value specifying whether to rename columns in
        a way that is expected by other functions.
        (By default: rename_cols=True)

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function fetches financial data of municipalities
        (KKNR20XXC12, KKTR20XX, and KKOTR20XX) from the database
        of State Treasury of Finland (Valtiokonttori). The data is fetched
        based on business ID and year. Currently, database include data only
        in Finnish and Swedish. The function requires working internet
        connection.

        When data is subsetted, only certain key figures are returned. They
        include (in Finnish):

        "Antolainasaamisten lisäys",

        "Antolainasaamisten vähennys",

        "Antolainasaamisten muutokset + (-)",

        "Antolainasaamisten muutokset",

        "Investointien rahavirta",

        "Lainakannan muutokset",

        "Lyhytaikaisten lainojen lisäys",

        "Lyhytaikaisten lainojen vähennys",

        "Lyhytaikaisten lainojen muutos",

        "Muut maksuvalmiuden muutokset",

        "Muut maksuvalmiuden muutokset + (-)",

        "Oman pääoman muutokset + (-)",

        "Oman pääoman muutokset",

        "Pitkäaikaisten lainojen lisäys",

        "Pitkäaikaisten lainojen vähennys",

        "Pitkäaikaisten lainojen muutos",

        "Rahavarat 1.1.",

        "Rahavarat 31.12.",

        "Rahavarojen muutos",

        "Rahoituksen rahavirta",

        "Satunnaiset erät",

        "Toiminnan rahavirta",

        "Toimintakate",

        "Toimintakulut",

        "Toimintatuotot",

        "Tulorahoituksen korjauserät",

        "Verotulot",

        "Vuosikate",

        "2400-2439 Pitkäaikainen (korollinen vieras pääoma)",

        "2500-2539 Lyhytaikainen (korollinen vieras pääoma)",

        "5000-5499 Verotulot",

        "5500-5899 Valtionosuudet",

        "6000-6099 Korkotuotot",

        "7000-7299 Poistot ja arvonalentumiset",

        "8000-8199 Satunnaiset erät + (-)",

        "8800-8800 Tilikauden ylijäämä (alijäämä)",

        "Toimintakate",

        "Toimintakulut",

        "Toimintatulot",

        "Tuloveroprosentti"

        ... of municipality and...

        "Antolainasaamisten lisäys",

        "Antolainasaamisten vähennys",

        "Antolainasaamisten muutokset + (-)",

        "Antolainasaamisten muutokset",

        "Investointien rahavirta",

        "Korkotuotot",

        "Lainakannan muutokset + (-)",

        "Lainakannan muutokset",

        "Lyhytaikainen (korollinen vieras pääoma)",

        "Lyhytaikaisten lainojen lisäys",

        "Lyhytaikaisten lainojen vähennys",

        "Lyhytaikaisten lainojen muutos",

        "Muut maksuvalmiuden muutokset + (-)",

        "Muut maksuvalmiuden muutokset",

        "Oman pääoman muutokset + (-)",

        "Oman pääoman muutokset",

        "Pitkäaikaisten lainojen lisäys",

        "Pitkäaikaisten lainojen vähennys",

        "Pitkäaikaisten lainojen muutos",

        "Poistot ja arvonalentumiset",

        "Rahavarat 1.1.",

        "Rahavarat 31.12.",

        "Rahavarojen muutos",

        "Rahoituksen rahavirta",

        "Tilikauden tulos",

        "Tilikauden ylijäämä (alijäämä)",

        "Toiminnan rahavirta",

        "Tulorahoituksen korjauserät",

        "Tuloveroprosentti",

        "Vuosikate"

        ... of municipal group.

    Examples:
        ```
        bid = pd.Series(["0135202-4", "0204819-8"])
        year = pd.Series(["2021", "2020"])
        df = fetch_financial_data(bid, year)
        ```

    Output:
        pd.DataFrame including financial data.
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_list(bid) or isinstance(bid, str)):
        raise Exception(
            "'bid' must be a string non-empty pandas.Series"
            )
    if not (utils.__is_non_empty_list(year) or isinstance(year, str)):
        raise Exception(
            "'year' must be a string non-empty pandas.Series."
            )
    # Ensure that inputs are as pd.Series; works with pd.Series, list or single
    # values
    bid = pd.Series(bid)
    year = pd.Series(year)
    # If year is only one value, repeat it
    if len(year) == 1:
        year = year.repeat(len(bid))
    if len(bid) != len(year):
        raise Exception(
            "The lengths of 'bid' and 'year' must match."
            )
    if not isinstance(subset, bool):
        raise Exception(
            "'subset' must be a boolean value."
            )
    if not isinstance(wide_format, bool):
        raise Exception(
            "'wide_format' must be a boolean value."
            )
    if not (isinstance(language, str) and language in ["fi", "en", "sv"]):
        raise Exception(
            "'language' must be 'en', 'fi', or 'sv'."
            )
    if not isinstance(rename_cols, bool):
        raise Exception(
            "'rename_cols' must be a boolean value."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # Test if year can be detected, and convert it to object
    try:
        # Test if year can be detected, convert to str because integers are
        # interpreted as days
        year = year.astype(str)
        year = pd.to_datetime(year).dt.year
        year = year.astype(str)
    except Exception:
        raise Exception(
            "'year' data was not detected."
            )
    # Create a dataframe and remove duplicates
    df_org = pd.DataFrame({"bid": bid.tolist(), "year": year.tolist()})
    df_org = df_org.drop_duplicates()
    df_org = df_org.reset_index(drop=True)

    # If the data includes only years before 2021, they can be found from
    # Statistics Finland. --> use different function
    if all(df_org["year"].isin([
            "2015", "2016", "2017", "2018", "2019", "2020"])):
        df = __search_fin_from_stats(df_org, subset)
        return df

    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop over rows
    df = pd.DataFrame()
    df_not_found = pd.DataFrame()
    for i, r in df_org.iterrows():
        # Update the progress bar
        percent = 100*((i+1)/df_org.shape[0])
        if verbose:
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Get data from the database
        df_temp = __fetch_org_financial_data_help(
            r["bid"], r["year"], subset=subset, language=language, **args)
        # Add organization and year info
        df_temp["bid"] = r["bid"]
        df_temp["year"] = r["year"]
        # If the data was not found
        if df_temp.empty:
            df_temp = pd.DataFrame([r["bid"], r["year"]],
                                   index=["bid", "year"]).transpose()
            df_not_found = pd.concat([df_not_found, df_temp])
        else:
            # Add to whole data
            df = pd.concat([df, df_temp])
    # Reset index and return whole data
    df = df.reset_index(drop=True)
    # Rename columns if specified
    if rename_cols:
        new_colnames = {
            "alkupvm": "report_start_date",
            "hyväksymispvm": "report_approval_date",
            "hyväksymisvaihe": "report_approval_phase",
            "kieli": "report_language",
            "kommentti": "comment",
            "osakokonaisuus": "report_subentity",
            "raportointikausi": "reporting_period",
            "raportointikokonaisuus": "report_entity",
            "taksonomia": "report_taxonomy",
            "tarkastushavainnot": "report_observations",
            "tunnusluku": "key_figure",
            "ytunnus": "org_bid",
            "tunnusluku_lab": "key_figure_label",
            "arvo": "value",
            }
        df = df.rename(columns=new_colnames)
    # If specified, convert into wide format
    if not df.empty and wide_format:
        df = df.pivot_table(index="bid",
                            columns="key_figure_label",
                            values="value")
        df = df.reset_index(drop=False)
    # Give warning if some input values were not found
    if not df_not_found.empty:
        warnings.warn(
            message=f"The following BID-year combinations were not found:\n"
            f"{df_not_found}",
            category=Warning
            )
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    return df


def getMuniComp(bid, year, language="en", verbose=True):
    """
    Fetch data about companies of municipality.

    Arguments:
        `bid`: A string or a list-like object including business IDs of
        municipalities.

        `year`: A string or a list-like object including year specifying the
        year of data that will be fetched.

        `language`: A string specifying the language of fetched data. Must be
        "en" (English), or "fi" (Finnish).

        'verbose': A boolean value specifying whteher to show a progress bar.
        (By default: verbose=True)

    Details:
        This function fetches data on companies of municipalities (TOLT)
        from the database of State Treasury of Finland (Valtiokonttori).
        The function requires working internet connection.

    Examples:
        ```
        codes = pd.Series(["0135202-4", "1567535-0"])
        year = pd.Series(["2021", "2022"])
        df = fetch_org_company_data(codes, year)
        ```

    Output:
        pd.DataFrame including company data.
    """
    # INPUT CHECK
    if not (utils.__is_non_empty_list(bid) or isinstance(bid, str)):
        raise Exception(
            "'bid' must be a string non-empty pandas.Series"
            )
    if not (utils.__is_non_empty_list(year) or isinstance(year, str)):
        raise Exception(
            "'year' must be a string non-empty pandas.Series."
            )
    # Ensure that inputs are as pd.Series; works with pd.Series, list or single
    # values
    bid = pd.Series(bid)
    year = pd.Series(year)
    # If year is only one value, repeat it
    if len(year) == 1:
        year = year.repeat(len(bid))
    if len(bid) != len(year):
        raise Exception(
            "The lengths of 'bid' and 'year' must match."
            )
    if not (isinstance(language, str) and language in ["fi", "en"]):
        raise Exception(
            "'language' must be 'en', or 'fi'."
            )
    if not isinstance(verbose, bool):
        raise Exception(
            "'verbose' must be True or False."
            )
    # INPUT CHECK END
    # Test if year can be detected
    try:
        # Test if year can be detected, convert to str because integers are
        # interpreted as days
        year = year.astype(str)
        year = pd.to_datetime(year).dt.year
        year = year.astype(str)
    except Exception:
        raise Exception(
            "'year' data was not detected."
            )
    # Create a DF and remove duplicates
    df_org = pd.DataFrame([bid, year], index=["org_bid", "year"])
    df_org = df_org.transpose()
    df_org = df_org.drop_duplicates()
    # Add different datatypes
    df_org["type"] = "TOLT"
    df_org_temp = df_org.copy()
    df_org_temp["type"] = "HTOLT"
    df_org = pd.concat([df_org, df_org_temp])
    df_org = df_org.reset_index(drop=True)
    # For progress bar, specify the width of it
    progress_bar_width = 50
    # Loop over rows
    df = pd.DataFrame()
    for i, r in df_org.iterrows():
        # Update the progress bar
        if verbose:
            percent = 100*((i+1)/df_org.shape[0])
            sys.stdout.write('\r')
            sys.stdout.write("Completed: [{:{}}] {:>3}%"
                             .format('='*int(percent/(100/progress_bar_width)),
                                     progress_bar_width, int(percent)))
            sys.stdout.flush()
        # Get data from the database
        df_temp = __fetch_org_company_data_help(
            r["org_bid"], r["year"], r["type"])
        # Add organization and year info
        df_temp["org_bid"] = r["org_bid"]
        df_temp["year"] = r["year"]
        # Add to whole data
        df = pd.concat([df, df_temp])
    # Reset index and return whole data
    df = df.reset_index(drop=True)
    # Rename columns if specified
    if language == "en":
        new_colnames = {
            "alkupvm": "report_start_date",
            "hyväksymispvm": "report_approval_date",
            "hyväksymisvaihe": "report_approval_phase",
            "kieli": "report_language",
            "kunta_ytunnus": "municipality_bid",
            "lei_tunnus": "lei_code",
            "loppupvm": "report_end_date",
            "osuus_aanivallasta": "share_vote",
            "osuus_osakepaaomasta": "share_capital",
            "raportointikausi": "reporting_period",
            "raportointikokonaisuus": "report_entity",
            "sidosyksikkoasemassa": "affiliated_entity",
            "tolt_nimi": "name",
            "tolt_toimiala": "industry",
            "tolt_tunnus": "bid",
            "tunniste": "company_code",
            "tyyppi": "company_type",
            "virhetilanne": "report_error",
            }
        df = df.rename(columns=new_colnames)
    # Convert specific column to float
    ind = [x for x in ["share_vote", "osuus_aanivallasta"] if x in df.columns]
    if len(ind) == 1:
        df[ind[0]] = df[ind[0]].astype(str).str.strip(
            ).replace(r'^\s*$', None, regex=True).astype(float)
    ind = [x for x in ["share_capital", "osuus_osakepaaomasta"]
           if x in df.columns]
    if len(ind) == 1:
        df[ind[0]] = df[ind[0]].astype(str).str.strip(
            ).replace(r'^\s*$', None, regex=True).astype(float)
    # Stop progress bar
    if verbose:
        sys.stdout.write("\n")
    return df


def getMuniMap(year=None, resolution="1000", coord_sys="4326"):
    """
    Fetch the coordinate data of municipality borders from Statistics Finland
    (Tilastokeskus,
     https://www.stat.fi/org/avoindata/paikkatietoaineistot/kuntapohjaiset_tilastointialueet.html).

    Arguments:
        `year`: A string or an integer specifying the year of the data.

        `resolution`: A string specifying the resolution of the data. Must be
        "1000" (1 : 1 000 000) or "4500" (1 : 4 500 000).
        (By default: resolution="1000")

        `coord_sys`: A string specifying the coordinate system to which the
        data is converted. (By default: coord_sys="4326")

    Details:
        This function fetches coordinates of borders of municipalities. The
        borders are retunred as a polygons that can be plotted.

    Examples:
        ```
        # Fetch map data for all municipalities.
        df_map = fetch_map_data(2023)
        ```

    Output:
        pandas.DataFrame with url addresses.

    """
    # INPUT CHECK
    if not (isinstance(year, str) or isinstance(year, (int, np.integer))):
        raise Exception(
            "'year' must be a string or an integer."
            )
    year = str(year)
    if not (isinstance(resolution, str) and
            (resolution == "1000" or resolution == "4500")):
        raise Exception(
            "'resolution' must be '1000' or '4500'."
            )
    if not isinstance(coord_sys, str):
        raise Exception(
            "'coord_sys' must be a string."
            )
    # INPUT CHECK END
    output_format = "json"
    # Get available years
    response = requests.get(
        "https://geo.stat.fi/geoserver/tilastointialueet/wfs?service=WFS&"
        "request=GetCapabilities&version=2.0.0")
    if not response.ok:
        raise Exception(
            "Error while fetching the data. Please, check internet connection."
            )
    dict_data = xmltodict.parse(response.content)
    # Loop through results and get those years that have municipality data at
    # 1: 4 500 000 resolution
    years = []
    for x in dict_data["wfs:WFS_Capabilities"]["FeatureTypeList"][
            "FeatureType"]:
        temp = x["Title"]
        temp = re.search("Kunnat \\d\\d\\d\\d \\(1:4 500 000\\)", temp)
        if temp and temp is not None:
            temp = re.search("\\d\\d\\d\\d",
                             temp.group()).group()  # type: ignore
            years.append(temp)
    # Check that year is correct
    if year not in years:
        raise Exception(
            "The database does not include data from year specified by 'year'."
            )
    # URL to database
    url = "https://geo.stat.fi/geoserver/wfs?amp%3Brequest=GetCapabilities&"\
        "request=GetFeature&service=WFS&version=1.1.0&"\
        "typeName=tilastointialueet:kunta" + resolution + "k"\
        "_" + year + "&outputFormat=" + output_format
    # Get the data. Try catch; year might not be correct
    df = gpd.read_file(url)
    # Convert data to coordinate system
    df = df.to_crs(pyproj.CRS.from_epsg(coord_sys))
    return df

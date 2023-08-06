#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pkg_resources
import pandas as pd


def orgData():
    """
    Get organization data.

    Arguments:

    Details:
        Get organization data that osta package is utilizing as a resource.

    Examples:
        ```
        df = orgData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_municipality.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df


def accountData():
    """
    Get account data.

    Arguments:

    Details:
        Get account data that osta package is utilizing as a resource.

    Examples:
        ```
        df = accountData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_account.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df


def serviceData():
    """
    Get service data.

    Arguments:

    Details:
        Get service data that osta package is utilizing as a resource.

    Examples:
        ```
        df = serviceData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_service.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df


def financialData():
    """
    Get financial data.

    Arguments:

    Details:
        Get financial code data (only key figures) that osta package is
        utilizing as a resource.

    Examples:
        ```
        df = financialData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_financial.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df


def landData():
    """
    Get land data.

    Arguments:

    Details:
        Get land data that osta package is utilizing as a resource.

    Examples:
        ```
        df = landData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_land.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df


def fieldData():
    """
    Get field data.

    Arguments:

    Details:
        Get field data that osta package is utilizing as a resource.

    Examples:
        ```
        df = fieldData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_mandatory.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_optional.csv")
    df2 = pd.read_csv(path, index_col=0, dtype=str)
    df = pd.concat([df, df2])
    return df


def fieldPairData():
    """
    Get field pair data.

    Arguments:

    Details:
        Get data on what fields are name-number pairs. Data is utilized by
        osta package.

    Examples:
        ```
        df = fieldPairData()
        ```

    Output:
        pandas.DataFrame.

    """
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_pairs.csv")
    df = pd.read_csv(path, index_col=0, dtype=str)
    return df

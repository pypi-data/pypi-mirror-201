#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import osta.resources as res
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import pkg_resources


def test_orgData():
    with pytest.raises(Exception):
        df = res.orgData(123)
    with pytest.raises(Exception):
        df = res.orgData(True)
    with pytest.raises(Exception):
        df = res.orgData("test")
    df = res.orgData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_municipality.csv")
    df_ref = pd.read_csv(path, index_col=0, dtype=str)
    assert_frame_equal(df, df_ref)


def test_accountData():
    with pytest.raises(Exception):
        df = res.accountData(123)
    with pytest.raises(Exception):
        df = res.accountData(True)
    with pytest.raises(Exception):
        df = res.accountData("test")
    df = res.accountData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_account.csv")
    df_ref = pd.read_csv(path, index_col=0, dtype=str)
    assert_frame_equal(df, df_ref)


def test_serviceData():
    with pytest.raises(Exception):
        df = res.serviceData(123)
    with pytest.raises(Exception):
        df = res.serviceData(True)
    with pytest.raises(Exception):
        df = res.serviceData("test")
    df = res.serviceData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_service.csv")
    df_ref = pd.read_csv(path, index_col=0, dtype=str)
    assert_frame_equal(df, df_ref)


def test_financialData():
    with pytest.raises(Exception):
        df = res.financialData(123)
    with pytest.raises(Exception):
        df = res.financialData(True)
    with pytest.raises(Exception):
        df = res.financialData("test")
    df = res.financialData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_financial.csv")
    df_ref = pd.read_csv(path, index_col=0, dtype=str)
    assert_frame_equal(df, df_ref)


def test_landData():
    with pytest.raises(Exception):
        df = res.landData(123)
    with pytest.raises(Exception):
        df = res.landData(True)
    with pytest.raises(Exception):
        df = res.landData("test")
    df = res.landData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "data_land.csv")
    df_ref = pd.read_csv(path, index_col=0, dtype=str)
    assert_frame_equal(df, df_ref)


def test_fieldData():
    with pytest.raises(Exception):
        df = res.fieldData(123)
    with pytest.raises(Exception):
        df = res.fieldData(True)
    with pytest.raises(Exception):
        df = res.fieldData("test")
    df = res.fieldData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_mandatory.csv")
    df_ref = pd.read_csv(path, index_col=0)
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_optional.csv")
    df2 = pd.read_csv(path, index_col=0)
    df_ref = pd.concat([df_ref, df2])
    assert_frame_equal(df, df_ref)


def test_fieldPairData():
    with pytest.raises(Exception):
        df = res.fieldPairData(123)
    with pytest.raises(Exception):
        df = res.fieldPairData(True)
    with pytest.raises(Exception):
        df = res.fieldPairData("test")
    df = res.fieldPairData()
    path = pkg_resources.resource_filename(
        "osta", "resources/" + "fields_pairs.csv")
    df_ref = pd.read_csv(path, index_col=0)
    assert_frame_equal(df, df_ref)

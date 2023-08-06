#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from osta.enrich import enrich
from osta.enrich import getComp
from osta.enrich import getMuniFin
from osta.enrich import getMuniComp
from osta.enrich import getMuni
from osta.enrich import getMuniMap
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import requests


def test_enrich_wrong_arguments():
    df = __create_dummy_data()
    with pytest.raises(Exception):
        enrich()
    with pytest.raises(Exception):
        enrich(pd.DataFrame())
    with pytest.raises(Exception):
        enrich(1)
    with pytest.raises(Exception):
        enrich("test")
    with pytest.raises(Exception):
        enrich(True)
    with pytest.raises(Exception):
        enrich(df, org_data=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, org_data=1)
    with pytest.raises(Exception):
        enrich(df, org_data="test")
    with pytest.raises(Exception):
        enrich(df, org_data=True)
    with pytest.raises(Exception):
        enrich(df, suppl_data=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, suppl_data=1)
    with pytest.raises(Exception):
        enrich(df, suppl_data="test")
    with pytest.raises(Exception):
        enrich(df, suppl_data=True)
    with pytest.raises(Exception):
        enrich(df, service_data=[pd.DataFrame()])
    with pytest.raises(Exception):
        enrich(df, service_data=1)
    with pytest.raises(Exception):
        enrich(df, service_data="test")
    with pytest.raises(Exception):
        enrich(df, service_data=True)
    with pytest.raises(Exception):
        enrich(df, account_data=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, account_data=1)
    with pytest.raises(Exception):
        enrich(df, account_data="test")
    with pytest.raises(Exception):
        enrich(df, account_data=True)
    with pytest.raises(Exception):
        enrich(df, disable_org=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, disable_org=1)
    with pytest.raises(Exception):
        enrich(df, disable_org="test")
    with pytest.raises(Exception):
        enrich(df, disable_org=[True])
    with pytest.raises(Exception):
        enrich(df, disable_suppl=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, disable_suppl=1)
    with pytest.raises(Exception):
        enrich(df, disable_suppl="test")
    with pytest.raises(Exception):
        enrich(df, disable_suppl=[True])
    with pytest.raises(Exception):
        enrich(df, disable_service=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, disable_service=None)
    with pytest.raises(Exception):
        enrich(df, disable_service="test")
    with pytest.raises(Exception):
        enrich(df, disable_service=[True])
    with pytest.raises(Exception):
        enrich(df, disable_account=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, disable_account=None)
    with pytest.raises(Exception):
        enrich(df, disable_account="test")
    with pytest.raises(Exception):
        enrich(df, disable_account=[True])
    with pytest.raises(Exception):
        enrich(df, disable_sums=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, disable_sums=None)
    with pytest.raises(Exception):
        enrich(df, disable_sums="test")
    with pytest.raises(Exception):
        enrich(df, disable_sums=[True])
    with pytest.raises(Exception):
        enrich(df, subset_account_data=pd.DataFrame())
    with pytest.raises(Exception):
        enrich(df, subset_account_data="test")
    with pytest.raises(Exception):
        enrich(df, subset_account_data=[True])


def test_getComp_wrong_arguments():
    df = __create_dummy_data()
    bids = pd.Series(["1458359-3", "2403929-2"])
    with pytest.raises(Exception):
        getComp()
    with pytest.raises(Exception):
        getComp(df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getComp(pd.Series())
    with pytest.raises(Exception):
        getComp(1)
    with pytest.raises(Exception):
        getComp(None)
    with pytest.raises(Exception):
        getComp(bids, df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getComp(bids, pd.Series())
    with pytest.raises(Exception):
        getComp(bids, 1)
    with pytest.raises(Exception):
        getComp(bids, language="test")
    with pytest.raises(Exception):
        getComp(bids, language=1)
    with pytest.raises(Exception):
        getComp(bids, language=True)
    with pytest.raises(Exception):
        getComp(bids, language=None)
    with pytest.raises(Exception):
        getComp(bids, merge_bid="test")
    with pytest.raises(Exception):
        getComp(bids, merge_bid=1)
    with pytest.raises(Exception):
        getComp(bids, merge_bid=None)
    with pytest.raises(Exception):
        getComp(bids, use_cache="test")
    with pytest.raises(Exception):
        getComp(bids, use_cache=1)
    with pytest.raises(Exception):
        getComp(bids, use_cache=None)
    with pytest.raises(Exception):
        getComp(bids, temp_dir=["test"])
    with pytest.raises(Exception):
        getComp(bids, temp_dir=1)
    with pytest.raises(Exception):
        getComp(bids, temp_dir=True)


def test_getMuniFin_wrong_arguments():
    df = __create_dummy_data()
    codes = pd.Series(["0135202-4", "1567535-0"])
    years = pd.Series(["2021", "2022"])
    with pytest.raises(Exception):
        getMuniFin()
    with pytest.raises(Exception):
        getMuniFin(df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniFin(pd.Series())
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniFin(codes, pd.Series())
    with pytest.raises(Exception):
        getMuniFin(1)
    with pytest.raises(Exception):
        getMuniFin("TEST")
    with pytest.raises(Exception):
        getMuniFin(codes)
    with pytest.raises(Exception):
        getMuniFin(codes, "test")
    with pytest.raises(Exception):
        getMuniFin(codes, True)
    with pytest.raises(Exception):
        getMuniFin(codes, years, subset=1)
    with pytest.raises(Exception):
        getMuniFin(codes, years, subset="test")
    with pytest.raises(Exception):
        getMuniFin(codes, years, subset=None)
    with pytest.raises(Exception):
        getMuniFin(codes, years, wide_format=1)
    with pytest.raises(Exception):
        getMuniFin(codes, years, wide_format="test")
    with pytest.raises(Exception):
        getMuniFin(codes, years, wide_format=None)
    with pytest.raises(Exception):
        getMuniFin(codes, years, language=1)
    with pytest.raises(Exception):
        getMuniFin(codes, years, language="test")
    with pytest.raises(Exception):
        getMuniFin(codes, years, language=None)
    with pytest.raises(Exception):
        getMuniFin(codes, years, rename_cols=1)
    with pytest.raises(Exception):
        getMuniFin(codes, years, rename_cols="test")
    with pytest.raises(Exception):
        getMuniFin(codes, years, rename_cols=None)


def test_getMuniComp_wrong_arguments():
    df = __create_dummy_data()
    codes = pd.Series(["0135202-4", "1567535-0"])
    years = pd.Series(["2021", "2022"])
    with pytest.raises(Exception):
        getMuniComp()
    with pytest.raises(Exception):
        getMuniComp(df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniComp(pd.Series())
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniComp(codes, pd.Series())
    with pytest.raises(Exception):
        getMuniComp(1)
    with pytest.raises(Exception):
        getMuniComp("TEST")
    with pytest.raises(Exception):
        getMuniComp(codes)
    with pytest.raises(Exception):
        getMuniComp(codes, "test")
    with pytest.raises(Exception):
        getMuniComp(codes, True)
    with pytest.raises(Exception):
        getMuniComp(codes, years, rename_cols=1)
    with pytest.raises(Exception):
        getMuniComp(codes, years, rename_cols="test")
    with pytest.raises(Exception):
        getMuniComp(codes, years, rename_cols=None)


def test_getMuni_wrong_arguments():
    df = __create_dummy_data()
    codes = pd.Series(["020", "005"])
    years = pd.Series(["2021", "2022"])
    with pytest.raises(Exception):
        getMuni()
    with pytest.raises(Exception):
        getMuni(df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuni(pd.Series())
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuni(codes, pd.Series())
    with pytest.raises(Exception):
        getMuni(1)
    with pytest.raises(Exception):
        getMuni("TEST")
    with pytest.raises(Exception):
        getMuni(codes)
    with pytest.raises(Exception):
        getMuni(codes, "test")
    with pytest.raises(Exception):
        getMuni(codes, True)
    with pytest.raises(Exception):
        getMuni(codes, years, add_bid=1)
    with pytest.raises(Exception):
        getMuni(codes, years, add_bid="test")
    with pytest.raises(Exception):
        getMuni(codes, years, add_bid=None)
    with pytest.raises(Exception):
        getMuni(codes, years, language=1)
    with pytest.raises(Exception):
        getMuni(codes, years, language="test")
    with pytest.raises(Exception):
        getMuni(codes, years, language=None)


def test_getMuniMap_wrong_arguments():
    df = __create_dummy_data()
    codes = pd.Series(["020", "005"])
    with pytest.raises(Exception):
        getMuniMap()
    with pytest.raises(Exception):
        getMuniMap(df)
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniMap(pd.Series())
    with pytest.raises(Exception):
        with pytest.warns(Warning):
            getMuniMap(codes, pd.Series())
    with pytest.raises(Exception):
        getMuniMap(1)
    with pytest.raises(Exception):
        getMuniMap("TEST")
    with pytest.raises(Exception):
        getMuniMap(codes)
    with pytest.raises(Exception):
        getMuniMap(codes, "test")
    with pytest.raises(Exception):
        getMuniMap(codes, True)


def test_enrich():
    df = __create_dummy_data()
    df.columns = ["test", "org_code"]
    data = {"info": ["information", "testi_3", "test_2"],
            "code": ["1", "256", "5673"],
            }
    df_add = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, org_data=df_add)
    df = df.loc[:, ["test", "org_code", "org_info"]]
    df_expect["org_info"] = ["information", None, None]
    assert_frame_equal(df, df_expect)

    df = __create_dummy_data()
    df.columns = ["suppl_name", "test"]
    data = {"name": ["test", "testi_not", "test"],
            "info": ["information", "testi_3", "test_2"],
            "code": ["1", "256", "5673"],
            }
    df_add = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, suppl_data=df_add)
    df = df.loc[:, ["suppl_name", "test", "suppl_info"]]
    df_expect["suppl_info"] = ["information", None, "information"]
    assert_frame_equal(df, df_expect)

    df = __create_dummy_data()
    df.columns = ["account_name", "test"]
    data = {"name": ["test", "testi_not", "test"],
            "info": ["information", "testi_3", "test_2"],
            "code": ["1", "256", "5673"],
            }
    df_add = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, account_data=df_add)
    df = df.loc[:, ["account_name", "test", "account_info"]]
    df_expect["account_info"] = ["information", None, "information"]
    assert_frame_equal(df, df_expect)

    df = __create_dummy_data()
    df.columns = ["test", "service_code"]
    data = {"info": ["information", "testi_3", "test_2"],
            "code": ["1", "256", "5673"],
            }
    df_add = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, service_data=df_add)
    df = df.loc[:, ["test", "service_code", "service_info"]]
    df_expect["service_info"] = ["information", None, None]
    assert_frame_equal(df, df_expect)

    df = __create_dummy_data()
    df.columns = ["test", "service_code"]
    data = {"info": ["information", "testi_3", "test_2"],
            "code": ["1", "256", "5673"],
            }
    df_add = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, service_data=df_add, disable_service=True)
    assert_frame_equal(df, df_expect)

    data = {"price_vat": [0.5, 1, 4],
            "price_total": [1, 1.5, 5],
            }
    df = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df)
    df_expect["price_ex_vat"] = [0.5, 0.5, 1]
    assert_frame_equal(df, df_expect)

    data = {"price_vat": [0.5, 1, 4],
            "price_total": [1, 1.5, 5],
            }
    df = pd.DataFrame(data)
    df_expect = df.copy()
    df = enrich(df, disable_sums=True)
    assert_frame_equal(df, df_expect)


def internet_connection_ok(url, timeout=5):
    try:
        request = requests.get(url, timeout=timeout)
        res = request.ok
    except Exception:
        res = False
    return res


@pytest.mark.skipif(not internet_connection_ok("https://www.google.com/"),
                    reason="No internet access")
def test_getComp():
    bids = pd.Series(["1567535-0", "2403929-2", "ei_ole_olemassa"])
    df = getComp(bids, use_cache=False, search_website=False)
    df = df.loc[:, ["bid", "name", "search_word"]]
    data = {"bid": [None, "2403929-2", None],
            "name": [None, "Uros Oy", None],
            "search_word": ["1567535-0", "2403929-2", "ei_ole_olemassa"],
            }
    df_expect = pd.DataFrame(data)
    assert_frame_equal(df, df_expect)


# This test requires too much resources to be performed
@pytest.mark.skipif(not internet_connection_ok("https://www.google.com/"),
                    reason="No internet access")
def test_getMuniFin():
    codes = pd.Series(["0135202-4", "test"])
    years = pd.Series(["2021", "2020"])
    with pytest.warns(Warning):
        df = getMuniFin(codes, years, use_cache=False)
    df = df.loc[:, ["bid", "Lainakannan muutokset"]]
    data = {"bid": ["0135202-4"],
            "Lainakannan muutokset": [-286476.0],
            }
    df_expect = pd.DataFrame(data)
    assert_frame_equal(df, df_expect, check_names=False)


# This test requires too much resources to be performed
@pytest.mark.skipif(not internet_connection_ok("https://www.google.com/"),
                    reason="No internet access")
def test_getMuniComp():
    codes = pd.Series(["0204819-8"])
    years = pd.Series(["2021"])
    df = getMuniComp(codes, years)
    assert all(x in df["name"].tolist() for x in [
        "Arkea Oy", "Kaarea Oy", "Turun Vesihuolto Oy"])


@pytest.mark.skipif(not internet_connection_ok(
    "https://www.google.com/"), reason="No internet access")
def test_getMuni():
    codes = pd.Series(["005", "020"])
    years = pd.Series(["2021", "2020"])
    df = getMuni(codes, years)
    df = df.loc[:, ["code", "Population"]]
    df["Population"] = df["Population"].astype(float)
    data = {"code": ["005", "005", "020", "020"],
            "Population": [9419.0, 9311.0, 16391.0, 16467.0],
            }
    df_expect = pd.DataFrame(data)
    assert_frame_equal(df, df_expect)


def __create_dummy_data():
    data = {"org_name": ["test", "testi", "test"],
            "org_code": ["1", "2", "3"],
            }
    df = pd.DataFrame(data)
    return df

# -*- coding: utf-8 -*-
from osta.imports import searchData, getData, detectFields
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
import requests
import re
import copy


def test_imports_wrong_arguments():
    with pytest.raises(Exception):
        searchData(None)
    with pytest.raises(Exception):
        searchData(True)
    with pytest.raises(Exception):
        searchData(1)
    with pytest.raises(Exception):
        searchData(log_file=None)
    with pytest.raises(Exception):
        searchData(log_file=1)
    with pytest.raises(Exception):
        searchData(log_file=[True, False])
    with pytest.raises(Exception):
        searchData(verbose=None)
    with pytest.raises(Exception):
        searchData(verbose=1)
    with pytest.raises(Exception):
        searchData(verbose=[True, False])
    with pytest.raises(Exception):
        searchData(verbose="test")
    with pytest.raises(Exception):
        getData()
    with pytest.raises(Exception):
        getData(None)
    with pytest.raises(Exception):
        getData(True)
    with pytest.raises(Exception):
        getData(1)
    with pytest.warns(Warning):
        getData([1, True])
    with pytest.raises(Exception):
        getData(["test", "test"], as_df=None)
    with pytest.raises(Exception):
        getData(["test", "test"], as_df=1)
    with pytest.raises(Exception):
        getData(["test", "test"], as_df="test")
    with pytest.raises(Exception):
        getData(["test", "test"], as_df=[True, False])
    with pytest.raises(Exception):
        getData(["test", "test"], log_file=None)
    with pytest.raises(Exception):
        getData(["test", "test"], log_file=1)
    with pytest.raises(Exception):
        getData(["test", "test"], log_file=[True, False])

    def internet_connection_ok(url, timeout=5):
        try:
            request = requests.get(url, timeout=timeout)
            res = request.ok
        except Exception:
            res = False
        return res

    @pytest.mark.skipif(not internet_connection_ok("https://www.google.com/"),
                        reason="No internet access")
    def test_imports():
        # Test that URL addresses are fetched
        res = searchData("kaarina ostolasku")
        assert isinstance(res, pd.DataFrame)
        assert res.shape[0] > 0 and res.shape[1] > 0
        url = res.loc[1, "url"]
        assert re.match("https", url)

        # Read the file --> test that it can be read and it contains "Kaarina"
        if re.match("csv", url):
            df = pd.read_csv(url)
        else:
            df = pd.read_excel(url)
        assert df.isin("Kaarina")


# detectFields


def test_check_names_wrong_arguments():
    df = __create_dummy_data()
    with pytest.raises(Exception):
        df = detectFields()
    with pytest.raises(Exception):
        df = detectFields(pd.DataFrame())
    with pytest.raises(Exception):
        df = detectFields(None)
    with pytest.raises(Exception):
        df = detectFields(1)
    with pytest.raises(Exception):
        df = detectFields(True)
    with pytest.raises(Exception):
        df = detectFields("yes")
    with pytest.raises(Exception):
        df = detectFields(df, guess_names=1)
    with pytest.raises(Exception):
        df = detectFields(df, guess_names="yes")
    with pytest.raises(Exception):
        df = detectFields(df, guess_names=None)
    with pytest.raises(Exception):
        df = detectFields(df, make_unique=1)
    with pytest.raises(Exception):
        df = detectFields(df, make_unique="yes")
    with pytest.raises(Exception):
        df = detectFields(df, make_unique=None)
    with pytest.raises(Exception):
        df = detectFields(df, fields=1)
    with pytest.raises(Exception):
        df = detectFields(df, fields=df)
    with pytest.raises(Exception):
        df = detectFields(df, fields="dict")
    with pytest.raises(Exception):
        df = detectFields(df, fields=True)
    with pytest.raises(Exception):
        df = detectFields(df, pattern_th=None)
    with pytest.raises(Exception):
        df = detectFields(df, pattern_th=2)
    with pytest.raises(Exception):
        df = detectFields(df, pattern_th=True)
    with pytest.raises(Exception):
        df = detectFields(df, pattern_th="0.1")
    with pytest.raises(Exception):
        df = detectFields(df, pattern_th=-0.5)
    with pytest.raises(Exception):
        df = detectFields(df, scorer=None)
    with pytest.raises(Exception):
        df = detectFields(df, scorer=1)
    with pytest.raises(Exception):
        df = detectFields(df, scorer="None")
    with pytest.raises(Exception):
        df = detectFields(df, scorer=True)
    with pytest.raises(Exception):
        df = detectFields(df, match_th=2)
    with pytest.raises(Exception):
        df = detectFields(df, match_th="0.1")
    with pytest.raises(Exception):
        df = detectFields(df, match_th=2)
    with pytest.raises(Exception):
        df = detectFields(df, match_th=-0.1)
    with pytest.raises(Exception):
        df = detectFields(df, match_th=None)
    with pytest.raises(Exception):
        df = detectFields(df, match_th=True)


def test_detectFields_all_wrong():
    df = __create_dummy_data()
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_some_wrong():
    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan nimi", "org_code", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "Test3"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_specify_fields():
    df = __create_dummy_data()
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    own_field = dict([("test1", "suppl_name"),
                      ("test2", "testinimi"),
                      ("test3", "doc_id")])
    # Do not expect a warning
    df = detectFields(df, fields=own_field)
    # Expected names
    df_ref.columns = ["suppl_name", "testinimi", "doc_id"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    df = __create_dummy_data()
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Create own fields as a DF
    own_field = pd.DataFrame({"key": ["Test1", "Test2", "Test3"],
                              "value": ["price_total", "doc_date",
                                        "org_name"]})
    # Do not expect a warning
    df = detectFields(df, fields=own_field)
    # Expected names
    df_ref.columns = ["price_total", "doc_date", "org_name"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_duplicated_names():
    df = __create_dummy_data()
    # Original names
    df.columns = ["doc_date", "Test2", "doc_date"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["doc_date", "doc_id", "doc_date_2"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["doc_date", "Test2", "doc_date"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, make_unique=False)
    # Expected names
    df_ref.columns = ["doc_date", "doc_id", "doc_date"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_guess_names():
    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Summa."]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "price_total"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Summa."]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, guess_names=False)
    # Expected names
    df_ref.columns = ["Kunnan_nimi", "Kunta numero", "Summa."]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_pattern_th():
    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, pattern_th=1)
    # Expected names
    df_ref.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, pattern_th=0.6)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "price_total"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_test_sums():
    data = {"test1": [10.0, 12.0, 13.5],
            "test2": [1.5, 2.5, 3.0],
            "test3": [8.5, 9.5, 10.5]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["price_total", "price_vat", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["price_total", "price_vat", "price_ex_vat"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["price_total", "test2", "price_ex_vat"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["price_total", "price_vat", "price_ex_vat"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["test1", "price_vat", "price_ex_vat"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    print(df)
    print(df_ref)
    df_ref.columns = ["price_total", "price_vat", "price_ex_vat"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_data_patterns():
    # matching land code, date, and doc_id
    data = {"test1": ["FI", "FI", "DK", "FI"],
            "test2": ["02/01/2023", "2-1-2023", "20.12.2023", "20.1.2023"],
            "test3": [1, 2, 2, 3]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["suppl_land", "doc_date", "doc_id"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_data_patterns2():
    data = {"test1": [10, 10, 10],
            "test2": ["test", "test", "test"],
            "test3": ["0000000-0", "0000000-0", "0000000-0"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "org_name", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["org_code", "org_name", "org_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["org_code", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["org_code", "org_name", "org_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "org_bid"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["org_code", "org_name", "org_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    data = {"test1": [10, 10, 10],
            "test2": ["test1", "test2", "test3"],
            "test3": ["2001160-4", "2403929-2", "0100006-9"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "suppl_bid"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["Test1", "suppl_name", "suppl_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "suppl_name", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["Test1", "suppl_name", "suppl_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_match_th():
    data = {"test1": [2191, 2191, 3710],
            "test2": [2282, 2251, 2191],
            "test3": ["test", "test", "test"],
            "test4": ["Henkilökohtainen apu", "test", "vammaisten perhehoito"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3", "Test4"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.67)
    # Expected names
    df_ref.columns = ["Test1", "service_code", "Test3", "Test4"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3", "Test4"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.65)
    # Expected names
    df_ref.columns = ["service_code", "service_code_2",
                      "Test3", "service_name"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_match_th1():
    data = {"test1": [3710, 3005, "test"],
            "test2": [3710, 3005, 3710],
            "test3": ["test", "test", "test"],
            "test4": ["myyntituotot", "test", "palkkatuki"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3", "Test4"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.67)
    # Expected names
    df_ref.columns = ["Test1", "account_code", "Test3", "Test4"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3", "Test4"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.65, make_unique=False)
    # Expected names
    df_ref.columns = ["account_code", "account_code",
                      "Test3", "account_name"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_match_th2():
    data = {"test1": [10, 12, 10],
            "test2": ["test1", "test2", "test3"],
            "test3": ["0204819-8", "0133226-9", "test"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.67)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "bid"]
    # Expect that are equal (if there are any BIDs, it is probable that column
    # includes BID values... --> match_th does not affect)
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.65)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "org_bid"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, pattern_th=0.6)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "price_total"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_match_th3():
    data = {"test1": [10, 12, 10],
            "test2": ["test1", "test2", "test3"],
            "test3": ["FI", "FI", "test"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.67)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "Test3"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.65)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "suppl_land"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, pattern_th=0.6)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "price_total"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def test_detectFields_match_th4():
    data = {"test1": ["FI00009578", "BE4448596870", "test"],
            "test2": ["test1", "test2", "test3"],
            "test3": ["FI", "FI", "test"]
            }
    df = pd.DataFrame(data)
    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.67)
    # Expected names
    df_ref.columns = ["Test1", "Test2", "Test3"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    # Original names
    df.columns = ["Test1", "Test2", "Test3"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, match_th=0.65)
    # Expected names
    df_ref.columns = ["suppl_vat_number", "Test2", "suppl_land"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)

    df = __create_dummy_data()
    # Original names
    df.columns = ["Kunnan_nimi", "Kunta numero", "Kokko.summa"]
    df_ref = copy.copy(df)
    # Expect a warning
    with pytest.warns(Warning):
        df = detectFields(df, pattern_th=0.6)
    # Expected names
    df_ref.columns = ["org_name", "org_code", "price_total"]
    # Expect that are equal
    assert_frame_equal(df, df_ref)


def __create_dummy_data():
    data = {"test1": ["test", "testi", "test"],
            "test2": [1, 2, 3],
            "test3": [True, False, False]
            }
    df = pd.DataFrame(data)
    return df

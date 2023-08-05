
import datetime
import json
from urllib.parse import urljoin

import pandas as pd
import requests


def build_url(path: str) -> str:
    base_url = "https://api.jquants.com/"
    return urljoin(base_url, path)


def fetch_login_token(refresh_token: str) -> str:
    """ J-Quantsからlogin_tokenを取得する
    """
    try:
        url = build_url(f"/v1/token/auth_refresh?refreshtoken={refresh_token}")
        r_post = requests.post(url, timeout=30)
        if r_post.status_code != 200:
            raise RuntimeError()
        token_dict = r_post.json()
        login_token = str(token_dict["idToken"])
        return login_token
    except Exception:
        raise RuntimeError("Failed to fetch login token.")


def fetch_refresh_token(username: str, password: str) -> str:
    """ J-Quantsからrefresh_tokenを取得する
    """
    try:
        data = {
            "mailaddress": username,
            "password": password,
        }
        url = build_url("/v1/token/auth_user")
        r_post = requests.post(url, data=json.dumps(data), timeout=30)
        if r_post.status_code != 200:
            raise RuntimeError()
        token_dict = r_post.json()
        refresh_token = str(token_dict["refreshToken"])
        return refresh_token
    except Exception:
        raise RuntimeError("Failed to fetch refresh token.")


def download_brand(login_token:str) -> pd.DataFrame:
    """ 利用可能な銘柄コード一覧を取得する

    Args:
        login_token(str): 認証トークン

    Returns:
        list of str: 取得した
    """
    try:
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url("/v1/listed/info")
        r = requests.get(url, headers=headers, timeout=10)
        result_dict = r.json()
    except Exception:
        raise RuntimeError("Failed to code list.")

    # 取得結果をパース
    rows = result_dict["info"]
    df = pd.DataFrame(rows)
    return df


def download_stock(login_token: str, code:str) -> pd.DataFrame:
    try:
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url(f"/v1/prices/daily_quotes?code={code}")
        r = requests.get(url, headers=headers, timeout=30)
        result_dict = r.json()

        record_ls = result_dict["daily_quotes"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Failed fetch stock information.")


def donwload_daily_stock(login_token :str, date: datetime.date) -> pd.DataFrame:
    try:
        date_str = date.strftime("%Y-%m-%d")
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url(f"/v1/prices/daily_quotes?date={date_str}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["daily_quotes"]
        if len(record_ls) == 0:
            raise RuntimeError("Success to fetch, but records are blank.")
        df = pd.DataFrame(record_ls)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df[df["Date"].dt.date == date]
        return df
    except Exception as e:
        raise e


def download_topix(login_token: str) -> pd.DataFrame:
    """ TOPIXの情報の取得
    """
    try:
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url("/v1/indices/topix")
        r = requests.get(url, headers=headers)
        result_dict = r.json()
        record_ls = result_dict["topix"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Faile to fetch topix information.")


def download_statements(login_token :str, code :str) -> pd.DataFrame:
    """ 財務情報の取得
    """
    try:
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url(f"/v1/fins/statements?code={code}")
        r = requests.get(url, headers=headers)
        result_dict = r.json()
        record_ls = result_dict["statements"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Failed to fetch statemnets information.")


def donwload_daily_statements(login_token :str, date: datetime.date) -> pd.DataFrame:
    try:
        date_str = date.strftime("%Y-%m-%d")
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url(f"/v1/fins/statements?date={date_str}")
        r = requests.get(url, headers=headers, timeout=30)

        result_dict = r.json()
        record_ls = result_dict["statements"]
        df = pd.DataFrame(record_ls)
        if len(df) == 0:
            return None
        df["DisclosedDate"] = pd.to_datetime(df["DisclosedDate"])
        df = df[df["DisclosedDate"].dt.date == date]
        return df
    except Exception as e:
        raise e


def download_market(login_token :str) -> pd.DataFrame:
    try:
        headers = {'Authorization': 'Bearer {}'.format(login_token)}
        url = build_url("/v1/markets/trades_spec")
        r = requests.get(url, headers=headers)
        record_dict = r.json()
        record_ls = record_dict["trades_spec"]
        df = pd.DataFrame(record_ls)
        return df
    except Exception:
        raise RuntimeError("Faile to fetch market information.")

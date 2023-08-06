from datetime import datetime
import asyncio
import aiohttp
import pandas as pd
import numpy as np
import requests
import io

import codal_tsetmc.config as db
from codal_tsetmc.models import Stocks


def get_stock_dividend_history(code: str) -> pd.DataFrame:
    """Get stock dividend from the web.

    params:
    ----------------
    code: str
        code -> symbol
        http://www.tsetmc.com/tsev2/data/DPSData.aspx?s=فولاد
        string after s=

    return:
    ----------------
    pd.DataFrame
        dtyyyymmdd: str
        dividend: float

    example
    ----------------
    df = get_stock_dividend_history('44891482026867833')
    """
    symbol = Stocks.query.filter_by(code=code).first().name
    url = f"http://www.tsetmc.com/tsev2/data/DPSData.aspx?s={symbol}"
    r = requests.get(url).content.decode("utf-8").replace(";", "\n").replace("@", ",")
    df = (
        pd.read_csv(io.StringIO(r), header=None)[[1, 2, 6]]
        .replace(r'^\s*$', np.nan, regex=True)
        .dropna().drop_duplicates()
    )
    df.columns = ["jdate", "fiscal_year", "dividend"]
    df = df[~df["dividend"].isin(["0", "0.00", 0])]
    df["jdate"] = df.jdate.jalali.parse_jalali("%Y/%m/%d")
    df["fiscal_year"] = df.fiscal_year.jalali.parse_jalali("%Y/%m/%d")
    df["dtyyyymmdd"] = (
        df.jdate.jalali.to_gregorian()
        .apply(lambda x: x.strftime("%Y%m%d"))
    )

    return df


async def update_stock_dividend(code: str):
    """
    Update (or download for the first time) Stock dividend


    params:
    ----------------
    code: str or intege

    example
    ----------------
    `update_stock_dividend('44891482026867833') #Done`
    """
    try:
        now = datetime.now().strftime("%Y%m%d")
        try:
            max_date_query = (
                f"select max(dtyyyymmdd) as date from stock_dividend where code = '{code}'"
            )
            max_date = pd.read_sql(max_date_query, db.engine)
            last_date = max_date.date.iat[0]
        except Exception as e:
            last_date = None
        try:
            # need to updata new dividend data
            if last_date is None or str(last_date) < now:
                symbol = Stocks.query.filter_by(code=code).first().name
                url = f"http://www.tsetmc.com/tsev2/data/DPSData.aspx?s={symbol}"
            else:  # The dividend data for this code is updateed
                return
        except Exception as e:
            print(f"Error on formating dividend:{str(e)}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.text()

        data = data.replace(";", "\n").replace("@", ",")
        df = (
            pd.read_csv(io.StringIO(data), header=None)[[1, 6]]
            .replace(r'^\s*$', np.nan, regex=True)
            .dropna().drop_duplicates()
        )
        df.columns = ["dtyyyymmdd", "dividend"]
        df["dividend"] = df["dividend"].astype(float)
        df = df[~(df["dividend"] == 0)]
        df["dtyyyymmdd"] = (
            df.dtyyyymmdd
            .jalali.parse_jalali("%Y/%m/%d")
            .jalali.to_gregorian()
            .apply(lambda x: x.strftime("%Y%m%d"))
            .astype(int)
        )
        df["code"] = code
        try:
            q = f"select dtyyyymmdd from stock_dividend where code = '{code}'"
            temp = pd.read_sql(q, db.engine)
            df = df[~df.dtyyyymmdd.isin(temp.dtyyyymmdd)]
        except:
            pass

        df.to_sql(
            "stock_dividend",
            db.engine,
            if_exists="append",
            index=False
        )
        return True, code

    except Exception as e:
        return e, code


def update_group_dividend(code):
    """
    Update and download data of all stocks in a group.

    `Warning: Stock table should be updated`
    """
    stocks = db.session.query(Stocks.code).filter_by(group_code=code).all()
    print("updating group", code, end="\r")
    loop = asyncio.get_event_loop()
    tasks = [update_stock_dividend(stock[0]) for stock in stocks]
    try:
        results = loop.run_until_complete(asyncio.gather(*tasks))
    except RuntimeError:
        WARNING_COLOR = "\033[93m"
        ENDING_COLOR = "\033[0m"
        print(WARNING_COLOR, "Please update stock table", ENDING_COLOR)
        print(
            f"{WARNING_COLOR}If you are using jupyter notebook, please run following command:{ENDING_COLOR}"
        )
        print("```")
        print("%pip install nest_asyncio")
        print("import nest_asyncio; nest_asyncio.apply()")
        print("from tehran_stocks.download import get_all_dividend")
        print("get_all_dividend()")
        print("```")
        raise RuntimeError

    print("group", code, "updated", end="\r")
    return results


def get_all_dividend():
    codes = db.session.query(db.distinct(Stocks.group_code)).all()
    for i, code in enumerate(codes):
        print(
            f"{' '*18} total progress: {100*(i+1)/len(codes):.2f}%",
            end="\r",
        )
        update_group_dividend(code[0])

    print("Dividend Download Finished.", " "*20)

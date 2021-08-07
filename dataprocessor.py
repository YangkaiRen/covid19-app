#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import pymysql
from datetime import datetime,timedelta
from sqlalchemy import create_engine
from configparser import ConfigParser

BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'

def get_config(filename='db.ini', section='rds'):
    '''
    read and parse the database.conf file, return postgresql connector parameters.
    '''
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        return {k: int(v) if k == 'port' else v for k, v in parser.items(section)}
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))


def get_engine(db_conf):
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(db_conf['user'],db_conf['password'],db_conf['host'],db_conf['port'],db_conf['database']))
    return engine

def fetch_daily_dateframe(db_conf,before_days=1):
    dt = datetime.now()-timedelta(days=before_days)
    report_date = dt.strftime('%Y-%m-%d')
    with pymysql.connect(**db_conf) as conn:
        cur = conn.cursor()
        cur.execute("select count(*) from covid19_us where report_date='{}'".format(report_date))
        cnt = cur.fetchall()[0][0]
        if cnt > 0:
            print("{} data had existed".format(report_date))
            return
    try:
        url = BASE_URL.format(dt.strftime('%m-%d-%Y'))
        df = pd.read_csv(url)
        df['report_date'] = report_date
        df2 = df[['Province_State','Lat','Long_','Confirmed','Deaths','report_date']]
        df2.columns = ['province_state','lat','lon','confirmed','deaths','report_date']
        print("inserting into {} data".format(report_date))
        df2.to_sql(name='covid19_us', con=get_engine(db_conf), if_exists='append',index=False)
    except Exception as e:
        print(e)

def init_history_data(dir,db_conf):
    files = os.listdir(dir)
    dfs = []
    for file in files:
        if file.endswith('.csv'):
            report_date = datetime.strptime(file.strip('.csv'),'%m-%d-%Y').strftime('%Y-%m-%d')
            df = pd.read_csv(os.path.join(dir,file))
            df['report_date'] = report_date
            df2 = df[['Province_State','Lat','Long_','Confirmed','Deaths','report_date']]
            df2.columns = ['province_state','lat','lon','confirmed','deaths','report_date']
            dfs.append(df2)
    df2 = pd.concat(dfs,ignore_index=True)
    df2.to_sql(name='covid19_us', con=get_engine(db_conf), if_exists='append',index=False)

    




if __name__ == '__main__':
    db_conf = get_config()
    # df = init_history_data('./')
    fetch_daily_dateframe(db_conf)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
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
#{'host': 'database-1.cpj3j49dqd6l.us-east-2.rds.amazonaws.com',
# 'port': 3306, 'database': 'covid19', 'user': 'admin',
# 'password': 'cicd2021'}
def get_engine(db):
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(db['user'],db['password'],db['host'],db['port'],db['database']))
    return engine

def fetch_daily_dateframe(dt=datetime.now()-timedelta(days=1)):
    url = BASE_URL.format(dt.strftime('%m-%d-%Y'))  #get url of new updat data
    df = pd.read_csv(url)
    df['report_date'] = dt.strftime('%Y-%m-%d')
    df2 = df[['Province_State','Lat','Long_','Confirmed','Deaths','report_date']]
    df2.columns = ['province_state','lat','lon','confirmed','deaths','report_date']
    return df2


def init_history_data(dir):
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
    return pd.concat(dfs, ignore_index=True)
    




if __name__ == '__main__':
    engine = get_engine(get_config())
    # df = init_history_data('./')
    df = fetch_daily_dateframe()
    df.to_sql(name='covid19_us',con=engine,if_exists='append',index=False)
    # print(engine)
    # # print(df)
    # dt = datetime.now() - timedelta(days=1)
    # print(dt)
    # url = BASE_URL.format(dt.strftime('%m-%d-%Y'))
    # print(url)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import pymysql
from dataprocessor import get_config

class TestCovidData(unittest.TestCase):

    def test_conn_rds(self):
        db_conf = get_config()
        with pymysql.connect(**db_conf) as conn:
            self.assertEqual(conn.get_host_info(),'socket database-1.cpj3j49dqd6l.us-east-2.rds.amazonaws.com:3306')


    def test_data_ready(self):
        db_conf = get_config()
        with pymysql.connect(**db_conf) as conn:
            cur = conn.cursor()
            cur.execute('select count(*) from covid19_us')
            self.assertGreater(cur.fetchall()[0][0],0)


if __name__ == '__main__':
    unittest.main()

        


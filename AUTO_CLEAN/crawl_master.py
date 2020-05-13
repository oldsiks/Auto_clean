import re
import time

import pymysql
import requests
from db_info import get_cik
from crawl_poc import download_masterindex
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)


yearstar = 1993
yearend = 2018

cik_range = get_cik()
form_f_range = ['20-F', '20-F/A', '40-F', '40-F/A' ]
form_range = ['10-K', '10-K/A', '10-KT', '10-KT/A', '10-K405', '10-K405/A', '10KT405', '10KT405/A', '10KSB', '10KSB/A', '10-KSB','10-KSB/A', '10KSB40', '10KSB40/A', '10-Q', '10-Q/A', '10-QT', '10-QT/A', '10QSB', '10QSB/A', '10-QSB']
def crawl_cik(yearstar, yearend):
    path_list = []
    for year in range(yearstar, yearend+1):
        for qrt in ['1', '2', '3', '4']:
            masterindex = download_masterindex(year, qrt)
            if masterindex:
                for item in masterindex:
                    if item.cik in cik_range and item.form in form_f_range:
                        value = (item.cik, item.path, year, qrt, item.form, item.filingdate)
                        path_list.append(value)
            print('{}年{}季度已爬去完毕'.format(year, qrt))
        print('{}年已爬去完毕'.format(year))
    return path_list

def save_path(path_list):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    sql_select = "insert into f_master(cik, path, Myear, Mqtr, Mtype, filingdate)value(%s, %s, %s, %s, %s, %s)"
    n = 0
    for i in path_list:
        cursor.execute(sql_select, i)
        db.commit()
        n += 1
        print(f'已经保存第{n}条数据， value ：{i}')
    db.close()



if __name__ == '__main__':
    path_list = crawl_cik(yearstar, yearend)
    save_path(path_list)

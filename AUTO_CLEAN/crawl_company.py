

import pymysql
from EDGAR_DownloadCompanyInfo import grab_company
from db_info import get_loaded, create_info_db


def get_uni(table_name):
    """
    获取mysql中的数据
    :param new_table: 目标表名。
    :return sql_data: 要查询的数据的 unique_key。
    """
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    sql = f"select FILINGDATE, UNIQUE_KEY from {table_name} where UNIQUE_KEY!=''"
    cursor.execute(sql)
    sql_data = set(cursor.fetchall())
    return sql_data

if __name__ == '__main__':
    com_form = 'company_info_ipo'
    source_form = 'file_thread_424B'

    create_info_db(com_form)
    loaded = get_loaded(com_form)
    uni_list = get_uni(source_form)

    company_set = set()
    cik_file = {}

    for i in uni_list:
        f_date = i[0].replace('-', '')
        cik, uni = i[1].split('_')
        if cik not in cik_file.keys():
            cik_file[cik] = f_date + '_' + i[1]
        else:
            if int(f_date) > int(cik_file[cik].split('_')[0]):
                cik_file[cik] = f_date + '_' + i[1]

    dsb = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = dsb.cursor()
    sql = f'insert into {com_form}(CIK, COMPANYNAME, INDUSTRY_TITLE, SIC, IRS_NO, STATE, ADDRESS_BUSINESS, ADDRESS_MAILING)value(%s, %s, %s, %s, %s, %s, %s, %s)'
    for j in cik_file.values():
        filing_data, cik, uni = j.split('_')
        if cik not in loaded:
            company = grab_company(cik, uni, dsb)
            cursor.execute(sql, company)
            dsb.commit()
    dsb.close()
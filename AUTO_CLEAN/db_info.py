
import pymysql

def save_info(com_file, new_table):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    sql = f'insert into {new_table}(CIK, SEC_LINK, FILINGDATE, PERIOD, DOCUMENTS, ACCEPTED, FILE_TYPE, FISCAL_YEAR_END, FISCAL_PERIOD, FILE_NO, FILM_NO, DOCUMENT, SEC_LINK_HASH, DESCRIPTION, ETYPE, ESIZE, TICKER, UNIQUE_KEY)value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        cursor.execute(sql, com_file)
        db.commit()
    except:
        db.rollback()

def check_exist(UNIQUE_KEY, new_table):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    check_sql = rf"select * from {new_table} where UNIQUE_KEY='{UNIQUE_KEY}'"
    cursor.execute(check_sql)
    length = len(cursor.fetchall())
    return length

def save_company(values, aim_table):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    sql = f'insert into {aim_table}(CIK, COMPANYNAME, INDUSTRY_TITLE, SIC, IRS_NO, STATE, ADDRESS_BUSINESS, ADDRESS_MAILING)value(%s, %s, %s, %s, %s, %s, %s, %s)'
    for value in values:

        cursor.execute(sql, value)
        db.commit()

    db.close()
def create_info_db(com_form):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    # sql_if = "DROP TABLE IF EXISTS `EDGAR_INFO`;"
    sql_create = f"CREATE TABLE if not exists {com_form}( `CIK` varchar(15) not NULL, `COMPANYNAME` varchar(100) default NULL,`SIC` char(15) DEFAULT NULL,`INDUSTRY_TITLE` varchar(50) DEFAULT NULL, `IRS_NO` varchar(20) DEFAULT NULL,`STATE` varchar(20) DEFAULT NULL,`ADDRESS_BUSINESS` varchar(200) DEFAULT NULL,`ADDRESS_MAILING` varchar(200) DEFAULT NULL, primary key (cik)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    # cursor.execute(sql_if)
    cursor.execute(sql_create)
    db.commit()
    db.close()

def get_loaded(company_form):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()
    sql = f'select cik from {company_form}'
    cursor.execute(sql)
    ciks = [i[0] for i in cursor.fetchall()]
    db.close()
    return ciks

def get_cik():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='a123456', db='edgar', charset='utf8')
    cursor = db.cursor()

    sql_select = "select CIK from cik_sheet limit 22000, 8000"  #
    cursor.execute(sql_select)
    ciks = cursor.fetchall()
    cik_list = []
    for i in ciks:
        cik_list.append(str(i[0]))

    return cik_list

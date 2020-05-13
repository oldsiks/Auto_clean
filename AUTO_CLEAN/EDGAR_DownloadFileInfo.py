import re
import time
import requests
from lxml import etree
import logging
from fake_useragent import UserAgent
from EDGAR_DownloadCompanyInfo import grab_company
from db_info import save_info, check_exist
logging.captureWarnings(True)
ua = UserAgent(use_cache_server=False)
PARM_EDGARPREFIX = 'https://www.sec.gov'


def request_step1(CIK, UNI, new_table):
    # company_info = grab_company(CIK, UNI)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        'Host': 'www.sec.gov',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random
    }
    url = f'https://www.sec.gov/Archives/edgar/data/{CIK}/{UNI}-index.htm'
    resp = requests.get(url=url, headers=headers, verify=False)
    html = etree.HTML(resp.text)
    FILE_TYPE = html.xpath('//div[@id="formName"]/strong/text()')[0][5:]
    EDATE = html.xpath('//div[@class="formContent"]/div[@class="formGrouping"]/div[@class="info"]/text()')[0]
    if html.xpath(r'//div[@class="formGrouping"]/div[contains(text(),"Period of Report")]/text()') != []:
        PERIOD = html.xpath(r'//div[contains(text(),"Period of Report")]/../div[2]/text()')[0]
    else:
        PERIOD = ''
    SEC_LINK = url
    DOCUMENTS = html.xpath('//div[@class="formContent"]/div[@class="formGrouping"]/div[@class="info"]/text()')[2]
    ACCEPTED = html.xpath('//div[@class="formContent"]/div[@class="formGrouping"]/div[@class="info"]/text()')[1]
    if ' | Fiscal Year End: ' in html.xpath(r'//*[@id="filerDiv"]/div[@class="companyInfo"]/p/text()'):
        FISCAL_YEAR_END = re.findall(r'Fiscal Year End: <strong>(.*?)</strong>', resp.content.decode('utf8'))[0]
    else:
        FISCAL_YEAR_END = ''
    if ' | Film No.: ' in html.xpath(r'//*[@id="filerDiv"]/div[@class="companyInfo"]/p/text()'):
        FILM_NO = re.findall(r'Film No.: <strong>(.*?)</strong>', resp.content.decode('utf8'))[0]
    else:
        FILM_NO = ''
    if ' | File No.: ' in html.xpath(r'//*[@id="filerDiv"]/div[@class="companyInfo"]/p/text()'):
        FILE_NO = re.findall(r'File No.: <a href=.*?<strong>(.*?)</strong>', resp.content.decode('utf8'))[0]
    else:
        FILE_NO = ''
    n = 1
    while True:
        if html.xpath('//table[@class="tableFile"]/@summary')[0] == 'Document Format Files':
            n += 1
            if html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[3]/a/text()') != []:
                SEC_LINK_HASH = PARM_EDGARPREFIX + \
                                html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[3]/a/@href')[0]
                DOCUMENT = html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[3]/a/text()')[0]
            else:
                SEC_LINK_HASH = ''
                DOCUMENT = ''

            if html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[2]/text()') != []:
                DESCRIPTION = str(
                    html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[2]/text()')[0]).lower()
            else:
                DESCRIPTION = ''

            if html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[4]/text()') != []:
                ETYPE = html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[4]/text()')[0]
            else:
                ETYPE = ''
            if html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[5]/text()') != []:
                ESIZE = html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[5]/text()')[0]
            else:
                ESIZE = ''
            if DESCRIPTION == 'Complete submission text file'.lower():
                UNIQUE_KEY = CIK + '_' + DOCUMENT[0: -4]
                TICKER = '1'
            else:
                UNIQUE_KEY = ''
                TICKER = '0'
            if PERIOD != '':
                FISCAL_PERIOD = PERIOD.split('-')[0] + '-' + FISCAL_YEAR_END[0:2] + '-' + FISCAL_YEAR_END[2:]
            else:
                FISCAL_PERIOD = ''
            if html.xpath(f'//table[@summary="Document Format Files"]/tr[{n}]/td[3]/a/@href') == [] and html.xpath(
                    f'//table[@summary="Document Format Files"]/tr[{n}]/td[2]/text()') == []:
                break
            file_info = [CIK, SEC_LINK, EDATE, PERIOD, DOCUMENTS, ACCEPTED, FILE_TYPE, FISCAL_YEAR_END, FISCAL_PERIOD, FILE_NO, FILM_NO, DOCUMENT, SEC_LINK_HASH, DESCRIPTION, ETYPE, ESIZE, TICKER, UNIQUE_KEY]
            com_file = file_info


            len_sear = check_exist(UNIQUE_KEY, new_table)
            if DESCRIPTION == 'Complete submission text file'.lower():
                if len_sear == 0:
                    save_info(com_file, new_table)
                    print(f'UNIQUE_KEY:{UNIQUE_KEY} 已储存。type：{FILE_TYPE}')
                else:
                    print('数据库中已存在该数据，unique_key:', UNIQUE_KEY, 'CIK:', CIK)
                    print('FILE_TYPE:', FILE_TYPE)
        else:
            with open('file_info_erro.txt', 'a') as f:
                f.write(f'cik: {CIK}, uni: {UNI}\n')
            break

def entrance(CIK, UNI, new_table):
    # try:
        request_step1(CIK, UNI, new_table)
    # except BaseException as e:
    #     with open('erro_catch.txt', 'a', encoding='utf8') as erf:
    #         erf.write(f'{time.strftime("%Y-%m-%d %X")}:{CIK}{e}\n')


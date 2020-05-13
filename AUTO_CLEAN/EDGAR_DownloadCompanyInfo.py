import logging
import time
import requests
import re
from lxml import etree
from fake_useragent import UserAgent

logging.captureWarnings(True)
ua = UserAgent(use_cache_server=False)
star_time = time.time()
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}

def grab_company(CIK, UNI, dsb):


    time.sleep(1)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'www.sec.gov',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random
    }
    n = 0
    url = f'https://www.sec.gov/Archives/edgar/data/{CIK}/{UNI}-index.htm'
    n += 100
    if (time.time() - star_time) % 3600 > 1800:
        resp = requests.get(url=url, headers=headers, verify=False).text
    else:
        print("代理ip开始抓...")
        resp = requests.get(url=url, headers=headers, proxies=proxies, verify=False).text
    text_list = resp.split('\n')
    index = 0
    while index < len(text_list):
        con_line = text_list[index]
        if '<div id="filerDiv">' in con_line:
            for i in range(index + 1, len(text_list)):
                endline = text_list[i]
                if '<div id="filerDiv">' in endline or i == len(text_list) - 1:
                    info = text_list[index:i + 1]
                    for line in info:
                        if CIK in line:
                            INFO = ' '.join(info)
        index += 1
    html2 = etree.HTML(resp)
    COMPANYNAME = re.findall(r'<span class="companyName">(.*?)<acronym', INFO)[0].strip()[:-7].replace('&amp', '')
    if  'SIC' in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../p/acronym/text()'):
        SIC = re.findall(r'<acronym title="Standard Industrial Code">SIC</acronym>: <b><a href=".*?">(.*?)</a>', INFO)[0].strip().replace('&amp', '')
    else:
        SIC = ''
    if 'SIC' in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../p/acronym/text()') and re.findall(r'<acronym title="Standard Industrial Code">SIC</acronym>.*?</b>(.*?)<br />', INFO) != []:
        INDUSTRY_TITLE = re.findall(r'<acronym title="Standard Industrial Code">SIC</acronym>.*?</b>(.*?)<br />', INFO)[0].strip().replace('&amp', '')
    else:
        INDUSTRY_TITLE = ''
    if 'IRS No.' in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../p/acronym/text()'):
        IRS_NO = re.findall('IRS No.</acronym>: <strong>(.*?)</strong>', INFO)[0].strip().replace('&amp', '')
        # print(IRS_NO)
    else:
        IRS_NO = ''
        # print('*******************',IRS_NO)
    if [i for i in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../p/text()') if 'State of Incorp' in i] != []:
        STATE = re.findall(r'State of Incorp.*?<strong>(.*?)</strong>', INFO)[0].strip().replace('&amp', '')
    else:
        STATE = ''

    if html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../../div[@class="mailer"][2]/span/text()') != []:
        ADDRESS_BUSINESS = ', '.join([i.strip() for i in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../../div[@class="mailer"][2]/span/text()')]).replace('&amp', '')
    else:
        ADDRESS_BUSINESS = ''
    if html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../../div[@class="mailer"][1]/span/text()') != []:
        ADDRESS_MAILING = ', '.join([i.strip() for i in html2.xpath(f'//*[@id="filerDiv"]/div/span/a[contains(text(),"{CIK}")]/../../../div[@class="mailer"][1]/span/text()')]).replace('&amp', '')
    else:
        ADDRESS_MAILING = ''
    company_info = (CIK, COMPANYNAME, INDUSTRY_TITLE, SIC, IRS_NO, STATE, ADDRESS_BUSINESS, ADDRESS_MAILING)

    print('company_info:', company_info)
    return company_info



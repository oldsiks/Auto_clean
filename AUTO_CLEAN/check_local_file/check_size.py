
import os
import requests
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)
path = r'F:\replenish_10-QK'

def params_loaded(staryear, endyear):
    all_file = set()
    for year in range(staryear, endyear + 1):
        for qtr in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
            for i in os.walk(path + r'\{}\{}'.format(year, qtr)):
                for j in i[2]:
                    all_file.add(j)
                    size = os.path.getsize(os.path.join(i[0], j))
                    if size == 0:
                        print(j, year, qtr)
                        headers = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            # 'Connection': 'keep-alive',
                            'Host': 'www.sec.gov',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': ua.random
                        }
                        url = 'https://www.sec.gov/Archives/edgar' + '/'.join(j.split('edgar')[1].split('_')[0:-1]) + '.txt'

                        response = requests.get(url=url, headers=headers).content.decode('utf8')
                        if not os.path.exists(path + r'\{year}\{qtr}'.format(year=year, qtr=qtr)):
                            os.mkdir(path + r'\{year}\{qtr}'.format(year=year, qtr=qtr))
                        with open(path + r'\{year}\{qtr}\{j}'.format(year=year, qtr=qtr, j=j), 'w', encoding='utf8') as f:
                            f.write(response)
                        print(f'{year}年，{qtr}季度，{j}为空文件！！！{url}')
                        print('已重新下载完毕！')



if __name__ == '__main__':
    params_loaded(1993, 2018)

def download_masterindex(year, qtr, flag=False):
    # Download Master.idx from EDGAR
    # Loop accounts for temporary server/ISP issues
    # ND-SRAF / McDonald : 201606

    import time
    from urllib.request import urlopen, Request
    # import requests
    from zipfile import ZipFile
    from io import BytesIO
    from fake_useragent import UserAgent

    ua = UserAgent(use_cache_server=False)

    headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Connection': 'keep-alive',
        'Referer': f'https://www.sec.gov/Archives/edgar/full-index/{year}/{qtr}/',
        'Host': 'www.sec.gov',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random
    }

    number_of_tries = 10
    sleep_time = 10  # Note sleep time accumulates according to err


    PARM_ROOT_PATH = 'https://www.sec.gov/Archives/edgar/full-index/'

    start = time.clock()  # Note: using clock time not CPU
    masterindex = []
    #  using the zip file is a little more complicated but orders of magnitude faster
    append_path = str(year) + '/QTR' + str(qtr) + '/master.zip'  # /master.idx => nonzip version
    sec_url = PARM_ROOT_PATH + append_path
    sec_url1 = PARM_ROOT_PATH + str(year) + '/QTR' + str(qtr) + '/master.idx'
    req1 = Request(url=sec_url, headers=headers)
    req2 = Request(url=sec_url1, headers=headers)
    for i in range(1, number_of_tries + 1):
        try:
            # master = urlopen(req2).read().decode('utf8', 'ignore')
            # with open(rf'D:\work\files\EDGAR_DATA\master\2018-11-9\{year}-{qtr}-master.idx', 'w', encoding='utf8') as f:
            #     f.write(master)
            # print('maste保存完毕')
            zipfile = ZipFile(BytesIO(urlopen(req1).read()))
            records = zipfile.open('master.idx').read().decode('utf-8', 'ignore').splitlines()[10:]
#           records = urlopen(sec_url).read().decode('utf-8').splitlines()[10:] #  => nonzip version
            break
        except Exception as exc:
            if i == 1:
                print('\nError in download_masterindex')
            print('  {0}. _url:  {1}'.format(i, sec_url))

            print('  Warning: {0}  [{1}]'.format(str(exc), time.strftime('%c')))
            if '404' in str(exc):
                break
            if i == number_of_tries:
                return False
            print('     Retry in {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
            sleep_time += sleep_time


    # Load m.i. records into masterindex list
    for line in records:
        mir = MasterIndexRecord(line)
        if not mir.err:
            masterindex.append(mir)

    if flag:
        print('download_masterindex:  ' + str(year) + ':' + str(qtr) + ' | ' +
              'len() = {:,}'.format(len(masterindex)) + ' | Time = {0:.4f}'.format(time.clock() - start) +
              ' seconds')

    return masterindex


class MasterIndexRecord:
    def __init__(self, line):
        self.err = False
        parts = line.split('|')
        if len(parts) == 5:
            self.cik = int(parts[0])
            self.name = parts[1]
            self.form = parts[2]
            self.filingdate = int(parts[3].replace('-', ''))
            self.path = parts[4]
        else:
            self.err = True
        return
import json
import os
from multiprocessing import cpu_count
from multiprocessing import Pool

import requests
from tqdm import tqdm

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'data/out-robots/')
DATASET = os.path.join(os.path.dirname(__file__), 'data/_NON_TECH_CANDIDATE.csv')

import pandas as pd


def fetch_robots_txt(host):
    host = 'http://' + host + '/robots.txt'

    try:
        r = requests.get(
            host,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 '
                              'Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-encoding': 'gzip, deflate, br',
                'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://yandex.ru/',
                'If-Modified-Since': 'Fri, 05 Mar 2021 13:58:07 GMT',
            },
            timeout=3
        )

        return {
            'ok': r.ok,
            'host': host,
            'contentType': r.headers.get('Content-Type'),
            'statusCode': r.status_code,
            'headers': r.headers,
            'content': r.content,
            'current_url': r.url,
            'history': json.dumps([
                                      h.url
                                      for h in r.history
                                  ] + [r.url]),
        }
    except:
        return {
            'ok': False,
            'host': host,
            'contentType': '',
            'statusCode': '',
            'headers': '',
            'content': '',
            'current_url': '',
            'history': '',
        }


def main():
    hosts = pd.read_csv(DATASET)['host'].tolist()

    with Pool(processes=cpu_count()) as p:
        with tqdm(total=len(hosts)) as pbar:
            for i, ret in enumerate(p.imap_unordered(fetch_robots_txt, hosts)):
                pbar.update()
                pd.Series(ret).to_csv(os.path.join(OUTPUT_DIR, f'{i}.csv'), index=False)


if __name__ == '__main__':
    main()

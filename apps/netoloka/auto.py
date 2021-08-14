from multiprocessing import cpu_count
from multiprocessing import Pool

import pandas as pd
import requests
from tqdm import tqdm

RAW_DATASET = 'data/raw/train.csv'
OUTPUT_DIR = 'data/out/'


def validate_host(host):
    try:
        r = requests.get(
            'http://' + host,
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
            'host': host,
            'contentType': r.headers.get('Content-Type'),
            'statusCode': r.status_code,
            'headers': r.headers,
            'content': r.content,
            'current_url': r.url,
            'history': [
                           h.url
                           for h in r.history
                       ] + [r.url],
            'ok': r.ok,
        }
    except:
        return {
            'host': host,
            'ok': False
        }


def main():
    df = pd.read_csv(RAW_DATASET)
    df = df[~df['is_tech']].reset_index(drop=True)
    hosts = df['host'].tolist()

    with Pool(processes=cpu_count()) as p:
        with tqdm(total=len(hosts)) as pbar:
            for i, ret in enumerate(p.imap_unordered(validate_host, hosts)):
                pbar.update()
                pd.Series(ret).to_csv(OUTPUT_DIR + f'{i}.csv', index=False)


if __name__ == '__main__':
    main()

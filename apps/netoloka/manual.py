import os

import pandas as pd
from selenium import webdriver

RAW_DATASET = 'data/raw/train.csv'
OUTPUT_DATASET = 'data/output.csv'


def main():
    df = pd.read_csv(RAW_DATASET)
    df = df[~df['is_tech']].reset_index(drop=True)
    if os.path.exists(OUTPUT_DATASET):
        df_out = pd.read_csv(OUTPUT_DATASET)
    else:
        df_out = pd.DataFrame({
            'host': [],
            'is_tech_auto': [],
            'is_tech_manual': [],

        })
        df_out.to_csv(OUTPUT_DATASET, index=False)

    df = df[~df['host'].isin(set(df_out['host'].tolist()))]

    out = df_out.to_dict('records')

    driver = webdriver.Chrome("drivers/chromedriver")

    for line in df.to_dict('records'):
        url = 'http://' + line['host']

        try:
            driver.get(url)
        except:
            pass

        is_tech_manual = ''
        while is_tech_manual not in {'y', 'n', 'q'}:
            print(url)
            is_tech_manual = input('Это технический хост? [y/n]')

        if is_tech_manual == 'q':
            exit()

        out += [{
            'host': line['host'],
            'is_tech_auto': line['is_tech'],
            'is_tech_manual': is_tech_manual == 'y'
        }]
        pd.DataFrame(out).to_csv(OUTPUT_DATASET, index=False)

    driver.close()


if __name__ == '__main__':
    main()

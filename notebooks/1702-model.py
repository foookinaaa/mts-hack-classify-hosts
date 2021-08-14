import re
from typing import List

import dill
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split

"""
digits_count           33.071538
url_len                25.948447
max_domain_level       22.741060
max_domain_part_len    18.238955
dtype: float64
precision=0.95
recall=0.96
------


"""


class ExternalPredictor:
    def __init__(self, booster):
        self._booster = booster

    def predict(self, hosts):
        return self._predict(self._booster, self._create_features(hosts))

    @classmethod
    def _create_features(cls, hosts: List[str]):
        import pandas as pd
        import re

        df_features = pd.DataFrame()
        df_features['host'] = hosts
        df_features['url_len'] = df_features['host'].apply(lambda s: len(s))
        df_features['max_domain_level'] = df_features['host'].apply(lambda s: len(s.split('.')))
        df_features['max_domain_part_len'] = df_features['host'].apply(
            lambda s: max((len(s_i) for s_i in s.split('.'))))

        re_digit = re.compile('\D')
        df_features['digits_count'] = df_features['host'].apply(lambda s: len(re_digit.sub('', s)))

        del df_features['host']
        return df_features

    @classmethod
    def _predict(cls, booster, df_features):
        import shap

        explainer = shap.Explainer(booster)
        predicted_proba = round(booster.predict_proba(df_features)[0][0], 2)
        shap_values = explainer(df_features)
        shap_feature_importance = dict(zip(
            shap_values.feature_names,
            [
                round(x, 2)
                for x in shap_values.values[0].tolist()
            ]
        ))

        return {
            'predicted_proba': predicted_proba,
            'shap_feature_importance': shap_feature_importance
        }


def main():
    df = pd.read_csv('data/train.csv')

    X, y = df[['host']], df['is_tech'].values.astype(int).tolist()
    X_train, X_test, y_train, y_test = train_test_split(X[['host']], y, test_size=0.33,
                                                        random_state=42)
    X = ExternalPredictor._create_features(X['host'].tolist())
    X_train = ExternalPredictor._create_features(X_train['host'].tolist())
    X_test = ExternalPredictor._create_features(X_test['host'].tolist())

    model = CatBoostClassifier(random_state=0, verbose=0)
    booster = model.fit(X_train, y_train)
    print(pd.Series(dict(zip(booster.feature_names_, booster.feature_importances_))).sort_values(ascending=False))
    predicts = booster.predict(X_test)
    print(f'precision={round(precision_score(y_test, predicts), 2)}')
    print(f'recall={round(recall_score(y_test, predicts), 2)}')

    booster_export = model.fit(X, y)
    predictor = ExternalPredictor(booster_export)
    with open('data/model.bin', 'wb') as f:
        dill.dump(predictor, f)


if __name__ == '__main__':
    main()

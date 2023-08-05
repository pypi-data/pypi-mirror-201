import os
os.environ["OMP_NUM_THREADS"] = "1" # export OMP_NUM_THREADS=1
os.environ["OPENBLAS_NUM_THREADS"] = "1" # export OPENBLAS_NUM_THREADS=1
os.environ["MKL_NUM_THREADS"] = "1" # export MKL_NUM_THREADS=1
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" # export VECLIB_MAXIMUM_THREADS=1
os.environ["NUMEXPR_NUM_THREADS"] = "1" # export NUMEXPR_NUM_THREADS=1

from sklearn import preprocessing
import numpy as np
import gc
from collections import Counter
import pandas as pd
import scipy.stats as ss
from numpy import dot
from numpy.linalg import norm
import math
from sklearn.metrics import matthews_corrcoef
from joblib import Parallel, delayed
import optuna


class ConditionProbabilitiesClassifier:
    """
    This classifier measures the conditional probability of the target variable for each feature
    separately. Numerical values are converted into buckets for this purpose.
    Additionally, the explanatory power of each feature is measured using Theil's U. The conditional probabilities
    are then weighted by Theil's U.
    :param df: Pandas DataFrame containing the target feature.
    :param cat_feats: List of strings with column names specifying categorical features.
    :param num_feats: List of strings with column names specifying numerical features.
    :param target: String specifying name of the target column.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 cat_feats: list,
                 num_feats: list,
                 target: str,
                 thresholds: int = 100):
        self.df = df.reset_index(drop=True)
        self.cat_feats = cat_feats
        self.num_feats = num_feats
        self.target = target

        self.thresholds = np.linspace(0, 1, thresholds)
        self.num_buckets = [f"< {threshold}" for threshold in self.thresholds]
        self.cat_cond_probs = {}
        self.num_cond_probs = {}
        self.prediction_cond_probs = {}
        self.cat_theil_u_weights = {}
        self.num_theil_u_weights = {}
        self.cat_selected_features = []
        self.num_selected_features = []
        self.scalers = {}
        self.feature_weights = {}
        self.weight_scaler = None
        self.pred_scalar = None

    def fill_nulls(self, df: pd.DataFrame, col: str, fill_with=None, coltype: str = 'str'):
        """
        Fill nulls with provided term.
        :param df: Pandas DaaFrame
        :param col: String specifying column name.
        :param fill_with: String, integer or float to fill missing values with.
        :param coltype: One of 'str' or 'float'. Will be used to typecast the column.
        """
        if coltype == 'str':
            df[col] = df[col].astype(str)
        elif coltype == 'float':
            df[col] = df[col].astype(np.float32)

        df[col] = df[col].fillna(fill_with)
        return df

    def fill_infs(self, df):
        """
        Fill nulls with provided term.
        :param df: Pandas DataFrame
        :param col: String specifying column name.
        """
        df = df.replace([np.inf, -np.inf], 0)
        return df

    def conditional_entropy(self, x, y):
        # entropy of x given y
        y_counter = Counter(y)
        xy_counter = Counter(list(zip(x, y)))
        total_occurrences = sum(y_counter.values())
        entropy = 0
        for xy in xy_counter.keys():
            p_xy = xy_counter[xy] / total_occurrences
            p_y = y_counter[xy[1]] / total_occurrences
            entropy += p_xy * math.log(p_y / p_xy)
        return entropy

    def theil_u(self, x, y):
        s_xy = self.conditional_entropy(x, y)
        x_counter = Counter(x)
        total_occurrences = sum(x_counter.values())
        p_x = list(map(lambda n: n / total_occurrences, x_counter.values()))
        s_x = ss.entropy(p_x)
        if s_x == 0:
            return 1
        else:
            return (s_x - s_xy) / s_x

    def fit_theil_u_weights(self):
        """
        Loops through categorical and numerical columns and measured their target explainability
        using Theil's U.
        :return: Updates class attributes.
        """
        for col in self.cat_feats:
            theil_u = self.theil_u(self.df[col], self.df[self.target])
            self.cat_theil_u_weights[col] = theil_u

        for col in self.num_feats:
            theil_u = self.theil_u(self.df[col], self.df[self.target])
            self.num_theil_u_weights[col] = theil_u

    def fit_theil_u_feature_selection(self):
        """
        Loops through all columns and selects columns with Theil U value of 0.03 or higher.
        :return: Updates selected_features attribute.
        """
        for col in self.cat_feats:
            if self.cat_theil_u_weights[col] >= 0.003:
                self.cat_selected_features.append(col)

        for col in self.num_feats:
            if self.num_theil_u_weights[col] >= 0.003:
                self.num_selected_features.append(col)

    def fit_categorical_cond_probas(self):
        """
        Loops through all categorical features and their categories
        and maps the conditional probability of the target.
        :return: Updates class attributes.
        """
        for col in self.cat_feats:
            self.cat_cond_probs[col] = {}
            nb_cats = self.df[col].nunique()
            for category in self.df[col].unique():
                temp_df = self.df.loc[self.df[col] == category]
                prior = nb_cats / len(self.df.index)
                likelihood = len(temp_df.loc[temp_df[self.target] == True].index) / len(temp_df.index)
                cond_prob = prior * likelihood #/ (len(temp_df.index) / len(self.df.index))
                self.cat_cond_probs[col][category] = cond_prob
                del temp_df
                _ = gc.collect()

            if "Unknown" not in self.cat_cond_probs[col].keys():
                self.cat_cond_probs[col]["Unknown"] = 0

    def fit_predict_buckets(self, col: str):
        """
        Takes a column of a numerical type and returns it as a bucketed version.
        :param col: String specifying which column to scale and return as bucketed version.
        :return: Pandas DataFrame
        """
        # scale Series
        scaler = preprocessing.MinMaxScaler()
        scaled = scaler.fit_transform(self.df[[col]])
        scaled = pd.DataFrame(scaled, columns=[col])
        self.scalers[col] = scaler

        # transform into buckets
        conditions = []
        for thres in self.thresholds:
            conditions.append((scaled[col] < thres))

        choices = self.num_buckets

        scaled[col] = np.select(conditions, choices, default='Unknown')
        return scaled

    def predict_buckets(self, df, col: str):
        """
        Takes a Pandas Series of a numerical type and returns it as a bucketed version.
        :param col: String specifying which column to scale and return as bucketed version.
        returns: Pandas DataFrame
        """
        # scale Series
        scaler = self.scalers[col]
        scaled = scaler.transform(df[[col]])
        scaled = pd.DataFrame(scaled, columns=[col])

        # transform into buckets
        conditions = []
        for thres in self.thresholds:
            conditions.append((scaled[col] < thres))

        choices = self.num_buckets

        scaled[col] = np.select(conditions, choices, default='Unknown')
        return scaled

    def fit_numerical_cond_probas(self):
        """
        Loops through all numerical features and their buckets
        and maps the conditional probabilities of the target.
        """
        for col in self.num_feats:
            bucketed = self.fit_predict_buckets(col=col)
            bucketed[self.target] = self.df[self.target]
            self.num_cond_probs[col] = {}
            cond_prob = 0
            for bucket in self.num_buckets:
                temp_df = bucketed.loc[bucketed[col] == bucket]
                if temp_df.empty:
                    pass
                else:
                    prior = len(self.thresholds) / len(self.df.index)
                    likelihood = len(temp_df.loc[temp_df[self.target] == True].index) / len(temp_df.index)
                    cond_prob = prior * likelihood #/ (len(temp_df.index) / len(self.df.index))
                    del temp_df
                    _ = gc.collect()
                self.num_cond_probs[col][bucket] = cond_prob

            if "Unknown" not in self.num_cond_probs[col].keys():
                self.num_cond_probs[col]["Unknown"] = 0

            del bucketed
            _ = gc.collect()

    def fit_predict_feature_weights(self):
        all_features = self.cat_selected_features + self.num_selected_features
        temp_df = self.df[all_features].copy()

        best_score = -1
        for i in range(1):
            for col in all_features:
                if i == 0:
                    self.feature_weights[col] = 1 #initialize default value
                best_weight = 1
                or_feat = self.df[col].copy()

                for weight in np.linspace(0, 1, 200):
                    temp_df[col] = or_feat * weight
                    preds = temp_df[all_features].mean(axis=1) + (2 * temp_df[all_features].std(axis=1))
                    #preds = np.log1p(preds)
                    feat_scaler = preprocessing.MinMaxScaler()
                    preds = feat_scaler.fit_transform(preds.values.reshape(-1, 1))
                    score = matthews_corrcoef(preds > 0.5, self.df[self.target])
                    if score > best_score:
                        best_score = score
                        best_weight = weight
                        self.feature_weights[col] = best_weight
                        #print(f"New best score achieved for feat {col}: {score}.")

                self.df[col] = or_feat * self.feature_weights[col]

        preds = self.df[all_features].mean(axis=1)
        feat_scaler = preprocessing.MinMaxScaler()
        preds = feat_scaler.fit_transform(preds.values.reshape(-1, 1))
        self.pred_scalar = feat_scaler

    def predict_feature_weights(self, df):
        all_features = self.cat_selected_features + self.num_selected_features

        for col in all_features:
            df[col] = df[col] * self.feature_weights[col]
        return df

    def fit_predict_prediction_buckets(self, predictions: np.array):
        """
        Takes a column of a numerical type and returns it as a bucketed version.
        :param predictions: Takes numpy array, scales it and places it into buckets.
        :return: Pandas DataFrame
        """
        col = "predictions"
        # scale Series
        scaler = preprocessing.MinMaxScaler()
        scaled = scaler.fit_transform(predictions.reshape(-1, 1))
        scaled = pd.DataFrame(scaled, columns=[col])
        self.scalers[col] = scaler

        # transform into buckets
        conditions = []
        for thres in np.linspace(0, 1, 20):
            conditions.append((scaled[col] < thres))

        choices = [f"< {threshold}" for threshold in np.linspace(0, 1, 20)]

        scaled[col] = np.select(conditions, choices, default='Unknown')
        return scaled

    def predict_prediction_buckets(self, predictions: np.array):
        """
        Takes a Pandas Series of a numerical type and returns it as a bucketed version.
        :param predictions: Takes numpy array, scales it and places it into buckets.
        returns: Pandas DataFrame
        """
        col = "predictions"
        # scale Series
        scaler = self.scalers[col]
        scaled = scaler.transform(predictions.reshape(-1, 1))
        scaled = pd.DataFrame(scaled, columns=[col])

        # transform into buckets
        conditions = []
        for thres in np.linspace(0, 1, 20):
            conditions.append((scaled[col] < thres))

        choices = [f"< {threshold}" for threshold in np.linspace(0, 1, 20)]

        scaled[col] = np.select(conditions, choices, default="Unknown")
        return scaled

    def fit_prediction_cond_probas(self, predictions: np.array):
        """
        Takes predictions and maps the conditional probabilities of the target.
        """
        col = "predictions"
        bucketed = self.fit_predict_prediction_buckets(predictions)
        bucketed[self.target] = self.df[self.target]
        self.prediction_cond_probs = {}
        cond_prob = 0
        for bucket in [f"< {threshold}" for threshold in np.linspace(0, 1, 20)]:
            temp_df = bucketed.loc[bucketed[col] == bucket]
            if temp_df.empty:
                pass
            else:
                target_df = temp_df.loc[temp_df[self.target] == True]
                cond_prob = len(target_df.index) / len(temp_df.index)
                del target_df
                _ = gc.collect()
            self.prediction_cond_probs[bucket] = cond_prob
        if "Unknown" not in self.prediction_cond_probs.keys():
            self.prediction_cond_probs["Unknown"] = 1
        _ = gc.collect()
        return bucketed

    def fit(self):
        """
        Wrapper function to fit conditional probabilities
        of categorial and numerical features. Updates the
        dictionaries self.cat_cond_probs and self.num_cond_probs.
        """
        self.df = self.fill_infs(self.df)

        for col in self.cat_feats:
            self.df = self.fill_nulls(self.df, col, fill_with='Unknown', coltype='str')

        for col in self.num_feats:
            self.df = self.fill_nulls(self.df, col, fill_with=0, coltype='float')

        self.fit_categorical_cond_probas()
        self.fit_numerical_cond_probas()
        self.fit_theil_u_weights()
        self.fit_theil_u_feature_selection()

    def fit_predict(self):
        """
        Wrapper function to fit conditional probabilities
        of categorial and numerical features. Updates the
        dictionaries self.cat_cond_probs and self.num_cond_probs.
        """
        self.fit()

        # transform cols into conditional probas
        for col in self.cat_selected_features:
            for category in self.df[col].unique():
                if category not in self.cat_cond_probs[col].keys():
                    self.cat_cond_probs[col][category] = 0
            self.df = self.df.replace(self.cat_cond_probs[col])

        for col in self.num_selected_features:
            self.df[col] = self.predict_buckets(self.df, col)
            self.df = self.df.replace(self.num_cond_probs[col])

        self.fit_predict_feature_weights()

        # get predictions
        preds = self.df[self.cat_selected_features + self.num_selected_features].mean(axis=1)
        preds_df = self.fit_prediction_cond_probas(preds.values)
        preds_df = preds_df.replace(self.prediction_cond_probs)
        self.df = None
        _ = gc.collect()
        return preds_df["predictions"]

    def predict(self, df: pd.DataFrame):
        """
        Create predictions based on conditional probabilities and their Theil's U weights.
        :param df: Pandas DataFrame for prediction.
        :return Pandas Series
        """
        df = self.fill_infs(df)
        # transform cols into conditional probas
        for col in self.cat_selected_features:
            df = self.fill_nulls(df, col, fill_with='Unknown')
            for category in df[col].unique():
                if category not in self.cat_cond_probs[col].keys():
                    self.cat_cond_probs[col][category] = 0
            df = df.replace(self.cat_cond_probs[col])

        for col in self.num_selected_features:
            df = self.fill_nulls(df, col, fill_with=0, coltype='float')
            df[col] = self.predict_buckets(df, col)
            df = df.replace(self.num_cond_probs[col])

        df = self.predict_feature_weights(df)
        # get predictions
        preds = df[self.cat_selected_features + self.num_selected_features].mean(axis=1)
        preds_df = self.predict_prediction_buckets(preds.values)
        preds_df = preds_df.replace(self.prediction_cond_probs)
        self.df = None
        _ = gc.collect()
        return preds_df["predictions"]


class ProbaBoost:
    """
    This classifier measures the conditional probability of the target variable for each feature
    separately. Numerical values are converted into buckets for this purpose.
    Additionally, the explanatory power of each feature is measured using Theil's U. The conditional probabilities
    are then weighted by Theil's U.
    :param df: Pandas DataFrame containing the target feature.
    :param cat_feats: List of strings with column names specifying categorical features.
    :param num_feats: List of strings with column names specifying numerical features.
    :param target: String specifying name of the target column.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 cat_feats: list,
                 num_feats: list,
                 target: str,
                 nb_boosters: int = 10,
                 sample_per_booster: float = 0.2,
                 random_state=5000):
        self.df = df.reset_index(drop=True)
        self.cat_feats = cat_feats
        self.num_feats = num_feats
        self.target = target
        self.nb_boosters = nb_boosters
        self.sample_per_booster = sample_per_booster
        self.class_sizes = {}
        self.class_representation_order = {}
        self.random_state = random_state
        self.conditional_classifiers = []
        self.thresholds_chosen = []
        self.target_class_samp_sizes = []
        self.final_models = []
        self.training_model_scores = {}

    def eda(self):
        sample_df = self.df.sample(frac=self.sample_per_booster, random_state=self.random_state)
        most_samples = 0
        for i in range(2):
            for clas in self.df[self.target].unique():
                no_samples = len(sample_df.loc[sample_df[self.target] == clas].index)
                self.class_sizes[clas] = no_samples
                if no_samples >= most_samples:
                    self.class_representation_order["most"] = clas
                    most_samples = no_samples
                else:
                    self.class_representation_order["least"] = clas

    def train_model(self, i, threshold, tcss):
        if tcss > 100:
            class_1_needed = self.class_sizes[self.class_representation_order["least"]]
            class_0_needed = int(-1*(self.class_sizes[self.class_representation_order["least"]] * (tcss/100)) + (self.class_sizes[self.class_representation_order["most"]] + self.class_sizes[self.class_representation_order["least"]]))
        elif tcss < 100:
            class_1_needed = int(self.class_sizes[self.class_representation_order["least"]] * (tcss/100))
            class_0_needed = self.class_sizes[self.class_representation_order["most"]]
        else:
            class_1_needed = self.class_sizes[self.class_representation_order["least"]]
            class_0_needed = self.class_sizes[self.class_representation_order["most"]]

        sample_df = self.df.sample(frac=self.sample_per_booster, random_state=self.random_state+i, replace=True)
        df_clas_0 = sample_df.sample(class_0_needed, random_state=self.random_state+i, replace=True)
        df_clas_1 = sample_df.sample(class_1_needed, random_state=self.random_state+i, replace=True)
        sample_df = pd.concat([df_clas_0, df_clas_1]).reset_index(drop=True)

        cpc = ConditionProbabilitiesClassifier(
            df=sample_df,
            cat_feats=self.cat_feats,
            num_feats=self.num_feats,
            target=self.target,
            thresholds=threshold)

        cpc.fit_predict()
        return {"model_obj": cpc,
                "threshold": threshold}

    def model_predict(self, i, df):
        cpc = self.conditional_classifiers[i]
        churn_proba = cpc.predict(df)
        churn_proba = churn_proba.astype(float)
        del cpc
        _ = gc.collect()
        return {i: churn_proba}

    def fit(self):
        self.eda()
        # Training part with insample data
        for i in range(self.nb_boosters):
            threshold = int(np.random.normal(100, 5))
            tcss = int(np.random.normal(int(self.sample_per_booster*100), 15))
            if threshold < 10:
                threshold = 10
            elif threshold > 200:
                threshold = 200
            self.thresholds_chosen.append(threshold)
            if tcss < 0.0001:
                tcss = 0.0001
            elif tcss > 200:
                tcss = 200
            self.target_class_samp_sizes.append(tcss)

        model_objects = Parallel(n_jobs=-1)(
            delayed(self.train_model)(i, threshold, tcss) for i, threshold, tcss in zip(range(self.nb_boosters), self.thresholds_chosen, self.target_class_samp_sizes))

        for obj in model_objects:
            self.conditional_classifiers.append(obj["model_obj"])

        del model_objects
        _ = gc.collect()

        # fine-tuning on new sample
        self.df = self.df.sample(frac=1.0, random_state=self.random_state+self.nb_boosters, replace=True).reset_index(drop=True)
        prediction_objects = Parallel(n_jobs=-1)(
            delayed(self.model_predict)(i, self.df) for i in range(self.nb_boosters))

        predictions = {}
        for i in prediction_objects:
            for key, item in i.items():
                predictions[key] = item

        del prediction_objects
        _ = gc.collect()

        pred_df = pd.DataFrame(predictions)

        for col in pred_df.columns:
            self.training_model_scores[col] = matthews_corrcoef(pred_df[col] > 0.5, self.df[self.target])

        def objective(trial):
            param = {}
            # we go crazy here and allow Optuna to choose the columns
            for col in pred_df.columns:
                param[col] = trial.suggest_int(col, 0, 1)

            temp_features = []
            for k, v in param.items():
                if v == 1:
                    temp_features.append(k)
                else:
                    pass

            if len(temp_features) > 0:
                temp_preds = pred_df[temp_features].mean(axis=1)
                temp_preds = temp_preds.astype(float) > 0.5
                res = matthews_corrcoef(temp_preds, self.df[self.target])
            else:
                res = -1

            return res

        sampler = optuna.samplers.TPESampler(multivariate=True, seed=42)
        study = optuna.create_study(
            direction="maximize", sampler=sampler, study_name="select models"
        )
        study.optimize(
            objective,
            n_trials=2000,
            gc_after_trial=True,
            show_progress_bar=True,
            timeout=1 * 60 * 60,
        )

        for k, v in study.best_trial.params.items():
            if v == 1:
                self.final_models.append(k)
            else:
                pass

    def predict(self, df):
        prediction_objects = Parallel(n_jobs=-1)(
            delayed(self.model_predict)(i, df) for i in range(self.nb_boosters) if i in self.final_models)

        predictions = {}
        for i in prediction_objects:
            for key, item in i.items():
                predictions[key] = item

        del prediction_objects
        _ = gc.collect()

        pred_df = pd.DataFrame(predictions)

        pred_df["predictions"] = pred_df[self.final_models].mean(axis=1)
        pred_df["predictions"] = pred_df["predictions"].astype(float)
        return pred_df


class DatetimePrep:
    def __init__(self,
                 df,
                 date_columns):
        self.df = df
        self.date_columns = date_columns
        self.date_columns_created = {}
        self.new_sin_cos_col_names = {}

    def date_converter(self):
        """
        Takes in a dataframe and loops through datetime columns to and extracts the date parts month, day, dayofweek
        and hour and adds them as additional columns.
        :param dataframe:
        :return: Returns modified dataframe.
        """
        for c in self.date_columns:
            if c in self.df.columns:
                self.df[c + "_month"] = self.df[c].dt.month
                self.date_columns_created[c + "_month"] = "month"

                self.df[c + "_day"] = self.df[c].dt.day
                self.date_columns_created[c + "_day"] = "day"

                self.df[c + "_hour"] = self.df[c].dt.hour
                self.date_columns_created[c + "_hour"] = "hour"

    def cos_sin_transformation(self):
        """
        Takes in a dataframe and loops through date columns. Create sine and cosine features and appends them
        as new columns.
        :param dataframe:
        :return: Returns modified dataframe.
        """
        for c in self.date_columns_created:
            if c in self.df.columns:
                if self.date_columns_created[c] == "month":
                    self.df[c + "_sin"] = np.sin(
                        self.df[c] * (2.0 * np.pi / 12)
                    )
                    self.df[c + "_cos"] = np.cos(
                        self.df[c] * (2.0 * np.pi / 12)
                    )
                    self.new_sin_cos_col_names[c] = []
                    self.new_sin_cos_col_names[c].append(c + "_sin")
                    self.new_sin_cos_col_names[c].append(c + "_cos")
                elif self.date_columns_created[c] == "day":
                    self.df[c + "_sin"] = np.sin(
                        self.df[c] * (2.0 * np.pi / 31)
                    )
                    self.df[c + "_cos"] = np.cos(
                        self.df[c] * (2.0 * np.pi / 31)
                    )
                    self.new_sin_cos_col_names[c] = []
                    self.new_sin_cos_col_names[c].append(c + "_sin")
                    self.new_sin_cos_col_names[c].append(c + "_cos")
                elif self.date_columns_created[c] == "hour":
                    self.df[c + "_sin"] = np.sin(
                        self.df[c] * (2.0 * np.pi / 24)
                    )
                    self.df[c + "_cos"] = np.cos(
                        self.df[c] * (2.0 * np.pi / 23)
                    )
                    self.new_sin_cos_col_names[c] = []
                    self.new_sin_cos_col_names[c].append(c + "_sin")
                    self.new_sin_cos_col_names[c].append(c + "_cos")

    def fit_transform(self):
        self.date_converter()
        self.cos_sin_transformation()



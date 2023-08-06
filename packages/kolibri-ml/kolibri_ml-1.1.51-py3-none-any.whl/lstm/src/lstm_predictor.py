import abc
import logging
import pandas as pd
from dataclasses import dataclass, field
from typing import Any
import numpy as np
from kolibri.preprocess.tabular.univar_outliers import UnivarOutlier
from kolibri.preprocess.tabular.data_imputer import DataImputer
from kolibri.preprocess.tabular.normalize import Normalizer
from kolibri.preprocess.timeseries.multi_window_generator import MultiWindowGenerator
from kolibri.backend.tensorflow.tasks.structured.regression.dnn_regression_estimator import DnnRegressionEstimator
from kolibri.backend.tensorflow.autoencoder.base_autoencoder import BaseAutoEncoder
from tqdm import tqdm
from kolibri import ModelTrainer, ModelConfig, ModelLoader
from kolibri.preprocess.tabular.one_hot_encoder_multi import MultiColomnOneHotEncoder

import os

@dataclass
class AnomalyDetector(abc.ABC):
    train_data: Any
    current_pay_data: Any
    event_config: dict
    model_config: dict = field(init=False)
    model: Any = field(init=False)

    @abc.abstractmethod
    def get_model_config(self) -> dict:
        raise NotImplementedError("Implement get_model_config method")

    @abc.abstractmethod
    def load_model(self) -> None:
        pass

    @abc.abstractmethod
    def train(self) -> Any:
        pass

    @abc.abstractmethod
    def detect(self) -> pd.DataFrame:
        raise NotImplementedError("Implement detect method")

    @abc.abstractmethod
    def scan(self) -> pd.DataFrame:
        raise NotImplementedError("Implement scan method")


class FPA(AnomalyDetector):
    model_config = {
        "columns_to_drop": ['Pay_Period', 'Period_End_Date', 'Company_Id', 'Paydate', 'Tolerance'],
        "group_by_columns": ['Period_Start_Date', 'Employee_Id', 'Employee_Status', 'Variable_Id', 'Year', 'Month',
                             'Week',
                             'Day'],
        "group_column": "Employee_Id",
        "date_column": "Period_Start_Date",
        "value_column": "Value",
        "employee_status_column": 'Employee_Status',
        "features": [],
        "epochs": 200,
        "dropout": 0.3,
        "ae-loss": 'mae',
        "target": None,
        "dummies": [],
        "scale_cols": [],
        "horizon": 1,
        "min_window": 1,
        "max_window": 4,
        "multi_variate_output": False,
        "confidence": 0.01,
        "loss": "mse",
        "bayesian_samples": 10,
        "patience": 2,
        "pooling_mode": "mean",  # "quantile"
        "normalize_method": "log10",
        "normalize_columns": [],
        "alpha": 0.05,
        "pre-train": True,
        "train": True,
        "steps_per_epoch": 150,
        "model": "lstm",
        "remote-storage": "azure-blob",
        "model-name": "model_nn.h5",
        "output-folder": ".",
        "sets":["val", "test"]
    }

    def __init__(self, train_data=None,  event_config=None):
        super().__init__(train_data, None, event_config)
        self.model_config.update(event_config)
        self.scaler=None
        self.model_interpreter=None
        self.target_label="_Value_"
        if train_data is not None:
            self.train_data=self._preprocess_data(self.train_data)

    def get_model_config(self) -> None:
        model_config = {
            "columns_to_drop": [],
            "group_by_columns": ['Period_Start_Date', 'Employee_Id', 'Employee_Status', 'Variable_Id'],
            "group_column": "Employee_Id",
            "date_column": "Original_Start_Date",
            "features": ["Employee_Status"],
            "epochs": 4,
            "target": 35,
            "dummies": ["Employee_Status"],
            "normalize_columns": [],
            "horizon": 1,
            "min_window": 1,
            "max_window": 4,
            "pre-train": True,
            "train":True,
            "n_jobs":-1,
#            "container-name": "lstmmodel",
            "remote-storage": None,
            "multi_variate_output": False,
            "output-folder": "../outputs"
        }
        self.model_config.update(model_config)
        logging.info(self.model_config)

    def load_model(self):

        if self.model_config["remote-storage"]== "azure-blob":
            print('loading regression model')
            self.lstm = DnnRegressionEstimator.load_from_azure(self.model_config["container-name"])
            print('loading auto encoders')
            self.auto_ae = BaseAutoEncoder.load_from_azure(self.model_config["container-name"])

        else:
            print('loading regression model')
            self.lstm = DnnRegressionEstimator.load(self.model_config['output-folder'])
            print('loading auto encoders')
            self.auto_ae = BaseAutoEncoder.load_model(model_path=self.model_config["output-folder"])

        print('model loaded')

    def train(self):
        self.train_data=self._fit_transform_features(self.train_data)
        self.fit_transform_normaliser()
        self.train_autoencoder()
        return self.train_lstm()

    def train_lstm(self):

        self.model_config["loss"] = "mse"

        self.model_config["multi_variate_output"] = True

        predictor_ds = self._generate_dataset(self.train_data, split_sets=self.model_config["sets"])

        print('Training predictor')


        Y_encoder_train = predictor_ds.train[0][:, :, 0]
        Y_encoder_val = predictor_ds.val[0][:, :, 0]

        # inference_feature
        XX_train = self.auto_ae.encoder.predict(Y_encoder_train)
        XX_val = self.auto_ae.encoder.predict(Y_encoder_val)

        x_train, y_train = predictor_ds.train
        x_val, y_val = predictor_ds.val

        external_feature_train = y_train[:, :, 1:]
        external_feature_val = y_val[:, :, 1:]

        Y_label_train = y_train[:, :, 0]

        Y_label_val = y_val[:, :, 0]

        self.model_config["n_features"] = x_train.shape[2] - 1

        self.lstm=DnnRegressionEstimator(self.model_config)


        self.lstm.fit(X=[XX_train, external_feature_train], y=Y_label_train, X_val=[XX_val, external_feature_val],
                        y_val=Y_label_val)
        if self.model_config["remote-storage"] == "azure-blob":
            self.lstm.save_to_azure(self.model_config["container-name"])
            self.lstm = DnnRegressionEstimator.load_from_azure(self.model_config["container-name"])
        else:
            self.lstm.persist(self.model_config["output-folder"])
            self.lstm=DnnRegressionEstimator.load(self.model_config["output-folder"])

        if "test" in self.model_config["sets"]:
            return  self.predict_values(predictor_ds.test, predictor_ds.test_df)

    def train_autoencoder(self):
        self.model_config['loss'] = 'mae'
        wg = self._generate_dataset(self.train_data, split_sets=self.model_config["sets"], targets= [self.target_label])

        x_train, y_train = wg.train
        x_val, y_val = wg.val

        Y_label_train = y_train
        Y_label_val = y_val

        Y_encoder_train = x_train[:, :, 0]
        Y_encoder_val = x_val[:, :, 0]

        Y_decoder_train = Y_encoder_train
        Y_decoder_val = Y_encoder_val

        Y_encoder_train = Y_encoder_train.reshape(-1, self.model_config["max_window"], 1)
        Y_decoder_train = Y_decoder_train.reshape(-1, self.model_config["max_window"], 1)

        input_shape = (Y_encoder_train.shape[1], Y_encoder_train.shape[2])
        output_shape = (Y_decoder_train.shape[1], Y_decoder_train.shape[2])

        auto_ae = BaseAutoEncoder(self.model_config, input_shape, output_shape)

        auto_ae.fit(Y_encoder_train, Y_decoder_train, Y_label_train, Y_encoder_val,
                    Y_decoder_val, Y_label_val, epochs=self.model_config["epochs"], patience=self.model_config["patience"])

        if self.model_config["remote-storage"] == "azure-blob":
            auto_ae.save_to_azure(self.model_config["container-name"])
        else:
            auto_ae.save(model_path=self.model_config["output-folder"])
        #reload the model to verify that we can safely load the model later
        if self.model_config["remote-storage"] == "azure-blob":
            self.auto_ae = BaseAutoEncoder.load_from_azure(self.model_config["container-name"])
        else:
            self.auto_ae=BaseAutoEncoder.load_model(model_path=self.model_config["output-folder"])

    def _generate_dataset(self, df, split_sets=["test", "val"], targets=None):

        max_win = self.model_config["max_window"]
        if self.model_config["max_window"] == None:
            max_win = self.model_config["min_window"]

#        if not self.model_config["multi_variate_output"]:
        config = {
                "target": targets,
                "group": self.model_config["group_column"],
                "timestamp": self.model_config["date_column"],
                "horizon": self.model_config["horizon"],
                "split_column": None,
                "max-window-history": max_win,
                "min-window-history": self.model_config["min_window"],
                "n_jobs": self.model_config["n_jobs"] if "n_jobs" in self.model_config else 1,
                "sets": split_sets
            }

        return MultiWindowGenerator(data=df.reset_index(), configs=config)

    def detect(self, current_pay_period) -> pd.DataFrame:
        processed_current_pay_data=None
        try:
            processed_current_pay_data=self._preprocess_data(current_pay_period)
        except Exception as e:
            print(e)
        processed_current_pay_data=self._transform_features(processed_current_pay_data)
        processed_current_pay_data=self.normalise(processed_current_pay_data)

        self.model_config["multi_variate_output"] = True
        wg=self._generate_dataset(processed_current_pay_data, split_sets=["predict"])



        df = self.predict_values(wg.main, wg.main_df)
        alpha = self.model_config["alpha"]

        df['diffs'] = df[self.target_label] - df["medium"]
        df['anomaly'] = False
        df['anomaly'] = ~((df['lower'] * (1 - alpha)) <= df[self.target_label]) & (
                    (df['upper'] * (1 + alpha)) >= df[self.target_label])

        df.rename(columns={'id_sort': self.model_config['date_column'], 'id_group': self.model_config['group_column']}, inplace=True)
        return df


    def predict_values(self, to_predict, to_predict_df):


        p = self.model_config["confidence"]
        predictions = []
        for i in tqdm(range(0, self.model_config["bayesian_samples"])):
            predictions.append(self._predict_values(to_predict))

        pred1 = np.asarray(predictions)
        pp = pred1.T
        if self.model_config["pooling_mode"] == "quantile":
            lower = np.quantile(pp, p / 4, axis=1)
            upper = np.quantile(pp, 1 - p / 4, axis=1)
            medium = np.quantile(pp, 0.5, axis=1)
        elif self.model_config["pooling_mode"] == "mean":
            medium = np.mean(pp, axis=1)
            std = np.std(pp, axis=1)
            lower = medium - std
            upper = medium + std

        fdf = pd.DataFrame({
            "lower": lower,
            "medium": medium,
            "upper": upper
        })
        fdf = pd.concat([fdf, to_predict_df], axis=1)

        fdf[self.target_label] = self.scaler.inverse_transform_col(fdf[self.target_label], colName=self.target_label)

        return fdf.dropna()

    def _predict_values(self, to_predict):


        Y_encoder = to_predict[0][:, :, 0]
        external_features = to_predict[1][:, :, 1:]

        XX_test = self.auto_ae.encoder.predict(Y_encoder)
        Y_test_predict = self.lstm.predict([XX_test, external_features])
        Y_test_predict = Y_test_predict.reshape(len(Y_test_predict), )
        Y_test_predict = self.scaler.inverse_transform_col(Y_test_predict, colName=self.target_label)

        return Y_test_predict

    def scan(self) -> pd.DataFrame:
        self.get_model_config()
        model = self.train()
        output = self.detect(model)
        return output.to_json(orient="records")

    def _preprocess_data(self, df):
        selected = [self.model_config["group_column"]]
        df = df.drop(columns=self.model_config["columns_to_drop"])
        if 'Retro_Period' in list(df.columns):
            df = df[df.Retro_Period.isna()]
        nb_timesteps=len(df[self.model_config["date_column"]].unique().tolist())
        if nb_timesteps <2:
            raise Exception(
                "Isuficient data. Number of recrods should be at least 5. "+str(nb_timesteps)+ " are provided."
            )
        index_columns=[self.model_config["date_column"], self.model_config["group_column"]]
        if self.model_config["employee_status_column"] is not None:
            selected.append(self.model_config["employee_status_column"])
            index_columns.append(self.model_config["employee_status_column"])
        # df = pd.pivot_table(df, values=self.model_config["value_column"],
        #                       index=index_columns,
        #                       columns=['Variable_Id'], aggfunc=np.sum).fillna(0).replace(np.inf, 0).reset_index()
        try:
            df[self.model_config["date_column"]] = pd.to_datetime(df[self.model_config["date_column"]])
        except Exception as e:
            print("Error in converting the date in the data: "+str(e))
        df = df.set_index(self.model_config["date_column"])
        selected.append(self.model_config["target"])
        df = df[selected]
        df.rename(columns={self.model_config["target"]: self.target_label}, inplace=True)
        #replace negative values in targets by 0
        df.loc[df[self.target_label] < 0, self.target_label] = 0
        outliers = UnivarOutlier(params={"include-columns": [self.target_label]})
        df = outliers.fit_transform(df)
        imputer = DataImputer()
        return imputer.fit_transform(df)

    def _fit_transform_dummies(self, df):
        self.one_hot_encode = MultiColomnOneHotEncoder(self.model_config)
        self.one_hot_encode.fit(data= df)
        if self.model_config["remote-storage"] == "azure-blob":
            self.one_hot_encode.save_to_azure(self.model_config["container-name"])
        else:
            self.one_hot_encode.persist(self.model_config["output-folder"])
        return self.one_hot_encode.transform(data=df)

    def _transform_dummies(self, data):
        if not hasattr(self, "one_hot_encode"):
            if self.model_config["remote-storage"] == "azure-blob":
                self.one_hot_encode = MultiColomnOneHotEncoder.load_from_azure(self.model_config["container-name"])
            else:
                self.one_hot_encode = MultiColomnOneHotEncoder.load(self.model_config["output-folder"])
        return self.one_hot_encode.transform(data=data)


    def _fit_transform_features(self, df):

        if self.model_config["date_column"] in list(df.columns):
            df = df.set_index(pd.to_datetime(df[self.model_config["date_column"]]))[
                [self.model_config["group_column"], self.target_label] + self.model_config["features"]]
        else:
            df = df[[self.model_config["group_column"], self.target_label] + self.model_config["features"]]

        # build average values for the target variable

        #    data.loc[data[configs["target"]] < 0, configs["target"]] = 0
        df['Target_mean'] = df.groupby([self.model_config["group_column"]])[self.target_label].transform('mean')

        if "group" in list(df.columns):
            df['Target_mean'] = df.groupby([self.model_config["date_column"], 'group']).Gross_Total.transform('mean')

            df["Target_mean_diff"] = df["Target_mean"].diff(-1)

        if "month" not in list(df.columns):
            df['month'] = pd.DatetimeIndex(df.index).month
        self.model_config["dummies"].append("month")
        if self.model_config["dummies"] != []:
            df = self._fit_transform_dummies(df)
        return df

    def _transform_features(self, df):

        if self.model_config["date_column"] in list(df.columns):
            df = df.set_index(pd.to_datetime(df[self.model_config["date_column"]]))[
                [self.model_config["group_column"], self.target_label] + self.model_config["features"]]
        else:
            df = df[[self.model_config["group_column"], self.target_label] + self.model_config["features"]]

        # build average values for the target variable

        #    data.loc[data[configs["target"]] < 0, configs["target"]] = 0
        df['Target_mean'] = df.groupby([self.model_config["group_column"]])[self.target_label].transform('mean')

        if "group" in list(df.columns):
            df['Target_mean'] = df.groupby([self.model_config["date_column"], 'group']).Gross_Total.transform('mean')

            df["Target_mean_diff"] = df["Target_mean"].diff(-1)

        if "month" not in list(df.columns):
            df['month'] = pd.DatetimeIndex(df.index).month
        if 'month' not in self.model_config["dummies"]:
            self.model_config["dummies"].append("month")
        if self.model_config["dummies"] != []:
            df = self._transform_dummies(df)
        return df

    def fit_transform_normaliser(self):
        columns_to_normalize = self.model_config["normalize_columns"]
        if "Target_mean" in self.train_data.columns and "Target_mean" not in columns_to_normalize:
            columns_to_normalize.append("Target_mean")
        if "Target_mean_diff" in self.train_data.columns and "Target_mean_diff" not in columns_to_normalize:
            columns_to_normalize.append("Target_mean_diff")
        if self.target_label not in columns_to_normalize:
            columns_to_normalize.append(self.target_label)

        self.scaler = Normalizer(
            configs={"normalization-method": self.model_config["normalize_method"], "include-columns": columns_to_normalize})
        self.train_data = self.scaler.fit_transform(self.train_data)
        if self.model_config["remote-storage"] == "azure-blob":
            self.scaler.save_to_azure(self.model_config["container-name"])
        else:
            self.scaler.persist(self.model_config["output-folder"])

    def normalise(self, df):
        if self.scaler is not None:
            self.scaler.transform(df)
        else:
            try:
                if self.model_config["remote-storage"] == "azure-blob":
                    self.scaler=Normalizer.load_from_azure(self.model_config["container-name"])
                else:
                    self.scaler=Normalizer.load(self.model_config["output-folder"])
            except Exception as e:
                raise Exception("Couldn't load Normaliser. " + e)
            self.scaler.transform(df)
        return df

class BPA(AnomalyDetector):
    pass


class CPA(AnomalyDetector):
    pass


if __name__ == "__main__":
    event_conf = {
        "scan_id": "1335",
        "client_id": "1",
        "scan_type": "production",
        "payrun_id": "1",
        "period_wid": "8e19e426558e012f70b79fc456220f1a",
        "payrun_name": "bi-weekly",
        "pay_date": "2019-08-09",
        "curr_period_start_date": "2019-07-29",
        "curr_period_end_date": "2019-08-11",
        "train_period_start_date": "2018-07-30",
        "train_period_end_date": "2019-07-29",
        "gcc": "alg",
        "pay_group_name": "bi-weekly",
    }
    ipa = FPA("training_data", "current_pay_data", event_conf, "model")
    ipa.train()
    ipa.detect()

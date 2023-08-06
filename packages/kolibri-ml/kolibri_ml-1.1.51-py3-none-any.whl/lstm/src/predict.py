import os
import json
import logging
from typing import Any
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
import tqdm

from kolibri.task.tabular.regression.dnn_regression_estimator import DnnRegressionEstimator
from kolibri.backend.tensorflow.autoencoder.base_autoencoder import BaseAutoEncoder
from lstm.src.preprocess import FPAPreprocessor


@dataclass
class FPAPredictor:
    gcc_code: str
    lcc_code: str
    period_schedule_name: str
    model_config: dict
    history_pay_data: pd.DataFrame = field(repr=False)
    current_pay_data: pd.DataFrame = field(repr=False)
    auto_encoder_model: Any = field(init=False, repr=False)
    lstm_model: Any = field(init=False, repr=False)
    preprocessor: FPAPreprocessor = field(init=False, repr=False)

    model_params = {
        "columns_to_drop": ['Pay_Period', 'Period_End_Date', 'Company_Id', 'Paydate', 'Tolerance'],
        "group_by_columns": ['Period_Start_Date', 'Employee_Id', 'Employee_Status', 'Variable_Id', 'Year', 'Month',
                             'Week',
                             'Day'],
        "group_column": "Employee_Id",
        "date_column": "Period_Start_Date",
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
        "sets": ["val", "test"]
    }

    def __post_init__(self):
        self.model_params.update(self.model_config["model_params"])
        self.preprocessor = FPAPreprocessor(self.model_params)

    def __load_models(self):
        # TODO: Models to be loaded from Azure blob in the future
        root_dir = os.path.abspath(os.curdir)
        if self.lcc_code and self.gcc_code:
            model_path = os.path.join(
                root_dir, f"models/{self.gcc_code.lower()}/{self.lcc_code.lower()}/{self.period_schedule_name.lower()}"
            )
        else:
            model_path =os.path.join(root_dir, self.model_params["output-folder"])
        logging.info(f"Model Path: {model_path}")
        if self.model_params["remote-storage"]== "azure-blob":
            print('loading regression model')
            self.lstm_model = DnnRegressionEstimator.load_from_azure(self.model_params["container-name"])
            print('loading auto encoders')
            self.auto_encoder_model = BaseAutoEncoder.load_from_azure(self.model_params["container-name"])

        else:
            print('loading regression model')
            self.lstm_model = DnnRegressionEstimator.load(model_path)
            print('loading auto encoders')
            self.auto_encoder_model = BaseAutoEncoder.load_model(model_path=model_path)

    def __preprocess(self, df):
        logging.info("LSTM - Selecting gross pay components")
        preprocessed_df = self.preprocessor.select_gross_pay(df, self.lcc_code)
        logging.info("LSTM - Preprocessing data")
        preprocessed_df = self.preprocessor.preprocess_data(df)
        logging.info("LSTM - Transforming features")
        preprocessed_df = self.preprocessor.transform_features(preprocessed_df)
        logging.info("LSTM - Normalizing data")
        preprocessed_df = self.preprocessor.normalise(preprocessed_df)
        return preprocessed_df

    def __predict_values(self, to_predict, to_predict_df):
        p = self.model_params["confidence"]
        predictions = []
        for i in tqdm.tqdm(range(0, self.model_params["bayesian_samples"])):
            predictions.append(self.__predict_batch(to_predict))

        pred1 = np.asarray(predictions)
        pp = pred1.T
        if self.model_params["pooling_mode"] == "quantile":
            lower = np.quantile(pp, p / 4, axis=1)
            upper = np.quantile(pp, 1 - p / 4, axis=1)
            medium = np.quantile(pp, 0.5, axis=1)
        elif self.model_params["pooling_mode"] == "mean":
            medium = np.mean(pp, axis=1)
            std = np.std(pp, axis=1)
            lower = medium - std
            upper = medium + std

        fdf = pd.DataFrame({
            "Lower": lower,
            "Medium": medium,
            "Upper": upper
        })
        fdf = pd.concat([fdf, to_predict_df], axis=1)

        fdf[self.preprocessor.target_label] = self.preprocessor.scaler.inverse_transform_col(fdf[self.preprocessor.target_label], colName=self.preprocessor.target_label)

        return fdf.dropna()


    def __predict_batch(self, to_predict):
        Y_encoder = to_predict[0][:, :, 0]
        external_features = to_predict[1][:, :, 1:]

        XX_test = self.auto_encoder_model.encoder.predict(Y_encoder)
        Y_test_predict = self.lstm_model.predict([XX_test, external_features])
        Y_test_predict = Y_test_predict.reshape(len(Y_test_predict), )
        Y_test_predict = self.preprocessor.scaler.inverse_transform_col(Y_test_predict, colName=self.preprocessor.target_label)

        return Y_test_predict

    def predict(self, current_parsed_data=None):
        preprocessed_data=None
        if current_parsed_data is None:
            current_parsed_data = json.loads(self.current_pay_data["dataset"])
            current_df = pd.DataFrame(current_parsed_data)
            history_parsed_data = json.loads(self.history_pay_data["dataset"])
            history_df = pd.DataFrame(history_parsed_data)
            df = history_df.append(current_df)
        else:
            df=current_parsed_data
        try:
            self.__load_models()
        except Exception as e:
            logging.error("Failed to load models")
        try:
            preprocessed_data = self.__preprocess(df)
        except Exception as e:
            logging.error(f"Data pre-processing for LSTM failed - {e}")

        window_dataset = self.preprocessor.generate_dataset(preprocessed_data, split_sets=["predict"])
        predict_df = self.__predict_values(window_dataset.main, window_dataset.main_df)
        alpha = self.model_params["alpha"]
        predict_df["Delta"] = predict_df[self.preprocessor.target_label] - predict_df["Medium"]
        predict_df["Anomaly"] = False
        predict_df["Anomaly"] = ~((predict_df["Lower"] * (1 - alpha)) <= predict_df[self.preprocessor.target_label]) & (
            (predict_df["Upper"] * (1 + alpha)) >= predict_df[self.preprocessor.target_label]
        )
        predict_df.rename(columns={'id_sort': self.model_params['date_column'], 'id_group': self.model_params['group_column']}, inplace=True)

        return predict_df
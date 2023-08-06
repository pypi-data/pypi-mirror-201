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
class FPATrainer:

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
        "sets": ["val", "test"]
    }

    def __init__(self, model_config):
        self.model_params.update(model_config["model_params"])
        self.scaler = None
        self.preprocessor = FPAPreprocessor(self.model_params)


    def train(self, train_data):
        train_data=self.preprocessor.preprocess_data(train_data)
        train_data=self.preprocessor.fit_transform_features(train_data)
        train_data=self.preprocessor.fit_transform_normaliser(train_data)
        self.train_autoencoder(train_data)
        self.train_lstm(train_data)

    def train_lstm(self, train_data):
        self.model_params["horizon"] = 1
        self.model_params["min_window"] = 4
        self.model_params["max_window"] = 4
        self.model_params["loss"] = "mse"

        self.model_params["multi_variate_output"] = True

        predictor_ds = self.preprocessor.generate_dataset(train_data, split_sets=self.model_params["sets"])

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

        self.model_params["n_features"] = x_train.shape[2] - 1

        self.lstm=DnnRegressionEstimator(self.model_params)


        self.lstm.fit(X=[XX_train, external_feature_train], y=Y_label_train, X_val=[XX_val, external_feature_val],
                        y_val=Y_label_val)
        if self.model_params["remote-storage"] == "azure-blob":
            self.lstm.save_to_azure(self.model_params["container-name"])
            self.lstm = DnnRegressionEstimator.load_from_azure(self.model_params["container-name"])
        else:
            self.lstm.persist(self.model_params["output-folder"])
            self.lstm=DnnRegressionEstimator.load(self.model_params["output-folder"])

    def train_autoencoder(self, train_data):
        self.model_params['loss'] = 'mae'
        wg = self.preprocessor.generate_dataset(train_data, split_sets=self.model_params["sets"], targets=[self.preprocessor.target_label])

        x_train, y_train = wg.train
        x_val, y_val = wg.val

        Y_label_train = y_train
        Y_label_val = y_val

        Y_encoder_train = x_train[:, :, 0]
        Y_encoder_val = x_val[:, :, 0]

        Y_decoder_train = Y_encoder_train
        Y_decoder_val = Y_encoder_val

        Y_encoder_train = Y_encoder_train.reshape(-1, self.model_params["max_window"], 1)
        Y_decoder_train = Y_decoder_train.reshape(-1, self.model_params["max_window"], 1)

        input_shape = (Y_encoder_train.shape[1], Y_encoder_train.shape[2])
        output_shape = (Y_decoder_train.shape[1], Y_decoder_train.shape[2])

        auto_ae = BaseAutoEncoder(self.model_params, input_shape, output_shape)

        auto_ae.fit(Y_encoder_train, Y_decoder_train, Y_label_train, Y_encoder_val,
                    Y_decoder_val, Y_label_val, epochs=self.model_params["epochs"], patience=self.model_params["patience"])

        if self.model_params["remote-storage"] == "azure-blob":
            auto_ae.save_to_azure(self.model_params["container-name"])
        else:
            auto_ae.save(model_path=self.model_params["output-folder"])
        #reload the model to verify that we can safely load the model later
        if self.model_params["remote-storage"] == "azure-blob":
            self.auto_ae = BaseAutoEncoder.load_from_azure(self.model_params["container-name"])
        else:
            self.auto_ae=BaseAutoEncoder.load_model(model_path=self.model_params["output-folder"])
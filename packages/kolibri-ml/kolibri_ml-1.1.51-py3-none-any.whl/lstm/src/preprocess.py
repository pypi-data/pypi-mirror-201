from dataclasses import dataclass
import numpy as np
import pandas as pd

try:
    from pyml.interfaces.db import EloiseDatabase as db
    from pyml.common.templates import gross_pay_id_query_template
except:
    pass
from kolibri.preprocess.tabular.univar_outliers import UnivarOutlier
from kolibri.preprocess.tabular.data_imputer import DataImputer
from kolibri.preprocess.tabular.normalize import Normalizer
from kolibri.preprocess.tabular.one_hot_encoder_multi import MultiColomnOneHotEncoder
from kolibri.preprocess.timeseries.multi_window_generator import MultiWindowGenerator


@dataclass
class FPAPreprocessor:
    model_params: dict
    scaler=None
    target_label="_Value_"
    def select_gross_pay(self, df, lcc_code):
        if hasattr(self, "db"):
            gross_pay_id_df = db.read(gross_pay_id_query_template, {"lcc_code": lcc_code})
            gross_pay_id = gross_pay_id_df["PayComponentId"].iloc[0]
            df = df[df["Variable_Id"] == gross_pay_id]
        return df

    def preprocess_data(self, df):
        selected = [self.model_params["group_column"]]
        df = df.drop(columns=self.model_params["columns_to_drop"])
        if 'Retro_Period' in list(df.columns):
            df = df[df.Retro_Period.isna()]
        nb_timesteps=len(df[self.model_params["date_column"]].unique().tolist())
        if nb_timesteps <5:
            raise Exception(
                "Isuficient data. Number of recrods should be at least 5. "+str(nb_timesteps)+ " are provided."
            )
        index_columns=[self.model_params["date_column"], self.model_params["group_column"]]
        if self.model_params["employee_status_column"] is not None:
            selected.append(self.model_params["employee_status_column"])
            index_columns.append(self.model_params["employee_status_column"])
        df = pd.pivot_table(df,  values=self.model_params["value_column"],
                              index=index_columns,
                              columns=['Variable_Id'], aggfunc=np.sum).fillna(0).replace(np.inf, 0).reset_index()
        try:
            df[self.model_params["date_column"]] = pd.to_datetime(df[self.model_params["date_column"]])
        except Exception as e:
            print("Error in converting the date in the data: "+str(e))
        df = df.set_index(self.model_params["date_column"])
        selected.append(self.model_params["target"])
        df = df[selected]
        df.rename(columns={self.model_params["target"]: self.target_label}, inplace=True)
        #replace negative values in targets by 0
        df.loc[df[self.target_label] < 0, self.target_label] = 0
        outliers = UnivarOutlier(params={"include-columns": [self.target_label]})
        df = outliers.fit_transform(df)
        imputer = DataImputer()
        return imputer.fit_transform(df)

    def fit_transform_dummies(self, df):
        self.one_hot_encode = MultiColomnOneHotEncoder(self.model_params)
        self.one_hot_encode.fit(data= df)
        if self.model_params["remote-storage"] == "azure-blob":
            self.one_hot_encode.save_to_azure(self.model_params["container-name"])
        else:
            self.one_hot_encode.persist(self.model_params["output-folder"])
        return self.one_hot_encode.transform(data=df)

    def transform_dummies(self, df):
        if not hasattr(self, "one_hot_encode"):
            if self.model_params["remote-storage"] == "azure-blob":
                self.one_hot_encode = MultiColomnOneHotEncoder.load_from_azure(self.model_params["container-name"])
            else:
                self.one_hot_encode = MultiColomnOneHotEncoder.load(self.model_params["output-folder"])
        return self.one_hot_encode.transform(data=df)

    def fit_transform_features(self, df):
        if self.model_params["date_column"] in list(df.columns):
            df = df.set_index(pd.to_datetime(df[self.model_params["date_column"]]))[
                [self.model_params["group_column"], self.target_label] + self.model_params["features"]]
        else:
            df = df[[self.model_params["group_column"], self.target_label] + self.model_params["features"]]
        df['Target_mean'] = df.groupby([self.model_params["group_column"]])[self.target_label].transform('mean')
        if "group" in list(df.columns):
            df['Target_mean'] = df.groupby([self.model_params["date_column"], 'group']).Gross_Total.transform('mean')
            df["Target_mean_diff"] = df["Target_mean"].diff(-1)
        if "month" not in list(df.columns):
            df['month'] = pd.DatetimeIndex(df.index).month
        self.model_params["dummies"].append("month")
        if self.model_params["dummies"] != []:
            df = self.fit_transform_dummies(df)
        return df

    def transform_features(self, df):

        if self.model_params["date_column"] in list(df.columns):
            df = df.set_index(pd.to_datetime(df[self.model_params["date_column"]]))[
                [self.model_params["group_column"], self.target_label] + self.model_params["features"]]
        else:
            df = df[[self.model_params["group_column"], self.target_label] + self.model_params["features"]]
        df['Target_mean'] = df.groupby([self.model_params["group_column"]])[self.target_label].transform('mean')
        if "group" in list(df.columns):
            df['Target_mean'] = df.groupby([self.model_params["date_column"], 'group']).Gross_Total.transform('mean')
            df["Target_mean_diff"] = df["Target_mean"].diff(-1)
        if "month" not in list(df.columns):
            df['month'] = pd.DatetimeIndex(df.index).month
        if 'month' not in self.model_params["dummies"]:
            self.model_params["dummies"].append("month")
        if self.model_params["dummies"] != []:
            df = self.transform_dummies(df)
        return df

    def fit_transform_normaliser(self, train_data):
        columns_to_normalize = self.model_params["normalize_columns"]
        if "Target_mean" in train_data.columns and "Target_mean" not in columns_to_normalize:
            columns_to_normalize.append("Target_mean")
        if "Target_mean_diff" in train_data.columns and "Target_mean_diff" not in columns_to_normalize:
            columns_to_normalize.append("Target_mean_diff")
        if self.target_label not in columns_to_normalize:
            columns_to_normalize.append(self.target_label)

        self.scaler = Normalizer(
            configs={"normalization-method": self.model_params["normalize_method"], "include-columns": columns_to_normalize})
        train_data = self.scaler.fit_transform(train_data)
        if self.model_params["remote-storage"] == "azure-blob":
            self.scaler.save_to_azure(self.model_params["container-name"])
        else:
            self.scaler.persist(self.model_params["output-folder"])
        return train_data
    def normalise(self, df):
        if self.scaler is not None:
            self.scaler.transform(df)
        else:
            try:
                if self.model_params["remote-storage"] == "azure-blob":
                    self.scaler=Normalizer.load_from_azure(self.model_params["container-name"])
                else:
                    self.scaler=Normalizer.load(self.model_params["output-folder"])
            except Exception as e:
                raise Exception("Couldn't load Normaliser. " + e)
            self.scaler.transform(df)
        return df

    def generate_dataset(self, df, split_sets=["test", "val"], targets=None):

        max_win = self.model_params["max_window"]
        if self.model_params["max_window"] == None:
            max_win = self.model_params["min_window"]
        config = {
                "target": targets,
                "group": self.model_params["group_column"],
                "timestamp": self.model_params["date_column"],
                "horizon": self.model_params["horizon"],
                "split_column": None,
                "max-window-history": max_win,
                "min-window-history": self.model_params["min_window"],
                "n_jobs": self.model_params["n_jobs"] if "n_jobs" in self.model_params else 1,
                "sets": split_sets
            }
        return MultiWindowGenerator(data=df.reset_index(), configs=config)

from lstm.src.predict import FPAPredictor
from lstm.src.train import FPATrainer
import pandas as pd
import os

os.environ[
    'AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=mentis1;AccountKey=8LHRahnNg+uIPiJVMsdxKZlILKYrmcPnwJ+ZYZiizI4EkDBmDrCU38ZTQwbNSkvxeQidIBnH+SpEmq0vq+s0pw==;EndpointSuffix=core.windows.net"

train_data = pd.read_csv(
    "/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri/kolibri-ml/lstm/notebooks/data/history_data_14032022.csv")  # .sample(5000)

current_pay_data = pd.read_csv(
    "/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri/kolibri-ml/lstm/notebooks/data/Test_data_5_weeks.csv")

model_config = {"model_params":{
    "columns_to_drop": [],
    "group_by_columns": ['Period_Start_Date', 'Employee_Id', 'Employee_Status', 'Variable_Id'],
    "group_column": "Employee_Id",
    "date_column": "Original_Start_Date",
    "features": ["Employee_Status"],
    "epochs": 4,
    "target": 35,
    "value_column":"Value",
    "dummies": ["Employee_Status"],
    "normalize_columns": [],
    "horizon": 1,
    "min_window": 1,
    "max_window": 4,
    "pre-train": True,
    "train": True,
    "n_jobs": 1,
    "container-name": "lstmmodel",
    "remote-storage": None, #"azure-blob",
    "multi_variate_output": False,
    "output-folder": "output"
}}


#trainer=FPATrainer(model_config=model_config)
#trainer.train(train_data)
predictor = FPAPredictor(
    gcc_code=None,
    lcc_code=None,
    period_schedule_name=None,
    model_config=model_config,
    history_pay_data=train_data,
    current_pay_data=current_pay_data,
)
results = predictor.predict(current_pay_data)


print(results)
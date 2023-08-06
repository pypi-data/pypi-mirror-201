import logging

import pandas as pd

from lstm.src.lstm_predictor import FPA

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


import os

if __name__ == "__main__":

    model_config = {
        "columns_to_drop": ["gcc", "lcc", "Period_Number"],
        "group_by_columns": ['Period_Start_Date', 'Employee_HRIS_Id', 'Employee_Status'],
        "group_column": "Employee_HRIS_Id",
        "date_column": "Period_Start_Date",
        "features": ["Employee_Status"],
        "epochs": 4,
        "target": "NetPay",
        "dummies": ["Employee_Status"],
        "normalize_columns": [],
        "horizon": 1,
        "min_window": 1,
        "max_window": 3,
        "pre-train": True,
        "train": True,
        "n_jobs": -1,
        "container-name": "lstmmodel",
        "sets": ["val"],
        "remote-storage": "",#"azure-blob",
        "multi_variate_output": False,
        "output-folder": "/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/outputs"
    }
    os.environ[
        'AZURE_STORAGE_CONNECTION_STRING'] = "DefaultEndpointsProtocol=https;AccountName=mentis1;AccountKey=8LHRahnNg+uIPiJVMsdxKZlILKYrmcPnwJ+ZYZiizI4EkDBmDrCU38ZTQwbNSkvxeQidIBnH+SpEmq0vq+s0pw==;EndpointSuffix=core.windows.net"

    train_data=pd.read_csv("/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/notebooks/data/bay_sa.csv")#.sample(5000)

    current_data= pd.read_csv("/Users/mohamedmentis/Dropbox/Mac (2)/Documents/Mentis/Development/Python/kolibri-ml/lstm/notebooks/data/bay_sa.csv")

    fpa=FPA(train_data, model_config)
    print(fpa.train())
    model=fpa.load_model()
    res=fpa.detect(current_data)

    print(res)



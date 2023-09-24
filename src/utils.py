import os 
import sys
import pymysql
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


#Reading out data from .env file for MYSQL Credentials
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

#Function for reading data from MYSQL workbench
def read_sql_data():
    logging.info("Reading SQL Database")
    
    try:
        logging.info("Trying to connect mySQL workbench")
        mydb = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = db
        )
        logging.info("Connection establish")
        
        df_train = pd.read_sql_query("select * from train1", mydb)
        logging.info("Train file readed")
        df_test = pd.read_sql_query("select * from test1", mydb)
        logging.info("Test file readed")
        
        return df_train, df_test
        
    except Exception as e:
        logging.info("Error occured in reading data from MYSQL database")
        raise CustomException(e, sys)
    
    
def save_object(file_path, obj):
    
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok = True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
                   
    except Exception as e:
        raise CustomException(e, sys)
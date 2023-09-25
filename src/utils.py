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
    

def evaluate_model(X_train, y_train, X_test, y_test, models,param):
    try:
        report = {} #Creating Dict report
        logging.info("Creating model report")
        for i in range(len(models)):
            model = list(models.values())[i] #Listed all models
            logging.info("Model Listd in Dictionary")
            para=param[list(models.keys())[i]]
            
            
            
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            logging.info(f"{model} trained")
            
            #Predicting value
            y_test_pred = model.predict(X_test)
            logging.info(f"{model} predicted")
            
            #getting accuracy score
            test_model_score = r2_score(y_test, y_test_pred)
            logging.info(f"{model} accuracy score generated")
            
            report[list(models.keys())[i]] = test_model_score
            logging.info("Report generated")
            
        return report

    except Exception as e:
        logging.info("Exception as model training step")
        raise CustomException(e, sys)
    
#Defining Function for loading the object
def load_object(file_path):
    
    try:
        logging.info("Load oject started")        
        with open(file_path, "rb") as file_obj:
            logging.info("Pickle file loaded")
            return pickle.load(file_obj)
           
    except Exception as e:
        logging.info("Exception in utils load object")
        raise CustomException(e, sys)    
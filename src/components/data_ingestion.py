#importing libraries
import os 
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import read_sql_data

#Data Ingestion Config Class
@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join("artifacts", "train.csv")
    logging.info("Train file loaded")
    test_data_path:str = os.path.join("artifacts", "test.csv")
    logging.info("Test file loaded")


#Creating class for Data Ingestion
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        logging.info("Data Ingestion config class initiated")
        
    def initiate_data_ingestion(self):
        try:
            logging.info("Reading Data Step started")
            df = read_sql_data()
            logging.info("Reading from SQL database")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok = True)
            logging.info("Directory made for Train path")
            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok = True)
            logging.info("Directory made for Test path")
            
            df[0].to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            logging.info("Train file saved as csv")
            df[1].to_csv(self.ingestion_config.test_data_path, index = False, header = True)
            logging.info("Test file saved as csv")
            
            logging.info("Data Ingestion Completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.info("Error occur at Data Ingestion Class")
            raise CustomException(e, sys)
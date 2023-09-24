from src.logger import logging
from src.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    
    obj = DataIngestion() 
    train_data_path, test_data_path = obj.initiate_data_ingestion() 
    logging.info("Data Ingestion step Completed") 
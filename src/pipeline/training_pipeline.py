from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

if __name__ == "__main__":
    
    data_ingestion = DataIngestion()
    train_data, test_data = data_ingestion.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_array, test_array = data_transformation.initiate_data_transformation(train_data, test_data)
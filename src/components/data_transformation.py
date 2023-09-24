import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_trasnformer_object(self):
        try:
            num_cols = ['Engine_no', 'Cycle_no',
            'LPC_outlet_temperature',
            'HPC_outlet_temperature', 'LPT_outlet_temperature',
            'HPC_outlet_pressure',
            'Physical_fan_speed', 'Physical_core_speed', 
            'HPC_outlet_static_pressure', 'Fuel_flow_ratio', 'Fan_speed',
            'Bypass_ratio', 'Bleed_enthalpy',
            'High_pressure_cool_air_flow', 'Low_pressure_cool_air_flow']
            
            num_pipeline = Pipeline(
                
                steps = [
                    ("scaler", RobustScaler()),
                    ("PCA", PCA(n_components=8))
                    
                ]
            )
            
            logging.info("Pipeline created")
            
            preprocessor = ColumnTransformer(
                
                [
                    ("num_pipeline", num_pipeline, num_cols)
                ]
            )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            train_df["RUL"][train_df["RUL"] > 103] = 103
            test_df["RUL"][test_df["RUL"] > 103] = 103
            
            logging.info("Train & test data readed")
            
            target_column_name = "RUL"
            drop_cols = [
                'Setting_1', 'Setting_2', 'Setting_3', 'Fan_inlet_temperature', 'Fan_inlet_pressure', 
                'Bypass_duct_pressure', 'Engine_pressure_ratio', 'Core_speed', 'Burner_fuel_air_ratio', 
                'Required_fan_speed', 'Required_fan_conversion_speed']  
            
            
            input_feature_train_df = train_df.drop(columns=[target_column_name] + drop_cols)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name] + drop_cols)
            target_feature_test_df = test_df[target_column_name]
            
            
            preprocessor_obj = self.get_data_trasnformer_object()
            logging.info("Applying preprocessing obj on train & test dataframe")
            
        #Transforming into Preprocessor object to data
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df) #train data
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df) #test data
            logging.info("Preprocessing applied to training & test datasets") 
            
            #Converting into numpy array for train & test data
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)] #train array 
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)] #test array
            logging.info("Data transfom into the array")
            
            #function from utils to save the preprocessor file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            logging.info("Preprocessor file saved as Pickle file")
            
            return (
                train_arr,
                test_arr
            )
            
            
        except Exception as e:
            raise CustomException(e, sys)
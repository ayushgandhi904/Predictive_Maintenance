import os, sys
from src.exception import CustomException 
from src.logger import logging 
from src.utils import load_object 
import pandas as pd

#Creating class for prediction pipeline
class PredictPipeline:
    
    def __init__(self): 
        pass    
    
    def predict(self, features):
        try:   
            logging.info("Starting for prediction path")
            
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl") 
            model_path = os.path.join("artifacts", "model.pkl") 
            logging.info("Preprocessor & Model path joined")
            
            preprocessor = load_object(preprocessor_path) 
            model = load_object(model_path)
            logging.info("Preprocessor object loaded")
            
            data_scaled = preprocessor.transform(features) 
            logging.info("Features transform through Preprocessor")

            pred = model.predict(data_scaled)
            logging.info("Output predicted through model")
            
            return pred
        
        except Exception as e:
            logging.info("Error occur in Prediction step")
            raise CustomException(e, sys)
        
#Defining the custom class to input data through form
class CustomData: 

    def __init__(self,
                 Engine_no:int,
                 Cycle_no:int,
                 LPC_outlet_temperature:float,
                 HPC_outlet_temperature:float,
                 LPT_outlet_temperature:float,
                 HPC_outlet_pressure:float,
                 Physical_fan_speed:float,
                 Physical_core_speed:float,
                 HPC_outlet_static_pressure:float,
                 Fuel_flow_ratio:float,
                 Fan_speed:float,
                 Bypass_ratio:float,
                 Bleed_enthalpy:float,
                 High_pressure_cool_air_flow:float,
                 Low_pressure_cool_air_flow:float):
        
        self.engine_no = Engine_no
        self.cycle_no= Cycle_no
        self.lpc_outlet_temperature = LPC_outlet_temperature
        self.hpc_outlet_temperature = HPC_outlet_temperature
        self.lpt_outlet_temperature = LPT_outlet_temperature
        self.hpc_outlet_pressure = HPC_outlet_pressure
        self.physical_fan_speed= Physical_fan_speed
        self.physical_core_speed = Physical_core_speed
        self.hpc_outlet_static_pressure = HPC_outlet_static_pressure
        self.fuel_flow_ratio = Fuel_flow_ratio
        self.fan_speed= Fan_speed
        self.bypass_ratio = Bypass_ratio
        self.bleed_enthalpy = Bleed_enthalpy
        self.high_pressure_cool_air_flow= High_pressure_cool_air_flow
        self.low_pressure_cool_air_flow = Low_pressure_cool_air_flow
        
        
        #defining function to store obtain data in the form of the dataframe
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "engine_no": [self.engine_no],
                "cycle_no": [self.cycle_no],
                "lpc_outlet_temperature": [self.lpc_outlet_temperature],
                "hpc_outlet_temperature": [self.hpc_outlet_temperature],
                "lpt_outlet_temperature": [self.lpt_outlet_temperature],
                "hpc_outlet_pressure": [self.hpc_outlet_pressure],
                "physical_fan_speed": [self.physical_fan_speed],
                "physical_core_speed": [self.physical_core_speed],
                "hpc_outlet_static_pressure": [self.hpc_outlet_static_pressure],
                "fuel_flow_ratio": [self.fuel_flow_ratio],
                "fan_speed": [self.fan_speed],
                "bypass_ratio": [self.bypass_ratio],
                "bleed_enthalpy": [self.bleed_enthalpy],
                "high_pressure_cool_air_flow": [self.high_pressure_cool_air_flow],
                "low_pressure_cool_air_flow": [self.low_pressure_cool_air_flow]
            }
          

            df = pd.DataFrame(custom_data_input_dict)
            return df     
        
        except CustomException as e:
            logging.info("Exception occured in prediction pipeline")
            raise CustomException(e, sys)
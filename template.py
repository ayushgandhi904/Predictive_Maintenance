from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "predictive_maintenance"

list_of_files = [
    "Dockerfile",
    "setup.py",
    "app.py",
    f"src/__init__.py",
    f"src/logger.py",
    f"src/exception.py",
    f"src/utils.py",
    f"src/components/__init__.py",
    f"src/components/data_ingestion.py",
    f"src/components/data_transformation.py",
    f"src/components/model_trainer.py",
    f"src/pipeline/__init__.py",
    f"src/pipeline/training_pipeline.py",
    f"src/pipeline/prediction_pipeline.py",
    f"notebooks/EDA.ipynb",
    f"notebooks/1.data_ingestion.ipynb",
    f"notebooks/2.data_transformation.ipynb",
    f"notebooks/3.model_trainer.ipynb",
    ".env",
    f"templates/index.html"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} is already exists")
from flask import Flask,request,render_template #for initializing flask & render the html templates
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

application=Flask(__name__)

app=application

@app.route('/')
def home_page():
    return render_template('index.html') 

@app.route("/predict", methods = ["GET", "POST"])
def predict_datapoint(): 
    if request.method == "GET":
        return render_template("form.html") 
    
    else:

        data = CustomData(
            Engine_no = float(request.form.get("Engine_no")),
            Cycle_no = float(request.form.get("Cycle_no")),
            LPC_outlet_temperature = float(request.form.get("LPC_outlet_temperature")),
            HPC_outlet_temperature = float(request.form.get("HPC_outlet_temperature")),
            LPT_outlet_temperature = float(request.form.get("LPT_outlet_temperature")),
            HPC_outlet_pressure = float(request.form.get("HPC_outlet_pressure")),
            Physical_fan_speed = float(request.form.get("Physical_fan_speed")),
            Physical_core_speed = float(request.form.get("Physical_core_speed")),
            HPC_outlet_static_pressure = float(request.form.get("HPC_outlet_static_pressure")),
            Fuel_flow_ratio = float(request.form.get("Fuel_flow_ratio")),
            Fan_speed = float(request.form.get("Fan_speed")),
            Bypass_ratio = float(request.form.get("Bypass_ratio")),
            Bleed_enthalpy = float(request.form.get("Bleed_enthalpy")),
            High_pressure_cool_air_flow = float(request.form.get("High_pressure_cool_air_flow")),
            Low_pressure_cool_air_flow  = float(request.form.get("Low_pressure_cool_air_flow"))       
        )
        
        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data) #to predict the final output
        
        if pred <25: 
            results = round(pred[0])
            return render_template("danger.html", final_result = results) 
        
        elif pred >60:
            results = round(pred[0])
            return render_template("safe.html", final_result = results)
        
        else:
            results = round(pred[0])
            return render_template("warning.html", final_result = results)
        # results = round(pred[0])
        # return render_template('results.html',final_result=results)
#to initalize the app when run
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000, debug= True)
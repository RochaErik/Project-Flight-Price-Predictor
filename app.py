import pandas as pd
from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')

@app.route('/prices')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['GET', 'POST']) 
@cross_origin()
def predict():
    if request.method == 'POST':

        # DEPARTURE Date 
        date_dep = request.form["Dep_Time"]

        # Date day
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)

        # Date month
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
     
        # Departure Time
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
       
        # ARRIVAL date
        date_arrival = request.form["Arrival_Time"]

        # Arrival Time
        Arrival_hour = int(pd.to_datetime(date_arrival, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arrival, format ="%Y-%m-%dT%H:%M").minute)
     
        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour) # WARNING: Maybe this is wrong! Need to review it!!
        dur_min = abs(Arrival_min - Dep_min)          

        # --------------- Total Stops ---------------

        total_stops = request.form["stops"]

        if (total_stops=='Total_Stops_0'):
            Total_Stops_non_stop = 1
            Total_Stops_2_stops = 0
            Total_Stops_3_stops = 0
            Total_Stops_4_stops = 0
        
        elif (total_stops=='Total_Stops_1'):
            Total_Stops_non_stop = 0
            Total_Stops_2_stops = 0
            Total_Stops_3_stops = 0
            Total_Stops_4_stops = 0
        
        elif (total_stops=='Total_Stops_2'):
            Total_Stops_non_stop = 0
            Total_Stops_2_stops = 1
            Total_Stops_3_stops = 0
            Total_Stops_4_stops = 0
        
        elif (total_stops=='Total_Stops_3'):
            Total_Stops_non_stop = 0
            Total_Stops_2_stops = 0
            Total_Stops_3_stops = 1
            Total_Stops_4_stops = 0
        
        elif (total_stops=='Total_Stops_4'):
            Total_Stops_non_stop = 0
            Total_Stops_2_stops = 0
            Total_Stops_3_stops = 0
            Total_Stops_4_stops = 1
        
        
        # --------------- Airlines ---------------------

        airline = request.form['airline']

        if(airline=='LATAM'):
            Latam = 1
            Azul = 0
            Gol = 0
            Voe_Pass = 0      
     
          
        elif (airline=='Azul'):
            Latam = 0
            Azul = 1
            Gol = 0
            Voe_Pass = 0
             
            
        elif (airline=='Gol'):
            Latam = 0
            Azul = 0
            Gol = 1
            Voe_Pass = 0
             
            
        elif (airline=='VoePass'):
            Latam = 0
            Azul = 0
            Gol = 0
            Voe_Pass = 1
             
            
        elif (airline=='Avianca Brasil'):
            Latam = 0
            Azul = 0
            Gol = 0
            Voe_Pass = 0
            

        # --------------- Source ---------------------

        Source = request.form["Source"]

        if (Source == 'Rio Grande do Sul'):
            s_Rio_Grande_do_Sul = 1
            s_Rio_de_Janeiro = 0
            s_Santa_Catarina = 0
            s_Vitória = 0

        elif (Source == 'Rio de Janeiro'):
            s_Rio_Grande_do_Sul = 0
            s_Rio_de_Janeiro = 1
            s_Santa_Catarina = 0
            s_Vitória = 0

        elif (Source == 'Santa Catarina'):
            s_Rio_Grande_do_Sul = 0
            s_Rio_de_Janeiro = 0
            s_Santa_Catarina = 1
            s_Vitória = 0

        elif (Source == 'Vitória'):
            s_Rio_Grande_do_Sul = 0
            s_Rio_de_Janeiro = 0
            s_Santa_Catarina = 0
            s_Vitória = 1

        elif (Source == 'Belo Horizonte'):
            s_Rio_Grande_do_Sul = 0
            s_Rio_de_Janeiro = 0
            s_Santa_Catarina = 0
            s_Vitória = 0

        # --------------- Destination ---------------------    

        Destination = request.form["Destination"]

        if (Destination == 'Rio de Janeiro'):
            d_Rio_de_Janeiro = 1
            d_Salvador = 0
            d_São_Paulo = 0
            d_Vitória = 0
        
        elif (Destination == 'Salvador'):
            d_Rio_de_Janeiro = 0
            d_Salvador = 1
            d_São_Paulo = 0
            d_Vitória = 0

        
        elif (Destination == 'São Paulo'):
            d_Rio_de_Janeiro = 0
            d_Salvador = 0
            d_São_Paulo = 1
            d_Vitória = 0

        elif (Destination == 'Vitória'):
            d_Rio_de_Janeiro = 0
            d_Salvador = 0
            d_São_Paulo = 0
            d_Vitória = 1

        elif (Destination == 'Belo Horizonte'):
            d_Rio_de_Janeiro = 0
            d_Salvador = 0
            d_São_Paulo = 0
            d_Vitória = 0

        # ----------- MODEL --------------

        prediction=model.predict([[
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Total_Stops_2_stops,
            Total_Stops_3_stops,
            Total_Stops_4_stops,
            Total_Stops_non_stop,
            Azul,
            Gol,
            Latam,
            Voe_Pass,
            s_Rio_Grande_do_Sul,
            s_Rio_de_Janeiro,
            s_Santa_Catarina,
            s_Vitória,
            d_Rio_de_Janeiro,
            d_Salvador,
            d_São_Paulo,
            d_Vitória
        ]])

        output=round(prediction[0],2)

        return render_template('index.html',prediction_text="Your flight will cost: R${}.".format(output))


    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)


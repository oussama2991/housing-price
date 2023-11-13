from flask import Flask, render_template, request

import joblib
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load(open('price_housing_2023.pkl', 'rb'))

# Function to preprocess user input and make predictions
def predict_price(property_type, ppd_category, duration, month, Price_Category_City, old_new):
    # Create a dictionary with integer column names
    input_data = {
        'Old/New': [int(old_new)],
        'Month': [int(month)],
        'Detached': [int(property_type == 'Detached')],
        'Flats/Maisonettes': [int(property_type == 'Flats/Maisonettes')],
        'Other': [int(property_type == 'Other')],
        'Semi-Detached': [int(property_type == 'Semi-Detached')],
        'Terraced': [int(property_type == 'Terraced')],
        'Freehold': [int(duration == 'Freehold')],
        'Leasehold': [int(duration == 'Leasehold')],
        'Standard Price': [int(ppd_category == 'Standard Price Paid')],
        'Additional Price': [int(ppd_category == 'Additional Price Paid')],
        'Price_Category_City': [int(Price_Category_City)]
    }

    # Convert the dictionary to a DataFrame
    input_data = pd.DataFrame(input_data)

    # Predict using the model
    prediction = model.predict(input_data)
    return prediction[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        property_type = request.form['property_type']
        ppd_category = request.form['ppd_category']
        duration = request.form['duration']
        month = request.form['month']
        Price_Category_City = request.form['Price_Category_City']
        old_new = request.form['old_new']

        prediction = predict_price(property_type, ppd_category, duration, month, Price_Category_City, old_new)
        return render_template('index.html', prediction=round(prediction, 2))
    
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)

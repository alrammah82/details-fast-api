# 1. Library imports
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
import numpy as np
import pandas as pd
import math
from sklearn import preprocessing
from utils import rfm, discount
# 2. Create the app object
app = FastAPI()

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
async def index():
    return {'message': 'Wellcom'}

# RFM Classification endpoint
@app.post('/rfm')
async def rfm_classification(file:UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except:
        raise HTTPException(
            status_code= 404,
            detail= 'Not csv file'
        )    
    
    # Calculating the rfm
    df = rfm.calculate_rfm(df)
    # Normlizing the rfm
    df = rfm.calculate_rfm_logs(df)
    # Divide rfm into 4 categories
    df = rfm.calculate_4_categories(df)
    # Create quartiles named RFM_segment
    df = rfm.rfm_segment(df)
    # Calculate rfm score by summing up the RFM quartile metrics
    df = rfm.rfm_score(df)
    # Create a general segment
    df = rfm.calculate_general_segment(df)
    # Unite cities
    df = rfm.calculate_city(df)
    # Unite payment methods
    df = rfm.calculate_payment_method(df)
    # Convert Dataframe to json format 
    data = df.to_json(orient='records')

    return data

# Discount Classification endpoint
@app.post('/discount')
async def discount_classification(file:UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
    except:
        raise HTTPException(
            status_code= 404,
            detail= 'Not csv file'
        )    
    
    # Calculate the frequency
    df = discount.calculate_frequency(df)
    # Gets transaction with discounts only
    df = discount.is_discount(df)
    # Calculate number of discounts
    df = discount.calculate_number_of_discounts(df)
    # Calculate amount of discount
    df = discount.calculate_amount_of_discount(df)
    # Calculate the amount
    df = discount.calculate_amount(df)
    # Calculate discounts percentege
    df = discount.calculate_discounts_percentege(df)
    # Create discount segment
    df = discount.calculate_discount_segment(df)
    # Drop unnecessary column
    df = discount.drop_unnecessary_column(df)
    # Convert Dataframe to json format 
    data = df.to_json(orient='records')
    return data


    

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload
import telegram_send
import time
import requests
import datetime as dt
import pandas as pd
x = 0
payload={}
headers = {
  'authority': 'cdn-api.co-vin.in',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
  'origin': 'https://www.cowin.gov.in',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.cowin.gov.in/',
  'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
}
pincodes = ['400601','400602','400603','400604','400605','400606','400607']
while x<50000:
    date = dt.date.today().strftime("%d-%m-%Y")
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=392&date=" + str(date)
    response = requests.get(url, headers=headers, data=payload)
    a = time.time()
    response.raise_for_status()
    x=x+1
    print("Run No: "+str(x))
    data = response.json()
    df = pd.DataFrame(data['centers'])
    rslt_df = df[df['pincode'].isin(pincodes)]
    # list_of_sessions = rslt_df.sessions.to_list()
    # for sessions in list_of_sessions:
    sessions = []
    for index, row in rslt_df.iterrows():
        df_index= index
        sessions.append(row['sessions'])
        for s in sessions:
            for session in s:
                if session['min_age_limit']==18:
                    if session['available_capacity'] >0:
                        # session_id = session['session_id']
                        availability = session['available_capacity']
                        center_name = df.iloc[df_index]['name']
                        pincode = df.iloc[df_index]['pincode']
                        fee_type = df.iloc[df_index]['fee_type']
                        date = session['date']
                        txt = "Center: "+str(center_name)+"\nPincode: "+str(pincode)+"\nFee Type: "+str(fee_type)+"\nAvailable Capacity: "+str(availability)+"\nDate: "+str(date)+"\nSign up: https://selfregistration.cowin.gov.in/"
                        telegram_send.send(messages=[txt])
    print('Thane Done. Sleeping')
    b = time.time()
    if b-a<60:
        time.sleep(round(60-(b-a)))
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=395&date=" + str(date)
    response = requests.get(url, headers=headers, data=payload)
    a = time.time()
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data['centers'])
    rslt_df = df
    sessions = []
    for index, row in rslt_df.iterrows():
        df_index = index
        sessions.append(row['sessions'])
        for s in sessions:
            for session in s:
                if session['min_age_limit'] == 18:
                    if session['available_capacity'] > 0:
                        # session_id = session['session_id']
                        availability = session['available_capacity']
                        center_name = df.iloc[df_index]['name']
                        pincode = df.iloc[df_index]['pincode']
                        fee_type = df.iloc[df_index]['fee_type']
                        date = session['date']
                        txt = "Center: " + str(center_name) + "\nPincode: " + str(pincode) + "\nFee Type: " + str(
                            fee_type) + "\nAvailable Capacity: " + str(availability) + "\nDate: " + str(
                            date) + "\nSign up: https://selfregistration.cowin.gov.in/"
                        telegram_send.send(messages=[txt])
    print('Mumbai Done. Sleeping.')
    b = time.time()
    if b - a < 60:
        time.sleep(round(60 - (b - a)))
    # time.sleep(60)

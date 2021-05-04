import telegram_send #needs to be configured before using. https://pypi.org/project/telegram-send/
import time
import requests
import datetime as dt

x = 0 #counter for how many loops have been completed

##This part is for the HTTP Request
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
##change to your location's pincodes
pincodes = [400601,400602,400603,400604,400605,400606,400607,400706,401101]

while True:
    
    x = x+1
    print("Run Number "+str(x))
    
    date = dt.date.today().strftime("%d-%m-%Y")  #Date for the url
    
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=392&date=" + str(date)
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()
    centers = data['centers']
    
    #block of code for region with pincode requirements
    for center in centers:
        # print(center['name'])
        for i in pincodes:
            if center['pincode'] == i: #filter centers in pincode list
                sessions = center['sessions']
                for session in sessions:
                    if session['min_age_limit']==18:  #filter sessions with min age = 18
                        if session['available_capacity'] >0: #filter sessions with availability
                            # session_id = session['session_id']
                            availability = session['available_capacity']
                            center_name = center['name']
                            pincode = center['pincode']
                            fee_type = center['fee_type']
                            vaccine = session['vaccine']
                            date = session['date']
                            txt = "Vaccine: "+vaccine+"\nCenter: "+str(center_name)+"\nPincode: "+str(pincode)+"\nFee Type: "+str(fee_type)+"\nAvailable Capacity: "+str(availability)+"\nDate: "+str(date)+"\nSign up: https://selfregistration.cowin.gov.in/"
                            telegram_send.send(messages=[txt])
                            # print(txt)
                            
                            
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=395&date=" + str(date)
    response = requests.get(url, headers=headers, data=payload)
    response.raise_for_status()
    data = response.json()
    centers = data['centers']
    
    #code without pincode restrictions
    for center in centers:
        # print(center['name'])
        sessions = center['sessions']
        for session in sessions:
                    if session['min_age_limit']==18:
                        if session['available_capacity'] >0:
                            # session_id = session['session_id']
                            availability = session['available_capacity']
                            center_name = center['name']
                            pincode = center['pincode']
                            fee_type = center['fee_type']
                            vaccine = session['vaccine']
                            date = session['date']
                            txt = "Vaccine: "+vaccine+"\nCenter: "+str(center_name)+"\nPincode: "+str(pincode)+"\nFee Type: "+str(fee_type)+"\nAvailable Capacity: "+str(availability)+"\nDate: "+str(date)+"\nSign up: https://selfregistration.cowin.gov.in/"
                            telegram_send.send(messages=[txt])
                            # print(txt)
    time.sleep(15)

#!/usr/bin/python3

##--------------------------------------------------------------------------------------------##
##  Author      : Ankit Vashistha                                                             ##
##  Version     : 2.2                                                                         ##
##  API         : COWIN Public API, Telegram API                                              ##
##  DISCLAIMER  : This piece of code is written to demonstrate the usage of COWIN OPEN API.   ##
##                It is not meant or should NEVER be used to abuse the system. Please note    ##
##                there are lakhs or even crores of users trying to register themselves for   ##
##                vaccination on COWIN site everyday. Please be compassionate and limit the   ##
##                testing to COWIN's Dev environment API. See COWIN website for more details. ##
##--------------------------------------------------------------------------------------------##

import requests
import json
import time as t
import hashlib
import datetime
from secrets import BOT_CHATID,BOT_TOKEN,AGENT_SECRET,MOBILE_NUMBER,DISTRICT_ID,PINCODE

## USER SPECIFIC VARIABLES - UPDATE secrets.py BEFORE EXECUTION.
## Get from secrets file. Get your Agent Secret from COWIN site using browser's Developer Plugin >> Network >> Headers >> secret.
NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
schedule_date_today = NextDay_Date.strftime ('%d-%m-%Y')
agent_secret = AGENT_SECRET
schedule_district_id = DISTRICT_ID
mobile_number = int(MOBILE_NUMBER)


## COWIN API Endpoints - Do NOT Change | SEE: https://apisetu.gov.in/public/marketplace/api/cowin
getOTPurl = 'https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP'
validateOTPurl = 'https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP'
# To find schedules by PIN, update below URL to use 'public/findByPin?pincode=<PINCODE>' instead of 'sessions/public/calendarByDistrict?district_id='
getSchedulesurl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=" + schedule_district_id + "&date=" + schedule_date_today
getBeneficiariesurl = "https://cdn-api.co-vin.in/api/v2/appointment/beneficiaries"
scheduleAppointmenturl = "https://cdn-api.co-vin.in/api/v2/appointment/schedule"


# Keep Alive Session
s = requests.Session()


## SEND MESSAGE ABOUT SUITABLE SCHEDULE ON TELEGRAM BOT
def telegram_bot_sendtext(BOT_MESSAGE):
    # https://api.telegram.org/bot<yourtoken>/getUpdates
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + BOT_CHATID + '&parse_mode=Markdown&text=' + BOT_MESSAGE
    response = s.get(send_text)
    return response.json()



## GENERATE OTP ON MOBILE NUMBER
payload = json.dumps({
  'mobile': mobile_number,
  'secret': agent_secret
})

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37',
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

response = s.post(getOTPurl, headers=headers, data=payload)

print("\n[GET OTP] RESULT:: Status Code: {} Reason: {}\n".format(response.status_code,response.reason))
txnId = response.json()['txnId']



## CONFIRM OTP FROM SMS RECEIVED ON MOBILE NUMBER - WE GET A TOKEN HERE USED IN getBeneficiaries AND scheduleAppointment CALLS AS BEARER TOKEN
# Read OTP from stdin
OTP = input('[USER INPUT] Please enter the COWIN OTP you just received on your number: ')
encodedOTP = hashlib.sha256(OTP.encode('utf-8')).hexdigest()
print(encodedOTP)
payload = json.dumps({
    "otp": encodedOTP,
    "txnId": txnId
})

headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
}

response = s.post(validateOTPurl, headers=headers, data=payload)

# Store token value. This will be required to getBeneficiaries and scheduleAppointment

print("\n[AUTH OTP] RESULT:: Status Code: {} Reason: {}\n".format(response.status_code,response.reason))

token = response.json()['token']


## GET APPOINTMENT SCHEDULES FOR PRESENT DAY BY DISTRICT_ID. SEE getSchedulesurl VARIABLE DECLARATION FOR DETAILS.
print('[INFO] Checking for Available Centers...\n')

while True:
    payload={}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
            }

    response = s.get(getSchedulesurl, headers=headers, data=payload)
    time = datetime.datetime.now()

    print("[GET SCHEDULE] [{}] RESULT:: Status Code: {} Reason: {}\n".format(time,response.status_code,response.reason))

    centers = response.json()['sessions']

    #print(centers)  ## DEBUG: Get All Center Details

    for center in centers:
        name = center['name']
        address = center['address']
        district = center['district_name']
        block = center['block_name']
        pincode = center['pincode']
        fee_type = center['fee_type']
        fee = center['fee']
        session_id = center['session_id']
        date = center['date']
        availability = center['available_capacity']
        min_age = center['min_age_limit']
        vaccine = center['vaccine']
        slots = center['slots']
        dose1cap = center['available_capacity_dose1']
        dose2cap = center['available_capacity_dose2']

        # Check if Age Group, Vaccine Type match and there are available slots for vaccination.
        if min_age == 18 and availability > 0:# and vaccine == "COVAXIN" and availability > 0:
            print('FOUND SUITABLE SLOT\nName: {} | Address: {}\nDistrict: {} | Block: {} | Pincode: {}\nFee_Type: {} | Fee: {} | Session_ID: {}\nDate: {} | Available Slots: {}\nAge_Limit: {} | Vaccine_Type: {}\nSlots: {}\nDose1_Cap: {} | Dose2_Cap: {}\n'.format(name,address,district,block,pincode,fee_type,fee,session_id,date,availability,min_age,vaccine,slots,dose1cap,dose2cap))
            
            message = '*Name*: ' + name + ' | *Address*: ' + address+ ' | *District*: ' + district + ' | *Block*: ' + block + ' | *Pincode*: ' + str(pincode) + ' | *Fee*: ' + str(fee) + ' | *Date*: ' + str(date) + ' | *Age-Limit*: ' + str(min_age) + ' | *Vaccine-Type*: ' + vaccine + ' | *https://selfregistration.cowin.gov.in* | *Available Slots*: ' + str(availability) + ' | *Dose1-Slots*: ' + str(dose1cap) + ' | *Dose2-Slots*: ' + str(dose2cap)

            sentMessage = telegram_bot_sendtext(message)
            print("[BOT MESSAGE] Message sent to Telegram: {}".format(sentMessage))

    print("..........\n")

    t.sleep(30)


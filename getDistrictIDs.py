import requests

getStates = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
getDistricts =  'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'

s = requests.Session()

headers = {
           'Accept-Language': 'en_US',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
          }

get_states = s.get(getStates, headers=headers)

state_respSTR = get_states.json()

print("DISTRICT_ID DISTRICT_NAME STATE_ID STATE_NAME")
for state in state_respSTR['states']:
   state_id = state['state_id']
   state_name = state['state_name']
   getAllDistricts = getDistricts + str(state_id)
   
   get_districts = s.get(getAllDistricts, headers=headers)
   district_respSTR = get_districts.json()
   
   for district in district_respSTR['districts']:
      district_id = district['district_id']
      district_name = district['district_name']
      print(district_id,district_name,state_id,state_name)

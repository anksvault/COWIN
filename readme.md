## COWIN API Calls

This piece of code is written to demonstrate the usage of COWIN OPEN API. Please visit **[COWIN API Documentation](https://apisetu.gov.in/public/marketplace/api/cowin)** for more details: 

## Initial Configurations
Update your mobile number, agent secret, telegram bot's details in `secrets.py`. Please refer telegram bot configuration note for more details about how to configure and send messages to telegram bot.

## How to get district ID and agent secret
Refer the list of district IDs from `DISTRICT.txt` or execute `getDistrictIDs.py` to retrieve the latest list. You will get client secret from your browser. In order to get this, open your web browser (Chrome, Edge, Firefox), open developer options, login to COWIN site and login normally. You will get the details under Developer Options window's **Network** >> **Headers** >>**Request**. See below screenshot for reference.

![screenshot](/images/agent_secret.png)

## Requirements
Install all dependent packages using `pip install -r requirements.txt`

## Execution
`python3 COWIN.py`

Enter `OTP` when requested and let it run. If a suitable session is found, script will send a message to your Telegram Bot.

## COWIN API Calls

This piece of code is written to demonstrate the usage of COWIN OPEN API. Please visit **[COWIN API Documentation](https://apisetu.gov.in/public/marketplace/api/cowin)** for more details.

## Initial Configurations
Update your mobile number, agent secret, telegram bot's details in `secrets.py`. Please refer **[telegram bot configuration](https://github.com/anksvault/COWIN/blob/main/telegram_bot_config.md)** for more details about how to configure and send messages to telegram bot.

## How to get district ID and agent secret
Refer the list of district IDs from `DISTRICT.txt` or execute `getDistrictIDs.py` to retrieve the latest list. You will get client secret from your browser. In order to get this, open your web browser (Chrome, Edge, Firefox), open developer options (`F12` in most cases), login to COWIN site normally. You will get the details under Developer Options window's **Network** >> **Headers** >>**Request** section. See below screenshot for reference.

![screenshot](/images/agent_secret.png)

## Requirements
Install all dependent packages using `pip install -r requirements.txt`

## Execution
`python3 COWIN.py`

Enter `OTP` when requested and let it run. If a suitable session is found, script will send a message to your Telegram Bot.

If you want to get the information related to available schedules only, execute the following instead. This will run without further intervention for inputs like `OTP`.

`python3 getVaccinationSchedule.py`



# Creating your Telegram bot
On Telegram, search **@ BotFather**, send him a `/start` message.
Send another `/newbot` message, then follow the instructions to setup a name and a username.
Your bot is now ready, be sure to save a backup of your **API token**, this API token will be your `BOT_TOKEN` which needs to be updated in `secrets.py`

# Getting your Chat ID
On Telegram, search your bot (by the username you just created), press the `Start` button or send a `/start` message.
Open a new tab with your browser, enter `https://api.telegram.org/bot<yourtoken>/getUpdates` , replace `<yourtoken>` with your API token, press enter and you should see something like this:

`{"ok":true,"result":[{"update_id":77xxxxxxx,
"message":{"message_id":550,"from":{"id":99xxxxxxx,"is_bot":false,"first_name":"Ankit","last_name":"Vashistha","username":"anksvault923","language_code":"en-US"}`

Look for `id`, for instance, `99xxxxxxx` above is my chat id. Look for yours and put it as your `bot_chatID` in the main script.

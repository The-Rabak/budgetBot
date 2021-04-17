# budgetBot
A private telegram bot to collect expenses, generate reports and (in the future) will draw conclusions from ML models

Use instructions:
1. in the main tree, open a "bot" directory and add a creds.py file
2. the creds.py file should contain the following vars: db_name, db_password, db_url, db_user_name, bot_token, bot_user_name, URL(the Heroku url I haven't set up yet)
3. you should open a bot with BotFather (Telegram) to get your api key and user_name
4. open a mysql db (currently on localhost) and have it listening on the default port
5. create a table called "tb_expenses" for your expenses tracking

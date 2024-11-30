# CyberProject

This project has three initial users

User1 password
User2 password
admin admin

## How to start the project

To start this project run in terminal the commands. The running will start the program with the flaws.

`python3 manage.py makemigrtaions`

`python3 manage.py migrate`

`python3 manage.py runserver`

## Change to web app with the fixes to the flaws

The fixes are in the **betterViews.py** file. To change to the program to use that file and to change back you need to do these steps.

1. Delete **db.sqlite3** file
2. Change **urls.py** file inside the polls folder to use **betterViews.py** file. You can simply do this by uncommenting the imoport section of it. And after comment the **views.py** file to ensure the change.
3. Go to your terminal and run these commands.

   `python3 manage.py makemigrtaions`

   `python3 manage.py migrate`

   `python3 manage.py runserver`

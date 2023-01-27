# Qr-and-Inspection-in-Food-Industry-Thesis
Features:
Portal
Qr Scanner
Attendance(WIP) wala pang Object Recognition
Add employee 

# Need to Download (but first you need to create a virtual environment) ?
- download the library that is being place in requirements.txt using "pip install requirements.txt"
- download Qr Code api "npm install --save-dev html5-qrcode"
- download virtual environment using "pip install virtualenv"

# How to Run ?
1. Create virtual envronment use "virtualenv env".
2. Activate the virtual environment use "env\scripts\activate".
3. After you activate, download all the libraries in requirements.txt.
4. Make migration so that you create the database use "python manage.py makemigrations".
5. After you make migration, migrate it using "python manage.py migrate".
6. Create super userr using "python manage.py createsuperuser" and fill up the form.
7. After that, you can open the website using "python manage.py runserver" just copy the url that is being provided in the terminal.

# Take note: Make sure the if you run this program you need to add Mask in the equipment table in the admin panel

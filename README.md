
# Readable Bookstore (e-commerce website)

This is a fully functional e-commerce website for selling books designed and developed as a part of a full-stack web development project, and it is completely for learning purpose only. This project is developed using Python Django framework as backend language, PostgreSQL as database and other tools like HTML, CSS, Bootstrap and JavaScript. You can find the deployed project [here.](https://readablebookstore.online)

- Modern and minimalistic design that appeals to the user.
- Guest user functionality for improved user experience.
- Custom Admin panel for advanced application management.
- Used Twilio API for OTP authentications and Razorpay for payment.
- Deployed on AWS using Nginex and Router53

### Tech stack
Python Django | PostgresSQL | pgAdmin
HTML5 | CSS3 | Bootstrap | JavaScript
AWS | Nginx | Gunicorn | Router53 | Git | Github

## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv venv
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source venv/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```
Set up a `.env` file in the below format
```
SECRET_KEY= <your_django_secret_key>
DEBUG= <True or False>

DATABASES_NAME= <your_database_name>
DATABASES_PASSWORD= <your_database_password>

EMAIL_HOST_USER= <email_from_which_all_mail_to_be_sent>
EMAIL_HOST_PASSWORD= <app_password_for_your_mail>

RAZORPAY_SECRET_KEY= <your_razorpay_secret_key>
RAZORPAY_KEY_ID= <your_razorpay_key_id>

TWILIO_ACCOUNT_SID= <your_twilio_account_sid>
TWILIO_AUTH_TOKEN= <your_twilio_auth_token>

```

Apply migrations and create your database
```
python manage.py migrate
```
Create a user with manage.py
```
python manage.py createsuperuser
```

Now you can run the project with this command

```
python manage.py runserver
```

---


## 📸 Screenshots :


**User Feed** : <br/>

<table width="100%"> 
<tr>

<td width="50%">
<p align="center">
Home Page
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/home.png">  
</td>
  <td width="50%">      
<p align="center">
  Product Listing
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/product-listing.png">
</td> 
</table>
<br/>

<table width="100%"> 
<tr>
<td width="50%">      

<p align="center">
Product Page
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/product-view.png">  
</td>
<td width="50%">
<p align="center">
Cart Page
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/cart.png">  
</td>
</table>
<br/>

<table width="100%"> 
<tr>
<td width="50%">
<p align="center">
  Register Page
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/register-page.png">
</td> 
<td width="50%">
<p align="center">
Login Page
</p>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/login-page.png">  
</td>
</table>
<br/>

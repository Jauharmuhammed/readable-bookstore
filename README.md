
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/jauharmuhammed/README-template">
    <img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/static/images/readable-icon-black-1.jpg" alt="Logo" width="80" height="80" border-radius="50%">
  </a>

  <h3 align="center">Readable Bookstore</h3>

  <p align="center">
    An awesome e-commerce website for books.
    <br />
    <a href="https://github.com/jauharmuhammed/readable-bookstore"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://readablebookstore.online">View Site</a>
    ·
    <a href="https://github.com/jauharmuhammed/readable-bookstore/issues">Report Bug</a>
    ·
    <a href="https://github.com/jauharmuhammed/readable-bookstore/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#running-this-project">Running this project</a>
    </li>
    <li><a href="#screenshots">Screenshots</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project
<br>
<p align='center'>
<img src="https://github.com/Jauharmuhammed/readable-bookstore/blob/main/assets/product-listing.png" width='70%' >
</p>
<br>

This is a fully functional e-commerce website for books designed and developed as a part of a full-stack web development project, and it is completely for learning purpose only. This project is developed using Python Django framework as backend language, PostgreSQL as database and other tools like HTML, CSS, Bootstrap and JavaScript. You can find the deployed project [here.](https://readablebookstore.online)

- Modern and minimalistic design that appeals to the user.
- Guest user functionality for improved user experience.
- Custom Admin panel for advanced application management.
- Used Twilio API for OTP authentications and Razorpay for payment.
- Deployed on AWS using Nginex and Router53

<br>

### Built With

![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![AWS](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5%20-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS%20-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

<br>

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

<br>

## Screenshots



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




## Contact

<div align='left'>

<a href="https://linkedin.com/in/jauharmuhammed" target="_blank">
<img src="https://img.shields.io/badge/linkedin-%2300acee.svg?color=405DE6&style=for-the-badge&logo=linkedin&logoColor=white" alt=linkedin style="margin-bottom: 5px;"/>
</a>
	
<a href="https://twitter.com/jauharmuhammed_" target="_blank">
<img src="https://img.shields.io/badge/twitter-%2300acee.svg?color=1DA1F2&style=for-the-badge&logo=twitter&logoColor=white" alt=twitter style="margin-bottom: 5px;"/>
</a>
	
<a href="mailto:jauharmuhammedk@gmail.com" target="_blank">
<img src="https://img.shields.io/badge/gmail-%23EA4335.svg?style=for-the-badge&logo=gmail&logoColor=white" t=mail style="margin-bottom: 5px;" />
</a>
	
		
<a href="https://codepen.io/jauharmuhammed" target="_blank">
<img src="https://img.shields.io/badge/codepen-%23000000.svg?style=for-the-badge&logo=codepen&logoColor=white" t=mail style="margin-bottom: 5px;" />
</a>

</div>



# PMS 

A small open-source PMS app made with Django.

## Live Demo

https://chapp-inn.herokuapp.com/

## Stored data
- Type of rooms: name, n° of guests and price per day
- Rooms: name, description
- Customers: name, email, phone
- Bookings: checkin, checkout, total guests, customer information, total amount


## Features
- Create, delete and check bookings for each room
- Check room availability
- Find bookings by code or customer name
- Dashboard with bookings, incoming and outcoming customers, total invoiced
- Get detailed information about each room
- Edit customer information

## Local Deployment

To deploy this project locally run

```bash
    pip install virtualenv
    virtualenv pms
    source pms/bin/activate
    pip install django
    git clone https://github.com/vsa-ok/chapp_pms
    cd chapp_pms
    pipenv sync
    python manage.py runserver
  
```
### Django admin (/admin)
Use for username and password for superuser is "admin" (without quotes).Remember to change it.

### Warnings
- SECRET_KEY should be stored in .env file for production!
- DEBUG is set to TRUE.

# 🚀 About Me
Fullstack developer. Tech skills:
- HTML
- Bootstrap 5
- CSS
- Javascript
- NodeJS
- ReactJS
- MongoDB
- PHP
- MYSQL
- Python
- C#
- Linux (Ubuntu Server / Manjaro)
- AWS (S3, EC2, Route 53)
- API REST


### 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/vsa-ok/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/maximiliano-villa)


## License
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://choosealicense.com/licenses/mit/)



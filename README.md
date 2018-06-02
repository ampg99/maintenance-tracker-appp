# Maintenance-Tracker-App

![Travis](https://img.shields.io/travis/asheuh/Maintenance-Tracker-App.svg)
![Code Climate](https://img.shields.io/codeclimate/coverage/asheuh/Maintenance-Tracker-App.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/asheuh/Maintenance-Tracker-App/develop.svg)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/asheuh/Maintenance-Tracker-App.svg)
#### Project Overview

Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

#### Required Features

- Users can create an account and log in.
- The users should be able to make maintenance or repairs request.
- An admin should be able to approve/reject a repair/maintenance request.
- The admin should be able to mark request as resolved once it is done.
- The admin should be able to view all maintenance/repairs requests on the application
- The admin should be able to filter requests
- The user can view all his/her requests

# Installation and Setup
Clone the repository.
```bash
git clone https://github.com/asheuh/Maintenance-Tracker-app
```
## Navigate to the API folder
```bash
cd Maintenance-Tracker-app/api
```

## Create a virtual environment

```bash
$ virtualenv venv
$ source venv/bin/activate
```
On Windows
```bash
py -3 -m venv venv
```

## Activate the virtual environment

```bash
source venv/bin/activate
```
Windows users
```bash
venv\Scripts\activate
```

## Install requirements( with pip)
```bash
$ pip install -r requirements.txt
```

## Running the application
After the configuration, you will run the app 
```bash
$ python api/run.py
```

## Url for endpoints

```
http://localhost:5000/api/v1/
```

## Testing
Run pytest to test
```bash
pytest
```
Z
## endpoints
|  Endpoint  | Task  |
|  ---  | --- |
| `POST api/v1/users/signup` | signing up a user |
| `POST api/v1/users/login`  | log in user|
| `DELETE api/v1/users/lgout` | logout user |
| `POST api/v1/users/requests` | User create a request | 
| `GET api/v1/users/requests` | User can view all requests|
| `PUT api/v1/users/requests/<request_id>` | User updates a request |
| `GET api/v1/users/requests/<request_id>` | User gets a request (one)|
| `GET api/v1/users/<int:id>` | Get user details |

#### 1. Sign Up for the Service

- Sign up at: https://asheuh.github.io/Maintenance-Tracker-App/
```
(_you need to use a "real" email address ...
Maintenance-Tracker-App will send you and alert if one of your projects has a security vulnerability so make sure it's
an email address you check regularly or better one that you receive on your phone!_)
```

- The sign up form looks like the one below:

![newsignup](https://user-images.githubusercontent.com/22955146/40570633-6f4cb02c-6095-11e8-975a-ebac778d8dbc.png)
- Fileds required to sign up
```Username```
```Email address```
```Password```
```Conform Password```

#### 2. Create your "Request" 

- Once you have verified your account with `Maintenance Tracker` go a head and make a `a Maintenance request`
so you can keep track of  your requests

![createrequestpage](https://user-images.githubusercontent.com/22955146/40580598-300ac1be-614a-11e8-820b-c60cc5290a53.png)

### Contributing 

- If you want to _encourage_ people to contribute to this project, by reminding them that you _welcome_ their input go to the app and use it

### Template
- You can view the UI template on [Github Pages](https://asheuh.github.io/Maintenance-Tracker-App/)

## Authors

* **Brian Mboya** - *Initial work* - [asheuh](https://github.com/asheuh)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thank's for my follow bootcampers at Open Andela
* Inspiration
* The power is w3school is really awesome. N
* Don't let life craft you, craft it
[![Build Status](https://travis-ci.org/andela-jmwalo/BucketListAPI.svg?branch=develop)](https://travis-ci.org/andela-jmwalo/BucketListAPI)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/da89e3c879c14eb8b22049d362c62cb4)](https://www.codacy.com/app/judith-achieng/BucketListAPI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-jmwalo/BucketListAPI&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/andela-jmwalo/BucketListAPI/develop/landscape.svg?style=plastic)](https://landscape.io/github/andela-jmwalo/BucketListAPI/develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/da89e3c879c14eb8b22049d362c62cb4)](https://www.codacy.com/app/judith-achieng/BucketListAPI?utm_source=github.com&utm_medium=referral&utm_content=andela-jmwalo/BucketListAPI&utm_campaign=Badge_Coverage)
# flask-bucketlist
A Flask API for a bucket list service that enables one to create, read update and delete Bucketlists and bucketlist items.
### Installation
Clone this repo from Github to your local machine:
```
git clone https://github.com/andela-jmwalo/BucketListAPI.git
```
cd into the BucketListAPI folder
```
cd BucketListAPI
```
## Install requirements
```
pip install -r requirements.txt
```
to Run the program :
```
python run.py
```
To run the tests: 
```
pytest
```

#### ENDPOINTS

The following endpoints are provided 

|URL Endpoint| HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login and retrieve token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?q=bl` | `GET` | Match bucketlist by name |
| `/bucketlists/<id>/` | `GET` |  Retrieve bucket list details |
| `/bucketlists/<id>/` | `PUT` | Update bucket list details |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucket list |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucket list |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete a item in a bucket list|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucket list item details|
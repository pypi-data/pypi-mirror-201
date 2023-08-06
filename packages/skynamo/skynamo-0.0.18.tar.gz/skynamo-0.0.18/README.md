# skynamo python SDK

## Overview
This package is a python SDK for skynamo public API. It allows you to pull data from your skynamo instance and update data in your skynamo instance. Some of the features include:
- Extending your instance's data classes with their respective custom fields. This allows you to use your IDE's autocomplete feature to easily access your custom fields.
- Pulling data from your skynamo instance and caching it locally to speed up subsequent calls and prevent hitting the skynamo API rate limit.
- Updating data in your skynamo instance using write batches to speed up the process and to prevent hitting the skynamo API rate limit.
- Saving raw or processed (e.g with filters or by combining different data types) skynamo data in csv files, which can be usefull for reporting.
- Sending emails using your gmail account.

## Performance
- Requests to Skynamo's API is made in parallel to speed up responses
- Pulled data from Skynamo is cached with only the changes being pulled, to ensure the request limit of your access token is not hit

## Requirements
- Python 3.6 or higher installed on your machine (https://www.python.org/downloads/)
- pip installed on your machine (should be installed with python)

## Installation
Run the following command in your terminal to install the latest version of the skynamo python SDK:
```bash
pip install skynamo
```

If you are planning on sending emails you also need to install the following python packages:
- email
- smtplib

## Setup
Add skynamo-config.json in the root directory of your repository with the following information:
```json
{
	"SKYNAMO_INSTANCE_NAME":"coolestcompanyever",
	"SKYNAMO_REGION":"za",
	"SKYNAMO_API_KEY":"a3csg###########",
	"SKYNAMO_CACHE_REFRESH_INTERVAL": 300,
	"SKYNAMO_GMAIL_SENDER":"me@coolestcompanyever@gmail.com",
	"SKYNAMO_GMAIL_PASSWORD":"qg3gs###########",
}
```
- Instance name and region can be found in your skynamo instance url. For example, if your instance url is https://coolestcompanyever.za.skynamo.me, then your instance name is coolestcompanyever and your region is za (only other region is uk).
- Api key can be found by going to your skynamo instance, clicking on the settings icon in the top right corner, clicking on 'Integration tokens' (in left panel) and clicking on the "Add access token"
- Cache refresh interval is the number of seconds between cache refreshes. This does not need to be in the json file. If not specified, the default value is 300 seconds.
- Gmail sender and password can be used to send emails. Sender is the email address that will be used to send the emails and password is the google app password for that email address. Note the app password is not the same as your normal password and can be created by going to https://myaccount.google.com/apppasswords

## Creating your instance's data classes
```python
from skynamo import refreshCustomFormsAndFields

refreshCustomFormsAndFields()
```
This creates files in the skynamo_data/code folder with files containing python classes. Each class represents a data model that can be customized using skynamo's forms.

## Pulling data from your skynamo instance
To pull any data from your skynamo instance, you need to import the Reader class and call the get method for the data you want to pull. For example, to pull all customers from your skynamo instance, you would do the following:
```python
from skynamo_data.code.Reader import Reader

reader=Reader()
customers=reader.getCustomers()
```

If you are using an IDE like Visual Studio Code you will see all the available options for pulling data if you simply type "reader." (like shown in the image below):

![alt text](doc/PullingData.png)

To make it easier to work with data pulled from Skynamo, all data is saved as objects making it possible for your IDE to show you what properties are available for each data object. See below as an example:

![alt text](doc/Working%20with%20pulled%20data.png)

## Writing data to your skynamo instance
To make any puts, posts or patches you need to build up a list of writes and then apply them together as shown below:
```python
from skynamo_data.code.Writer import Writer

writer=Writer()
writer.addCustomerCreate('GEP001','Gepa Store')
writer.addStockLevelUpdateUsingProductCodeAndUnitName('SKU 010','Cases',12)
listOfErrors=writer.apply()
if listOfErrors!=[]:
	print(listOfErrors)
```
If you are using an IDE like Visual Studio Code you will see all the available options for writing data if you simply type "writer." (like shown in the image below):

![alt text](doc/GettingListOfWriteOperations.png)

Furthermore, after selecting the desired write method you will get a clear guide of what inputs are required/allowed and what data types they must be as shown below:

![alt text](doc/Adding%20correct%20inputs%20to%20write%20method.png)

## To skynamo developers
The first action in the buddy pipeline ensures that the most updated code is deployed accross all the integration servers. The second action publishes the package to pypi if the version in setup.py was bumped. You will see a failure at this action if the buddy pipeline ran but the version in setup.py was not bumped. This gives you control over when the package is published to pypi.
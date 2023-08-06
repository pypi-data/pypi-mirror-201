import os
import requests
from typing import Literal,Any,Union,Dict
from .helpers import updateEnvironmentVariablesFromJsonConfig

def getApiBase():
	region=os.environ.get('SKYNAMO_REGION')
	if region==None:
		updateEnvironmentVariablesFromJsonConfig()
		region=os.environ.get('SKYNAMO_REGION')
	return f'https://api.{region}.skynamo.me/v1/'

def getHeaders():
	instanceName=os.environ.get('SKYNAMO_INSTANCE_NAME')
	apiKey=os.environ.get('SKYNAMO_API_KEY')
	if instanceName==None or apiKey==None:
		updateEnvironmentVariablesFromJsonConfig()
		instanceName=os.environ.get('SKYNAMO_INSTANCE_NAME')
		apiKey=os.environ.get('SKYNAMO_API_KEY')
	return {'x-api-client':instanceName,'x-api-key':apiKey,'accept':'application/json'}

def makeRequest(method:Literal['get','post','patch','put'],dataType:str,dataOrParams:Union[list,Dict[str,Any]]={}):
	print(method)
	print(dataType)
	print(dataOrParams)
	if method=='get':
		return requests.get(getApiBase()+dataType,headers=getHeaders(),params=dataOrParams).json()
	elif method=='post':
		return requests.post(getApiBase()+dataType,headers=getHeaders(),json=dataOrParams).json()
	elif method=='patch':
		return requests.patch(getApiBase()+dataType,headers=getHeaders(),json=dataOrParams).json()
	elif method=='put':
		return requests.put(getApiBase()+dataType,headers=getHeaders(),json=dataOrParams).json()
	elif method=='delete':
		return requests.delete(getApiBase()+dataType,headers=getHeaders(),json=dataOrParams).json()
	else:
		raise Exception(f'Invalid method: {method}')

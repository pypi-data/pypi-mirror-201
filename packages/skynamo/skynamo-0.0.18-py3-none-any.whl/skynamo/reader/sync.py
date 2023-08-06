from ..shared.helpers import ensureFolderExists
from typing import Union,Literal,List,Dict
from ..shared.api import makeRequest
import json,math,threading

def AddPageResultToExistingItemsAndReturnTotalItems(dataType:str,existingItems:Dict,pageNr:int,pageSize:int,filters:str,flags:List[str]=[]):
	print(f'Pagenr: {pageNr}')
	params:Dict[str,Union[str,int]]={'page_number':pageNr,'page_size':pageSize}
	if filters!='':
		params['filters']=filters
	if flags!=[]:
		params['flags']=','.join(flags)
	jsonResponse=makeRequest('get',dataType,params)
	if 'message' in jsonResponse:
		if jsonResponse['message']=='Forbidden':
			raise Exception('Invalid region, instance name or api key')
	totalItems=0
	if 'page' in jsonResponse:
		totalItems=jsonResponse['page']['filtered_item_count']
	if 'data' in jsonResponse:
		data=jsonResponse['data']
		for item in data:
			id=''
			if dataType=='stocklevels':
				warehouseId=0
				if 'warehouse_id' in item:
					warehouseId=item['warehouse_id']
				id=f'{item["product_id"]},{item["order_unit_id"]},{warehouseId}'
			elif dataType=='prices':
				id=f'{item["product_id"]},{item["order_unit_id"]},{item["price_list_id"]}'
			else:
				id=item['id']
			existingItems[id]=item
	return totalItems

def addLatestRowVersionToExistingData(existingData:dict,existingItems:dict):
	latestRowVersion=0
	for item in existingItems.values():
		possibleVersionKeys=['row_version','version']
		for key in possibleVersionKeys:
			if key in item:
				rowVersion=item[key]
				if rowVersion>latestRowVersion:
					latestRowVersion=rowVersion
	existingData['lastRowVersion']=latestRowVersion

def SyncDataTypeFromSkynamoToLocalJsonFiles(dataType,fullSync=False,syncFromLastRowVersion=False,flags:List[str]=[]):
	exceptionThatOccured=None
	print(f'Starting sync for {dataType}')
	pageSize=200
	totalItems=-1
	existingData={'lastPageNr':1,'items':{},'lastRowVersion':0}
	if not(fullSync):
		try:
			with open(getSynchedDataTypeFileLocation(dataType), "r") as read_file:
				existingData=json.load(read_file)
		except Exception as e:
			pass
	pageNr=1
	filters=''
	if syncFromLastRowVersion:
		rowVersion=existingData['lastRowVersion']
		filters=f'[\"greater_than(version,{rowVersion})\"]'
	else:
		pageNr=existingData['lastPageNr']
	existingItems=existingData['items']
	try:
			totalItems=AddPageResultToExistingItemsAndReturnTotalItems(dataType,existingItems,pageNr,pageSize,filters,flags)
			pageNr=pageNr+1
			predictedNumberOfPages=math.ceil(totalItems/pageSize)
			while pageNr<=predictedNumberOfPages:
				pagesLeft=predictedNumberOfPages-pageNr + 1
				nrThreads=pagesLeft
				if nrThreads>20:
					nrThreads=20
				threads=[]
				for t in range(nrThreads):
					t=threading.Thread(target=AddPageResultToExistingItemsAndReturnTotalItems,args=(dataType,existingItems,pageNr+t,pageSize,filters,flags))
					t.start()
					threads.append(t)
				for thread in threads:
					thread.join()
				pageNr=pageNr+nrThreads
	except Exception as e:
		exceptionThatOccured=e

	addLatestRowVersionToExistingData(existingData,existingItems)
	existingData['lastPageNr']=pageNr-1
	with open(getSynchedDataTypeFileLocation(dataType), "w") as write_file:
		print(f'updating cache for {dataType}')
		json.dump(existingData, write_file)
	if exceptionThatOccured!=None:
		raise exceptionThatOccured

def SyncDataTypesFromSkynamo(dataTypes:List[Literal['pricelists','taxrates','prices','warehouses','completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','formdefinitions','interactions']]=['completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','interactions']):
	fullSyncDataTypes=['users','stocklevels','formdefinitions','taxrates','warehouses','pricelists']
	versionedDataTypes=['customers','products','invoices']
	dataTypeFlags={'formdefinitions':['show_enums'],'orders':['show_nulls'],'creditrequests':['show_nulls'],'quotes':['show_nulls']}
	flags=[]
	for dataType in dataTypes:
		fullSync=False
		if dataType in fullSyncDataTypes:
			fullSync=True
		syncFromLastRowVersion=False
		if dataType in versionedDataTypes:
			syncFromLastRowVersion=True
		if dataType in dataTypeFlags:
			flags=dataTypeFlags[dataType]
		SyncDataTypeFromSkynamoToLocalJsonFiles(dataType,fullSync,syncFromLastRowVersion,flags)

def refreshJsonFilesLocallyIfOutdated(dataTypes:List[Literal['pricelists','taxrates','prices','warehouses','completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','formdefinitions','interactions']],forceRefresh:bool=False):
	import os
	import time
	nrSecondsToWaitBeforeRefreshing=300
	if os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')!=None:
		try:
			nrSecondsToWaitBeforeRefreshing=int(os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')) #type: ignore
		except:
			pass

	for dataType in dataTypes:
		if os.path.exists(getSynchedDataTypeFileLocation(dataType)):
			fileLastModifiedTime = os.path.getmtime(getSynchedDataTypeFileLocation(dataType))
			if forceRefresh or time.time()-fileLastModifiedTime>nrSecondsToWaitBeforeRefreshing:
				SyncDataTypesFromSkynamo([dataType])
		else:
			SyncDataTypesFromSkynamo([dataType])

def getSynchedDataTypeFileLocation(dataType:str):
	return f'skynamo_data/cache/{dataType}.json'
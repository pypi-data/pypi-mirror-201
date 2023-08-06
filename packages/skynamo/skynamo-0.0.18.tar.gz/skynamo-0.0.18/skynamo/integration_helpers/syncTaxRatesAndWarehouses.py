from typing import List,Dict,Any
from skynamo.main.Reader import Reader
from skynamo.main.Writer import Writer
from skynamo.models.TaxRate import TaxRate
from skynamo.models.Warehouse import Warehouse

def syncTaxRatesWithSkynamoAndReturnNameLookup(taxRates:List[Dict[str,Any]],idField:str,nameField:str,rateField:str,isActiveField:str='deleted_at',isActiveValue:Any='',multiplyRateBy=1):
	erpTaxRateIdToSkynamoTaxRates=getDictOfErpTaxRateIdToSkynamoTaxRate()
	writer=Writer()
	nameLookup={}
	for erpTaxRate in taxRates:
		erpTaxRateId=erpTaxRate[idField]
		name=erpTaxRate[nameField]+' ('+erpTaxRateId+')'
		nameLookup[erpTaxRateId]=name
		newRate=float(erpTaxRate[rateField])*multiplyRateBy
		isActiveInErp=erpTaxRate[isActiveField]==isActiveValue
		if erpTaxRateId not in erpTaxRateIdToSkynamoTaxRates:# if tax rate is not in skynamo and is active in erp
			if isActiveInErp:
				writer.addTaxRateCreate(name,newRate)
		else:# if tax rate is in skynamo
			skynamoTaxRate=erpTaxRateIdToSkynamoTaxRates[erpTaxRateId]
			if name!=skynamoTaxRate.name or newRate!=skynamoTaxRate.rate or isActiveInErp!=skynamoTaxRate.active:
				skynamoTaxRate.name=name
				skynamoTaxRate.rate=newRate
				skynamoTaxRate.active=isActiveInErp
				writer.addTaxRateUpdate(skynamoTaxRate,['name','rate','active'])
	errors=writer.apply()
	if errors!=[]:
		raise Exception('Error syncing tax rates with Skynamo: '+str(errors))
	return nameLookup

def syncWarehousesWithSkynamoAndReturnNameLookup(erpWarehouses:List[Dict[str,Any]],idField:str,nameField:str,isActiveField:str='deleted_at',isActiveValue:Any=''):
	erpWarehouseIdToSkynamoWarehouse=getDictOfErpWarehouseIdToSkynamoWarehouse()
	writer=Writer()
	nameLookup={}
	for erpWarehouse in erpWarehouses:
		erpWarehouseId=erpWarehouse[idField]
		name=erpWarehouse[nameField]+' ('+erpWarehouseId+')'
		nameLookup[erpWarehouseId]=name
		isActiveInErp=erpWarehouse[isActiveField]==isActiveValue
		if erpWarehouseId not in erpWarehouseIdToSkynamoWarehouse:# if warehouse is not in skynamo and is active in erp
			if isActiveInErp:
				writer.addWarehouseCreate(name)
		else:
			skynamoWarehouse=erpWarehouseIdToSkynamoWarehouse[erpWarehouseId]
			if name!=skynamoWarehouse.name or isActiveInErp!=skynamoWarehouse.active:
				skynamoWarehouse.name=name
				skynamoWarehouse.active=isActiveInErp
				writer.addWarehouseUpdate(skynamoWarehouse,['name','active'])
	errors=writer.apply()
	if errors!=[]:
		raise Exception('Error syncing warehouses with Skynamo: '+str(errors))
	return nameLookup


def getDictOfErpTaxRateIdToSkynamoTaxRate():
	reader=Reader()
	result:Dict[str,TaxRate]={}
	existingTaxRates=reader.getTaxRates(forceRefresh=True)
	for taxRate in existingTaxRates:
		addTaxOrWarehouseObjectToResult(result,taxRate)
	return result

def getDictOfErpWarehouseIdToSkynamoWarehouse():
	reader=Reader()
	result:Dict[str,Warehouse]={}
	existingWarehouses=reader.getWarehouses(forceRefresh=True)
	for warehouse in existingWarehouses:
		addTaxOrWarehouseObjectToResult(result,warehouse)
	return result

def addTaxOrWarehouseObjectToResult(result:Dict[str,Any],object):
	firstBracketPos=object.name.find('(')
	lastBracketPos=object.name.find(')')
	if firstBracketPos!=-1 and lastBracketPos!=-1 and lastBracketPos>firstBracketPos:
		erpTaxRateId=object.name[firstBracketPos+1:lastBracketPos]
		result[erpTaxRateId]=object
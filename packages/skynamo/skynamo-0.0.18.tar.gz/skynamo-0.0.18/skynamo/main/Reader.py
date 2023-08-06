from .CreditRequest import CreditRequest
from .Order import Order
from .Quote import Quote
from .Product import Product
from .Customer import Customer
from skynamo.models.Invoice import Invoice
from skynamo.models.User import User
from skynamo.models.Warehouse import Warehouse
from skynamo.models.TaxRate import TaxRate
from skynamo.models.Price import Price
from skynamo.models.StockLevel import StockLevel
from skynamo.models.PriceList import PriceList
from skynamo.reader.jsonToObjects import getListOfObjectsFromJsonFile,populateCustomPropsFromFormResults,populateUserIdAndNameFromInteractionAndReturnFormIds
from skynamo.reader.sync import refreshJsonFilesLocallyIfOutdated,getSynchedDataTypeFileLocation
import json
from typing import List,Dict
##|customImports|##

def _getTransactions(transactionClass,forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated([f'{transactionClass.__name__.lower()}s','completedforms','interactions'])#type:ignore
	interactionsJson={}
	with open(getSynchedDataTypeFileLocation('interactions'), "r") as read_file:
		interactionsJson=json.load(read_file)
	refreshJsonFilesLocallyIfOutdated(['orders','completedforms','interactions'],forceRefresh)
	completedForms={}
	with open(getSynchedDataTypeFileLocation('completedforms'), "r") as read_file:
		completedForms=json.load(read_file)
	transactions=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation(f'{transactionClass.__name__.lower()}s'),transactionClass)
	for i,transaction in enumerate(transactions):
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(transaction,interactionsJson)
		populateCustomPropsFromFormResults(transaction,formIds,completedForms)
	return transactions

class Reader:
	def __init__(self):
		pass
	def getOrders(self,forceRefresh=False):
		orders:List[Order]=_getTransactions(Order,forceRefresh)
		return orders

	def getCreditRequests(self,forceRefresh=False):
		creditRequests:List[CreditRequest]=_getTransactions(CreditRequest,forceRefresh)
		return creditRequests

	def getQuotes(self,forceRefresh=False):
		quotes:List[Quote]=_getTransactions(Quote,forceRefresh)
		return quotes

	def getProducts(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['products'],forceRefresh)
		products:List[Product]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('products'),Product)
		return products

	def getCustomers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['customers'],forceRefresh)
		customers:List[Customer]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('customers'),Customer)
		return customers

	def getInvoices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['invoices'],forceRefresh)
		invoices:List[Invoice]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('invoices'),Invoice)
		return invoices

	def getStockLevels(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['stocklevels'],forceRefresh)
		stockLevels:List[StockLevel]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('stocklevels'),StockLevel)
		return stockLevels

	def getUsers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['users'],forceRefresh)
		users:List[User]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('users'),User)
		return users

	def getWarehouses(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['warehouses'],forceRefresh)
		warehouses:List[Warehouse]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('warehouses'),Warehouse)
		return warehouses

	def getPrices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['prices'],forceRefresh)
		prices:List[Price]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('prices'),Price)
		return prices
	
	def getTaxRates(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['taxrates'],forceRefresh)
		taxRates:List[TaxRate]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('taxrates'),TaxRate)
		return taxRates
	
	def getPriceLists(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['pricelists'],forceRefresh)
		priceLists:List[PriceList]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('pricelists'),PriceList)
		return priceLists


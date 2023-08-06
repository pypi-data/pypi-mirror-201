from typing import Union,Literal,List,Dict
from datetime import datetime
from skynamo.models.Address import Address
from skynamo.shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.models.Transaction import Transaction

class CreditRequest(Transaction):
	def __init__(self,json:dict):
		super().__init__(json)

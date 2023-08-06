from typing import Literal,List,Union
class WriteError:
	def __init__(self,dataType:str,httpMethod:str,body:Union[list,dict,str],error:List[str]):
		self.dataType=dataType
		self.body=body
		self.httpMethod=httpMethod
		self.error=error
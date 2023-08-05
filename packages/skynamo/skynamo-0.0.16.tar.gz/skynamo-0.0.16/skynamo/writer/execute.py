from .WriteOperationCls import WriteOperation
from .WriteErrorCls import WriteError
from ..shared.api import makeRequest
import math,threading
from typing import List,Union

def executeWrites(writeOperations:List[WriteOperation]):
	writeBatchesGroupedByDataTypeAndHttpMethod=[]
	for write in writeOperations:
		found=False
		if not(write.canBeCombinedWithOtherWritesInAList):
			writeBatchesGroupedByDataTypeAndHttpMethod.append(write)
			continue
		for writeBatch in writeBatchesGroupedByDataTypeAndHttpMethod:
			if writeBatch[0].dataType==write.dataType and writeBatch[0].httpMethod==write.httpMethod:
				writeBatch.append(write)
				found=True
				break
		if not found:
			writeBatchesGroupedByDataTypeAndHttpMethod.append([write])
	subBatchesWithMaxSizeOf20:List[List[WriteOperation]]=[]
	for writeBatch in writeBatchesGroupedByDataTypeAndHttpMethod:
		if not(isinstance(writeBatch,list)):
			subBatchesWithMaxSizeOf20.append(writeBatch)
			continue
		for i in range(math.ceil(len(writeBatch)/20)):
			subBatchesWithMaxSizeOf20.append(writeBatch[i*20:i*20+20])
	return __makeThreadedWrites(subBatchesWithMaxSizeOf20)

def __makeThreadedWrites(subBatchesWithMaxSizeOf20:List[List[WriteOperation]]):
	threads=[]
	errors:List[WriteError]=[]
	for subBatch in subBatchesWithMaxSizeOf20:
		threads.append(threading.Thread(target=__makeWriteRequest,args=(subBatch,errors)))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return errors

def __makeWriteRequest(writeOperations:Union[WriteOperation,List[WriteOperation]],errors:List[WriteError]):
	body=[]
	httpMethod=''
	dataType=''
	if isinstance(writeOperations,list):
		httpMethod=writeOperations[0].httpMethod
		dataType=writeOperations[0].dataType
		for write in writeOperations:
			body.append(write.itemOrId)
	else:
		body=writeOperations.itemOrId
		httpMethod=writeOperations.httpMethod
		dataType=writeOperations.dataType
	results=makeRequest(httpMethod,dataType,body)#type:ignore
	if 'errors' in results:
		for error in results['errors']:
			errors.append(WriteError(dataType,httpMethod,body,error['detail']))
import csv
from ..shared.helpers import ensureFolderExists,getPathRelativeToSkynamoDataFolder
from typing import List
def writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames(listOfObjects:list, filename: str,columnsOrder:List[str]=[],delimiter: str = ',') -> None:
	##ensure filename is in output folder
	if 'output/' != filename[:7]:
		filename = 'output/' + filename
	##ensure filename ends with .csv
	if '.csv' != filename[-4:]:
		filename = filename + '.csv'
	headers=[]
	for col in columnsOrder:
		headers.append(col)
	for key in listOfObjects[0].__dict__.keys():
		if key not in headers:
			headers.append(key)
	ensureFolderExists(getPathRelativeToSkynamoDataFolder('output'))
	with open(getPathRelativeToSkynamoDataFolder(filename), 'w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter=delimiter,quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writeheader()
		for obj in listOfObjects:
			writer.writerow(obj.__dict__)
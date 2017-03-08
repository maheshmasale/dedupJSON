Coding Sample

1. Task - Remove duplicates from the json data where combination of ‘_id’ and ‘email’ keys should be unique. The selection criteria for duplicates is based on the ‘entryDate’, the latest the better and if both the contenders have same date-time then select the one with last entry.

2. Solution – The solution is to create a dictionary which will hold the records as value and key being the combination of the ‘_id’ and ‘email’. The unique combination of these two is created by appending their length at the start of the string. This way we will be storing one record per combination. Once we found out the duplicate record, we will compare their dates. The dates comparison is done through converting it to seconds and then adding the time zone difference to it. If the comparison is same or greater than the previous records then we are replacing the previous record with the current record.
3. Validations – This code validates date string and whether the input string is valid json or not. This code also validates the keys and input file name string. 
4. Output – The code prints the output to the console. And it also maintains a log file where it logs the changes made to the data i.e. which records being kept or rejected or being replaced. This can be disable with one flag, the code supports that as well.
5. Running time – Time complexity of the code is O(n) and space complexity of the code is also O(n).
Used garbage collector to free up space. (in small scale this one won’t help much but with larger data this one would surely help us)
6. Environment – Python 3 onwards, Windows 10.
7. Instruction for execution – Please run following command to run this file in console:
	Python deduplicateJSON.py leads.json
	#Here you can replace leads.json file name with other file name and you can also provide path to that file. 
8. Unit tests – This code is been tested for 9 different unit test cases. I have attached the unit test data and their output. The unit tests are for following cases – 
	a.	Invalid dates in first occurrence
	
	b.	Invalid dates in second occurrence
	c.	Same Dates and time and time zone
	d.	Same Dates and different time and same time zone
	e.	Same Dates, time and different time zone
	f.	Different dates
	g.	Issue with the key, improper key or key not found
	h.	Same id but different email
	i.	Same email but different id

import json
import time
import sys
import gc
#Flag set to true for writing to to file and false to avoid setting it.
writeToFileFlag = True

def main():
    if len(sys.argv) != 2:
        print("python deduplicateJSON.py <path_to_data_file>")
        exit(1)
    dataFilePath = sys.argv[1]

    #output.tx will be log file where I will be writing the output of my code and the changes made to the data.
    outputFileName = 'output.txt'
    trg = open(outputFileName,'w')
    trg.truncate()
    try:
        gc.collect()
        dataRead = readFromFile(dataFilePath)
        writeToFile(trg,"Data read from file - \n"+dataRead+"\n\n")
        jsonRead = parseJSON(dataRead)

        dedupicatedData = dict()
        dedupicatedData["leads"] = deduplicateIt(jsonRead["leads"],trg)
        print(convertToJson(dedupicatedData))
        writeToFile(trg, "\nFinal Output after dedupication - \n"+convertToJson(dedupicatedData))
    except FileNotFoundError:
        #This will handle if the file is not available at given location
        print("File not found at",dataFilePath)
    except json.decoder.JSONDecodeError as err:
        #This will handle if the data breaks any of standard JSON format rules
        print("Data given in file is not in proper JSON format!!")
        print("Error details - {0}".format(err))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    else:
        #If there is not exception then this block will be executed
        print("Execution complete!")
        print("Please find output.txt file for logs!")
    finally:
        trg.close()
        gc.collect()

def writeToFile(fileObj,strToWrite):
    #Common function to write to file, so that the file writing can be disabled.
    if writeToFileFlag:
        fileObj.write(strToWrite)

def deduplicateIt(dataArr,trg):
    '''
    This function removes duplicates from the input json data. Upon receiving duplicate data this will check which one has latest date and keep that.
    '''
    print(len(dataArr))
    writeToFile(trg,"Length of original leads array - "+str(len(dataArr))+"\n\n")
    dictData = {}
    for itr in dataArr:
        try:
            #Creating key this way will eliminate the possibilities of intersecting two different keys. Each key will be unique.
            key = str(len(itr["_id"]))+itr["_id"]+str(len(itr["email"]))+itr["email"]
            #Calling compareDates to validate dates, if dates are not valid then we are not inserting it inside.
            #Considering the time to be after 1st Jan. 1970. If the date is earlier then the whole logic would be required to be changed.
            if key not in dictData and compareDates('1970-01-01T00:00:00+00:00',itr["entryDate"]):
                dictData[key] = itr
                #adding this record with this unique combination for the first time.
                writeToFile(trg,"Retained record with id-"+itr["_id"]+" and email-"+itr["email"]+".\n")
            else:
                if compareDates(dictData[key]["entryDate"],itr["entryDate"]):
                    #If current record is latest than its pre-existing duplicate and this one is latest then we are replacing previous one with this one.
                    #If the datetime is same then we are using the last occured record i.e. the current record. 
                    dictData[key] = itr
                    writeToFile(trg,"Replaces previous record with id-"+itr["_id"]+" and email-"+itr["email"]+", with current record. Since this one is latest.\n")
                else:
                    #rejected this record
                    writeToFile(trg,"Rejected record with id-"+itr["_id"]+" and email-"+itr["email"]+". Since it was already present in the data and this one is not latest.\n")

        except TypeError as err:
            #This error will be raised if there is an error with the date string. No need of doing any thing here since we have taken care of this in its function.
            writeToFile(trg,"Rejecting the record with id-"+itr["_id"]+" and email-"+itr["email"]+", as the date string does not have a valid format.\n")
        except KeyError as err:
            #This error will be raised if one of the keys is/are missing.
            writeToFile(trg,"Rejecting the record as the key is missing from the data.\n")
            print("Key missing from the given data record - {0}".format(err))

    print(len(dictData.values()))
    writeToFile(trg,"\nLength of final leads array - "+str(len(dictData.values()))+"\n\n")
    return list(dictData.values())

def compareDates(dateStr1,dateStr2):
    '''
    This function will covert two strings to data type object and compare them.
    Timestamp is calculated to comapre two dates. This timestamp will include the gmtoffset(time zone adjustment).
    '''
    try:
        dateStr1 = dateStr1[:-3]+dateStr1[-2:]
        dateStr2 = dateStr2[:-3]+dateStr2[-2:]
        tm1 = time.strptime(dateStr1, "%Y-%m-%dT%H:%M:%S%z")
        tm2 = time.strptime(dateStr2, "%Y-%m-%dT%H:%M:%S%z")
        
        mkt1 = time.mktime(tm1) + tm1.tm_gmtoff
        mkt2 = time.mktime(tm2) + tm2.tm_gmtoff
        #print(dateStr1,"-", mkt1," ; ",dateStr2,"-", mkt2)

        if mkt1 <= mkt2:
            return True
        else:
            return False

    except (OverflowError, ValueError) as err:
        #This error will be raised if the input value cannot be represented as a valid time for mktime() function. The error depends on who raise it, c library or python.
        print("Cannot convert given data string to valid time!")
        print("Error details - {0}".format(err))
        raise TypeError
    except ValueError as err:
        #This error will be raised if the given date string is invalid.
        print("Given date string is not valid!!")
        print("Error details - {0}".format(err))
        raise TypeError
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise TypeError

def parseJSON(dataStr):
    '''
    This function conerts json string to python object and returns this object.
    '''
    return json.loads(dataStr)

def readFromFile(path):
    '''
    This function reads text from file and returns it.
    '''
    with open(path) as file:
        data = file.read()
    return data

def jdefault(o):
    #Enables objects to be converted to json string.
    if isinstance(o, set):
        return list(o)
    return o.__dict__

def convertToJson(data):
    '''
    This function will convert python object to json string and returns this string.
    '''
    #return json.dumps(data, default=jdefault)
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    main()
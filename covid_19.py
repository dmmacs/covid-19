#! /home/dmmacs/anaconda3/bin/python3
#############################################################################
# Data Source: https://covidtracking.com/
#  
# 
# 
# 
#############################################################################

from requests import request
from requests.exceptions import RequestException
from requests import get
import json
from datetime import datetime
from datetime import timedelta
import platform
import pytz
import csv

import time
import os
import shutil

import buildIndex

from contextlib import closing


def getRapidApiData():

    print("Running Rapid Data")
    fname = "jsonData.txt"
    # Load Saved Data First
    if os.path.exists(fname):
        with open(fname,"r", encoding="UTF-8") as fin:
            jsonData = json.load(fin)
    fname1 = "az.txt"
    if os.path.exists(fname1):
        with open(fname1,"r", encoding="UTF-8") as fin:
            jsonDataAZ = json.load(fin)


    # Get Date from last entry
    # lastFDate = list(jsonData[-1].keys())[0]

    # lastDate = datetime.strptime(lastFDate,"%Y-%m-%d")

    now = datetime.now()
    # today = datetime(year=now.year, month=now.month, day=now.day,hour=0, minute=0, second=0)

    url = "https://covid-19-data.p.rapidapi.com/report/country/name"
    headers = {
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
        'x-rapidapi-key': "017581f6cfmshc8f39f291c879dfp1140dejsn60deff78a7b2"
        }

    url = "https://covid-19-data.p.rapidapi.com/country/code"
    querystring = {"format":"json","code":"USA"}
    response = request("GET", url, headers=headers, params=querystring)

    fileDateStr = ""
    if response.status_code == 200:
        tmpjsonData = response.json()
        dateStr = f"{now:%Y-%m-%d}"
        totalCases = tmpjsonData[0]['confirmed']
        totalDeaths = tmpjsonData[0]['deaths']

        tmpjsonData = jsonData[-1]
        if dateStr == list(tmpjsonData.keys())[0]:
            jsonData[-1] = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
        else:
            jsonData.append({dateStr:{"cases":totalCases,"deaths":totalDeaths}})

    url2 = "https://covid-19-data.p.rapidapi.com/report/country/name"
    querystring = {"format":"json","code":"USA"}
    yesterday = now + timedelta(days=-1)
    dateStr = f"{yesterday:%Y-%m-%d}"
#    dateStr = f"{now:%Y-%m-16}"
    querystring = {"date-format":"YYYY-MM-DD","format":"json","date":dateStr,"name":"USA"}
    response = request("GET", url2, headers=headers, params=querystring)
    if response.status_code == 200:
        tmpjsonData = response.json()
        dateStr = f"{yesterday:%Y-%m-%d}"
        totalCases = 0
        totalDeaths = 0
        totalRecovered = 0
        for prov in tmpjsonData[0]['provinces']:
            if prov['province'] == 'Arizona':
                totalCases += prov['confirmed']
                totalDeaths += prov['deaths']
                totalRecovered += prov['recovered']
                break
        if totalCases > 0:
            tmpjsonData = jsonDataAZ[-1]
            if dateStr == list(tmpjsonData.keys())[0]:
                jsonDataAZ[-1] = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
            else:
                jsonDataAZ.append({dateStr:{"cases":totalCases,"deaths":totalDeaths}})

    # Create data1.js file
    out_data1 = "//Rapid API Data\n"
    out_data1 += "row_data1 = [\n"
    for entry in jsonData:
        #print(entry)
        key = list(entry.keys())[0]
        out_data1 += "\t[\"" + key  + "\"" 
        out_data1 += ","
        out_data1 += str(entry.get(key).get("cases"))
        out_data1 += ","
        out_data1 += str(entry.get(key).get("deaths"))
        out_data1 += "],\n" # + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

    out_data1 += "];\n"

    # Create data1.js file
    out_data1 += "//Rapid API Data\n"
    out_data1 += "row_dataAZ = [\n"
    for entry in jsonDataAZ:
        #print(entry)
        key = list(entry.keys())[0]
        out_data1 += "\t[\"" + key  + "\"" 
        out_data1 += ","
        out_data1 += str(entry.get(key).get("cases"))
        out_data1 += ","
        out_data1 += str(entry.get(key).get("deaths"))
        out_data1 += "],\n" # + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

    out_data1 += "];\n"

    # UTC_TZ = pytz.timezone('UTC')
    # Eastern_TZ = pytz.timezone("US/Eastern")
    # Mountain_TZ = pytz.timezone("US/Mountain")
    AZ_TZ = pytz.timezone("US/Arizona")
    
    try:
        with open("data1.js", "w", encoding="UTF-8") as out:
            # out.write(out_data)
            out.write(out_data1)
            now = datetime.now()
            out.write("updateTime=" + "\"" + now.astimezone(tz=AZ_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z') + "\"\n")
    except Exception as exc:
        print(exc)
        exit(-1)


    
    with open(fname, "w", encoding="UTF-8") as fout:
        json.dump(jsonData, fout, indent=4)



    fileDateStr = f"{now:%Y-%m-%d_%H%M%S}"

    shutil.copyfile(fname1, fileDateStr + "-" + fname1)

    with open (fname1, "w", encoding="UTF-8") as fout:
        json.dump(jsonDataAZ, fout, indent=4)

def getCovidTrackData(area):

    print("Running CovidTracking Data for " + area)
    retJsonData = None
    if area == "us":
        url = "https://covidtracking.com/api/v1/" + area + "/current.json"
        url = "https://api.covidtracking.com/v1/" + area + "/current.json"
        response = request("GET", url, headers="", params="")

        if response.status_code == 200:
            tmpData = response.json()
            # print(json.dumps(response.json(), indent=4))
            totalCases = tmpData[0]['positive']
            totalDeaths = tmpData[0]['death']
            tmpStr = str(tmpData[0]['date'])
            dateStr = tmpStr[0:4] + "-" + tmpStr[4:6] + "-" + tmpStr[6:8]
            
            #tmpjsonData = jsonDataAZ[-1]
            retJsonData = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}

    else:
        url = "https://covidtracking.com/api/v1/states/" + area + "/current.json"
        url = "https://api.covidtracking.com/v1/states/" + area + "/current.json"
        response = request("GET", url, headers="", params="")

        if response.status_code == 200:
            tmpData = response.json()
            # print(json.dumps(response.json(), indent=4))
            totalCases = tmpData['positive']
            totalDeaths = tmpData['death']
            tmpStr = str(tmpData['date'])
            dateStr = tmpStr[0:4] + "-" + tmpStr[4:6] + "-" + tmpStr[6:8]
            
            #tmpjsonData = jsonDataAZ[-1]
            retJsonData = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
    return(retJsonData)

def gethistoryData(fname):
    jsonData = None
    if os.path.exists(fname):
        with open(fname,"r", encoding="UTF-8") as fin:
            jsonData = json.load(fin)

    return(jsonData)

def createOutData(jsonData, varName):
    # now = datetime.now()

    # dateStr = f"{now:%Y-%m-%d}"
    
    OutStr = varName + " = [\n"
    for entry in jsonData:
        #print(entry)
        key = list(entry.keys())[0]
        OutStr += "\t[\"" + key  + "\"" 
        OutStr += ","
        OutStr += str(entry.get(key).get("cases"))
        OutStr += ","
        OutStr += str(entry.get(key).get("deaths"))
        OutStr += "],\n" # + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

    OutStr += "];\n"
    return (OutStr)

def AddNewData(new, history):
    
    # now = datetime.now()
    # dateStr = f"{now:%Y-%m-%d}"

    newDate = list(new.keys())[0]
    oldDate = list(history[-1].keys())[0]
    if newDate == oldDate:
    # if dateStr == list(new.keys())[0]:
        history[-1] = new
    else:
        history.append(new)

    return (history)


def udpateStateData(area):

    jsonData = gethistoryData(area.lower() + ".txt")
    tmpOutData = getCovidTrackData(area.lower())
    jsonData = AddNewData(tmpOutData, jsonData)
    fname = area.lower() + ".txt"
    with open(fname, "w", encoding="UTF-8") as fout:
        json.dump(jsonData, fout, indent=4)
    outStr = createOutData(jsonData, "row_data" + area)

    return outStr

def getAllCurrentData(stateData):
    start = time.time()

    stateData.remove("US")
    #getCDCData()

    #getRapidApiData()
    # Get US Data
    USjsonData = gethistoryData("jsonData.txt")
    tmpOutData = getCovidTrackData("us")
    USjsonData = AddNewData(tmpOutData, USjsonData)
    
    fname = "jsonData.txt"
    with open(fname, "w", encoding="UTF-8") as fout:
        json.dump(USjsonData, fout, indent=4)
    outStr = ""
    outStr += createOutData(USjsonData, "row_data1")

    for area in stateData:
        outStr += udpateStateData(area)

    ###### Output updateTime at end of tile
    AZ_TZ = pytz.timezone("US/Arizona")
    fname = "data1.js"
    with open(fname, "w", encoding="UTF-8") as out:
        # out.write(out_data)
        out.write(outStr)
        now = datetime.now()
        out.write("updateTime=" + "\"" + now.astimezone(tz=AZ_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z') + "\"\n")


    end = time.time()
    txt = 'Completed covid-19 current data collection in {elapsedTime:0.2f} s'
    print(txt.format(elapsedTime=(end-start)))
    # print('Completed covid-19 current data collection in {0.2f} s'.format(end - start))


if __name__ == "__main__":
    stateData = ["AZ","IL", "MI", "FL", "AL", "CA", "NY", "NJ","GA"]    
    stateData = buildIndex.get_state_list()

    getAllCurrentData(stateData)

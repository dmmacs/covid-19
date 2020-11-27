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

from pathlib import Path
import time
import os
import shutil

import buildIndex

from contextlib import closing


Pop_data = {}

# def getRapidApiData():

#     print("Running Rapid Data")
#     fname = "jsonData.txt"
#     # Load Saved Data First
#     if os.path.exists(fname):
#         with open(fname,"r", encoding="UTF-8") as fin:
#             jsonData = json.load(fin)
#     fname1 = "az.txt"
#     if os.path.exists(fname1):
#         with open(fname1,"r", encoding="UTF-8") as fin:
#             jsonDataAZ = json.load(fin)


#     # Get Date from last entry
#     # lastFDate = list(jsonData[-1].keys())[0]

#     # lastDate = datetime.strptime(lastFDate,"%Y-%m-%d")

#     now = datetime.now()
#     # today = datetime(year=now.year, month=now.month, day=now.day,hour=0, minute=0, second=0)

#     url = "https://covid-19-data.p.rapidapi.com/report/country/name"
#     headers = {
#         'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
#         'x-rapidapi-key': "017581f6cfmshc8f39f291c879dfp1140dejsn60deff78a7b2"
#         }

#     url = "https://covid-19-data.p.rapidapi.com/country/code"
#     querystring = {"format":"json","code":"USA"}
#     response = request("GET", url, headers=headers, params=querystring)

#     fileDateStr = ""
#     if response.status_code == 200:
#         tmpjsonData = response.json()
#         dateStr = f"{now:%Y-%m-%d}"
#         totalCases = tmpjsonData[0]['confirmed']
#         totalDeaths = tmpjsonData[0]['deaths']

#         tmpjsonData = jsonData[-1]
#         if dateStr == list(tmpjsonData.keys())[0]:
#             jsonData[-1] = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
#         else:
#             jsonData.append({dateStr:{"cases":totalCases,"deaths":totalDeaths}})

#     url2 = "https://covid-19-data.p.rapidapi.com/report/country/name"
#     querystring = {"format":"json","code":"USA"}
#     yesterday = now + timedelta(days=-1)
#     dateStr = f"{yesterday:%Y-%m-%d}"
# #    dateStr = f"{now:%Y-%m-16}"
#     querystring = {"date-format":"YYYY-MM-DD","format":"json","date":dateStr,"name":"USA"}
#     response = request("GET", url2, headers=headers, params=querystring)
#     if response.status_code == 200:
#         tmpjsonData = response.json()
#         dateStr = f"{yesterday:%Y-%m-%d}"
#         totalCases = 0
#         totalDeaths = 0
#         totalRecovered = 0
#         for prov in tmpjsonData[0]['provinces']:
#             if prov['province'] == 'Arizona':
#                 totalCases += prov['confirmed']
#                 totalDeaths += prov['deaths']
#                 totalRecovered += prov['recovered']
#                 break
#         if totalCases > 0:
#             tmpjsonData = jsonDataAZ[-1]
#             if dateStr == list(tmpjsonData.keys())[0]:
#                 jsonDataAZ[-1] = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
#             else:
#                 jsonDataAZ.append({dateStr:{"cases":totalCases,"deaths":totalDeaths}})

#     # Create data1.js file
#     out_data1 = "//Rapid API Data\n"
#     out_data1 += "row_data1 = [\n"
#     for entry in jsonData:
#         #print(entry)
#         key = list(entry.keys())[0]
#         out_data1 += "\t[\"" + key  + "\"" 
#         out_data1 += ","
#         out_data1 += str(entry.get(key).get("cases"))
#         out_data1 += ","
#         out_data1 += str(entry.get(key).get("deaths"))
#         out_data1 += "],\n" # + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

#     out_data1 += "];\n"

#     # Create data1.js file
#     out_data1 += "//Rapid API Data\n"
#     out_data1 += "row_dataAZ = [\n"
#     for entry in jsonDataAZ:
#         #print(entry)
#         key = list(entry.keys())[0]
#         out_data1 += "\t[\"" + key  + "\"" 
#         out_data1 += ","
#         out_data1 += str(entry.get(key).get("cases"))
#         out_data1 += ","
#         out_data1 += str(entry.get(key).get("deaths"))
#         out_data1 += "],\n" # + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

#     out_data1 += "];\n"

#     # UTC_TZ = pytz.timezone('UTC')
#     # Eastern_TZ = pytz.timezone("US/Eastern")
#     # Mountain_TZ = pytz.timezone("US/Mountain")
#     AZ_TZ = pytz.timezone("US/Arizona")
    
#     try:
#         with open("data1.js", "w", encoding="UTF-8") as out:
#             # out.write(out_data)
#             out.write(out_data1)
#             now = datetime.now()
#             out.write("updateTime=" + "\"" + now.astimezone(tz=AZ_TZ).strftime('%d-%b-%Y %I:%M:%S %p %Z') + "\"\n")
#     except Exception as exc:
#         print(exc)
#         exit(-1)


    
#     with open(fname, "w", encoding="UTF-8") as fout:
#         json.dump(jsonData, fout, indent=4)



#     fileDateStr = f"{now:%Y-%m-%d_%H%M%S}"

#     shutil.copyfile(fname1, fileDateStr + "-" + fname1)

#     with open (fname1, "w", encoding="UTF-8") as fout:
#         json.dump(jsonDataAZ, fout, indent=4)

def getCovidTrackData(area):

    print("Running CovidTracking Data for " + area)
    retJsonData = None
    if area == "us":
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
            retJsonData = {dateStr:tmpData[0]}
            # retJsonData = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}

    else:
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
            # retJsonData = {dateStr:{"cases":totalCases,"deaths":totalDeaths}}
            retJsonData = {dateStr:tmpData}
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
    
    mv_ave_data = []
    prev_cases = 0
    case_sum = 0
    ave_window = 7

    OutStr = varName + " = [\n"
    for entry in jsonData:
        #print(entry)
        key = list(entry.keys())[0]
        OutStr += "\t[\"" + key  + "\"" 
        OutStr += ","
        cases = 0
        if entry.get(key).get("positive") is None:
            OutStr += str(0)
        else:
            OutStr += str(entry.get(key).get("positive"))
            cases = entry.get(key).get("positive")
        OutStr += ","
        if entry.get(key).get("death") is None:
            OutStr += str(0)
        else:
            OutStr += str(entry.get(key).get("death"))

        OutStr += ","
        diff = cases - prev_cases
        prev_cases = cases
        case_sum += diff
        if len(mv_ave_data) == ave_window:
            case_sum -= mv_ave_data[0]
            mv_ave_data.pop(0)
        mv_ave_data.append(diff)
        average = case_sum / ave_window

        OutStr += str(average)

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

def getCSVHeadings(area):
    jsonData = gethistoryData(area.lower() + ".txt")

    retVal = "state" + "," + "Region" + "," + "Division" + ","
    for row in jsonData:
        retVal += list(row.keys())[0] + ","
    return retVal

def updateCSVFile(area):
    jsonData = gethistoryData(area.lower() + ".txt")

    population = 0
    region = ""
    division = ""
    for key,value in Pop_data.items():
        if key == area:
            population = int(value.get('population')) / 100000
            region =  value.get('region')
            division = value.get('division')
            break

    retVal = area.upper() + ","
    for row in jsonData:
        cases = list(row.items())[0][1].get('positive')
        if cases == None:
            cases = 0
        retVal += str(cases) + ","

    retVal2 = area.upper() + "," + region + "," + division + ","
    for row in jsonData:
        cases = list(row.items())[0][1].get('positive')
        if cases == None:
            cases = 0
        retVal2 += str(cases / population) + ","

    retVal3 = area.upper() + ","
    for row in jsonData:
        deaths = list(row.items())[0][1].get('deaths')
        if deaths is None:
            deaths = 0
        retVal3 += str(deaths) + ","
    
    retVal4 = area.upper() + ","
    for row in jsonData:
        deaths = list(row.items())[0][1].get('deaths')
        if deaths is None:
            deaths = 0
        retVal4 += str(deaths / population) + ","

    retVal5 = area.upper() + ","  + region + "," + division + ","
    cases_yesterday = 0
    for row in jsonData:
        cases = list(row.items())[0][1].get('positive')
        if cases == None:
            cases = 0
        retVal5 += str((cases - cases_yesterday) / population) + ","
        cases_yesterday = cases

    retVal6 = area.upper() + ","  + region + "," + division + ","
    cases_yesterday = 0
    for row in jsonData:
        cases = list(row.items())[0][1].get('positive')
        if cases == None:
            cases = 0
        retVal6 += str((cases - cases_yesterday)) + ","
        cases_yesterday = cases

    return retVal, retVal2, retVal3, retVal4, retVal5, retVal6

def getAllCurrentData(stateData):
    start = time.time()

    stateData.remove("US")
    # Get US Data, using CovidTrack
    USjsonData = gethistoryData("us.txt")
    tmpOutData = getCovidTrackData("us")
    USjsonData = AddNewData(tmpOutData, USjsonData)
    
    fname = "us.txt"
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

    outStr = getCSVHeadings("az") + "\n"
    outStr2 = outStr
    outStr3 = outStr
    outStr4 = outStr
    outStr5 = outStr
    outStr6 = outStr
    for area in stateData:
        val1, val2, val3, val4, val5, val6 = updateCSVFile(area)
        outStr += val1 + "\n"
        outStr2 += val2 + "\n"
        outStr3 += val3 + "\n"
        outStr4 += val4 + "\n"
        outStr5 += val5 + "\n"
        outStr6 += val6 + "\n"
        # outStr += updateCSVFile(area) + "\n"
    
    with open("data.csv", "w", encoding="UTF-8") as out:
        out.write(outStr)
    
    with open("data1.csv", "w", encoding="UTF-8") as out:
        out.write(outStr2)

    with open("data_deaths.csv", "w", encoding="UTF-8") as out:
        out.write(outStr3)

    with open("data_deaths_pop.csv", "w", encoding="UTF-8") as out:
        out.write(outStr4)

    with open("data_daily_cases_pop.csv", "w", encoding="UTF-8") as out:
        out.write(outStr5)

    with open("data_daily_cases.csv", "w", encoding="UTF-8") as out:
        out.write(outStr6)

    end = time.time()
    txt = 'Completed covid-19 current data collection in {elapsedTime:0.2f} s'
    print(txt.format(elapsedTime=(end-start)))
    # print('Completed covid-19 current data collection in {0.2f} s'.format(end - start))


if __name__ == "__main__":
    start = time.time()


    # Load State Population Data
    with open("pop_detail.json", "r", encoding="UTF-8") as fin:
        Pop_data = json.load(fin)
    stateData = ["AZ","IL", "MI", "FL", "AL", "CA", "NY", "NJ","GA"]    
    stateData = buildIndex.get_state_list()

    print(stateData)

    getAllCurrentData(stateData)

    end = time.time()

    print()
    print(Path(__file__).stem + ' completed in ' + str(timedelta(seconds=end-start)) + ' ({:02.3F} secdonds)'.format(end-start))


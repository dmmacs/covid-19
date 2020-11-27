import requests
import json
from datetime import datetime
from datetime import timedelta
import time
import os
import buildIndex
from pathlib import Path

def createEmptyEntry(dateStr, area):
    return {
            "date": dateStr.replace("-",""),
            "state": area.upper(),
            "positive": 0,
            "probableCases": 0,
            "negative": 0,
            "pending": None,
            "totalTestResultsSource": "totalTestsPeopleViral",
            "totalTestResults": 0,
            "hospitalizedCurrently": 0,
            "hospitalizedCumulative": 0,
            "inIcuCurrently": 0,
            "inIcuCumulative": None,
            "onVentilatorCurrently": 0,
            "onVentilatorCumulative": None,
            "recovered": 0,
            "dataQualityGrade": "A+",
            "lastUpdateEt": None,
            "dateModified": None,
            "checkTimeEt": None,
            "death": 0,
            "hospitalized": 0,
            "dateChecked": None,
            "totalTestsViral": None,
            "positiveTestsViral": None,
            "negativeTestsViral": None,
            "positiveCasesViral": 0,
            "deathConfirmed": 0,
            "deathProbable": 0,
            "totalTestEncountersViral": None,
            "totalTestsPeopleViral": 0,
            "totalTestsAntibody": 0,
            "positiveTestsAntibody": None,
            "negativeTestsAntibody": None,
            "totalTestsPeopleAntibody": None,
            "positiveTestsPeopleAntibody": None,
            "negativeTestsPeopleAntibody": None,
            "totalTestsPeopleAntigen": None,
            "positiveTestsPeopleAntigen": None,
            "totalTestsAntigen": None,
            "positiveTestsAntigen": None,
            "fips": "04",
            "positiveIncrease": 0,
            "negativeIncrease": 0,
            "total": 0,
            "totalTestResultsIncrease": 0,
            "posNeg": 0,
            "deathIncrease": 9,
            "hospitalizedIncrease": 0,
            "hash": None,
            "commercialScore": 0,
            "negativeRegularScore": 0,
            "negativeScore": 0,
            "positiveScore": 0,
            "score": 0,
            "grade": ""
        }

def getData(area):
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day,hour=0, minute=0, second=0)
    #now = datetime.now()
    #now = now + timedelta(days=1)

    print("Getting data for " + area.lower())
    fname = area.lower() + ".txt"

    sampleDate = datetime(year=2020, month=1, day=22, hour=0, minute=0, second=0)
    # sampleDate = datetime(year=2020, month=6, day=15, hour=0, minute=0, second=0)

    cnt = 0

    tmpData = []
    # US Historical Data
    while sampleDate < today:
        # https://covidtracking.com/api/v1/us/20200501.json
        dateStr = f"{sampleDate:%Y-%m-%d}"
        urldateStr = f"{sampleDate:%Y%m%d}"

        if area.lower() == "us":
            url = "https://covidtracking.com/api/v1/us/" + urldateStr + ".json"
        else:
            url = "https://api.covidtracking.com/v1/states/" + area.lower() + "/" + urldateStr + ".json"

        response = requests.request("GET", url, headers="", params="")
        if response.status_code == 200:
            jsonData = response.json()
            totalCases = jsonData["positive"]
            totalDeaths = jsonData['death']
            if totalDeaths is None:
                totalDeaths = 0
            totalRecovered = 0
            totalTests = jsonData["totalTestResults"]
            totalPositive = jsonData["positive"]

            # tmpData.append({dateStr:{"cases":totalCases,"deaths":totalDeaths,"recovered":totalRecovered,"positive":totalPositive,"totalTests":totalTests}})
            tmpData.append({dateStr:jsonData})
            print("found:" + dateStr,"",area.lower())
        else:
            tmpData.append({dateStr:createEmptyEntry(dateStr, area.lower())})
            # tmpData.append({dateStr:{"cases":0,"deaths":0,"recovered":0}})
            print(dateStr,"",area.lower())

        sampleDate += timedelta(days=1)
        cnt += 1

        # if cnt > 3:
        #     break
        # time.sleep(1)

    with open(fname.lower(), 'w',encoding="UTF-8") as fout:
        fout.write(json.dumps(tmpData, indent=4))


if __name__ == "__main__":

    start = time.time()

    stateData = buildIndex.get_state_list()
    
    for area in stateData:
        getData(area)
    # getData("az")
    
    end = time.time()

    print()
    print(Path(__file__).stem + ' completed in ' + str(timedelta(seconds=end-start)) + ' ({:02.3F} secdonds)'.format(end-start))



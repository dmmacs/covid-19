import requests
import json
from datetime import datetime
from datetime import timedelta
import time
import os


def getData(area):
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day,hour=0, minute=0, second=0)
    #now = datetime.now()
    #now = now + timedelta(days=1)

    fname = area + ".txt"

    sampleDate = datetime(year=2020, month=1, day=22, hour=0, minute=0, second=0)
    # sampleDate = datetime(year=2020, month=6, day=15, hour=0, minute=0, second=0)

    cnt = 0

    tmpData = []
    # US Historical Data
    while sampleDate < today:
        # https://covidtracking.com/api/v1/us/20200501.json
        dateStr = f"{sampleDate:%Y-%m-%d}"
        urldateStr = f"{sampleDate:%Y%m%d}"

        if area == "us":
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
            tmpData.append({dateStr:{"cases":totalCases,"deaths":totalDeaths,"recovered":totalRecovered}})
            print("found:" + dateStr,"",area)
        else:
            tmpData.append({dateStr:{"cases":0,"deaths":0,"recovered":0}})
            print(dateStr,"",area)

        sampleDate += timedelta(days=1)
        cnt += 1

        # if cnt > 3:
        #     break
        # time.sleep(1)

    with open(fname.lower(), 'w',encoding="UTF-8") as fout:
        fout.write(json.dumps(tmpData, indent=4))


if __name__ == "__main__":
    getData("il")
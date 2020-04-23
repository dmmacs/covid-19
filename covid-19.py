#! /home/dmmacs/anaconda3/bin/python3


from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import json
from datetime import datetime
import platform
import pytz
import csv

from contextlib import closing
from requests import get


def getMonth(s):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(s)+1

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def ScrapeData():

    # with open("contrived.html", "r", encoding="utf-8") as fin:
    #     html = BeautifulSoup(fin, 'html.parser')
    # for p in html.select('p'):
    #     print(p)
    #     if p['id'] == 'walrus':
    #         print(p.text)
    # return

    data = simple_get("https://ourworldindata.org/grapher/daily-cases-covid-19")
    html = BeautifulSoup(data, 'html.parser')

    for bullet in html.select('li'):
        # if bullet['class'] == "tab clickable":
        print(bullet)
    # for a in html.select('a'):
    #     if bullet['class'] == "data-track-click":
    #         print(a)



if __name__ == "__main__":

    # ScrapeData()
    # exit(0)

    deathUrl = "https://www.worldometers.info/coronavirus/country/us/"
    url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
    dailyUrl = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/us-cases-epi-chart.json"
    totalUrl = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/total-cases-onset.json"
    totalUrl = "https://www.cdc.gov//coronavirus/2019-ncov/json/cumm-total-chart-data.json"

    result = requests.request('GET', deathUrl)

    rawData = result.text

    idx = rawData.find("Total Coronavirus Deaths in the United States")
    idx = rawData.find("Highcharts.chart('coronavirus-deaths-linear'", idx)

    idx = rawData.find("xAxis", idx)
    idx1 = rawData.find("yAxis", idx)-2

    tmpData = rawData[idx:idx1].strip()


    idx = tmpData.find("{") + 1
    tmpData = tmpData[idx:len(tmpData)-2]

    tmpData = tmpData.replace("[","")
    tmpData = tmpData.replace("]","")
    tmpData = tmpData.replace("}","")
    tmpData = tmpData.replace("\"","")
    tmpData = tmpData.replace("categories:","").strip()

    deathDates = tmpData.split(',')

    for i, dat in enumerate(deathDates):
        splt = dat.split(' ')
        tmpDate = datetime(year=2020, month=getMonth(splt[0]), day=int(splt[1]))
        deathDates[i] = tmpDate

    idx = rawData.find('series', idx1)
    idx = rawData.find('data:', idx) + len('data:')
    idx1 = rawData.find("responsive",idx)
    tmpData = rawData[idx:idx1].strip()
    tmpData = tmpData.replace("[","")
    tmpData = tmpData.replace("]","")
    tmpData = tmpData.replace("}","")
    tmpData = tmpData[:len(tmpData)-1].strip()
    deathData = tmpData.split(',')

    idx = rawData.find("series",idx)
    result = requests.request("GET", totalUrl)
    virus_total_data = result.json()
    
    # result = requests.request("GET", dailyUrl)
    # virus_daily_data = result.json()

    # columns = virus_daily_data['data']['columns'][0]

    daily_data = []
    total_data = []
    # for i, col in enumerate(columns):
    #     if i >= 1:
    #         daily_data.append([col,0,0,0])
    #     # print(daily_data[-1])

    # vData = virus_daily_data['data']['columns'][1]

    # total = 0
    # for i,dat in enumerate(vData):
    #     if i >= 1:
    #         total += int(dat)
    #         daily_data[i-1] = [daily_data[i-1][0], dat, total,0]
    #         # print(daily_data[i])

    #columns = virus_total_data['data']['columns'][0]
    columns = virus_total_data[0]
    vData = virus_total_data[1]

    for i, col in enumerate(columns):
        if i >= 1:
            total_data.append([col,0,0])

    for i, dat in enumerate(vData):
        if i >= 1:
            total_data[i-1] = [total_data[i-1][0], dat,0]

    # for i, total_dat in enumerate(total_data):
    #     for j, dailyDat in enumerate(daily_data):
    #         if dailyDat[0] == total_dat[0]:
    #             daily_data[j] = [daily_data[j][0],daily_data[j][1],daily_data[j][2],total_dat[1]]

    for i, dat in enumerate(total_data):
        tDate = datetime.strptime(dat[0],"%m/%d/%Y")
        for j, dDate in enumerate(deathDates):
            if (tDate-dDate).days == 0:
                total_data[i] = [total_data[i][0], total_data[i][1],deathData[j]]
            # if platform.system() == "Windows":
            #     if dat[0] == dDate.strftime("%#m/%#d/%Y"):
            #         # print(dat)
            #         total_data[i] = [total_data[i][0], total_data[i][1],deathData[j]]
            #         break
            # else:
            #     if dat[0] == dDate.strftime("%-m/%-d/%Y"):
            #         # print(dat)
            #         total_data[i] = [total_data[i][0], total_data[i][1],deathData[j]]
            #         break


    # Create data1.js file
    out_data = ""
    #    [2014,0, -.5,5.7],
    out_data += "row_data = [\n"
    for row in daily_data:
        # print(row)
        tmp = row[0].split("/")
        entry_date = datetime(year=int(tmp[2]), month=int(tmp[0]), day=int(tmp[1]))
        out_data += "\t[" + str(entry_date.year) + "," + str(entry_date.month-1) + "," + str(entry_date.day) + "," + str(row[3]) + "],\n"
        # print(out_data)
        # break
    out_data += "];\n"

    out_data1 = ""
    out_data1 += "row_data1 = [\n"
    for row in total_data:
        out_data1 += "\t[\"" + row[0] + "\"," + str(row[1]) + "," + str(row[2]) + "],\n"

    out_data1 += "];\n"

    UTC_TZ = pytz.timezone('UTC')
    Eastern_TZ = pytz.timezone("US/Eastern")
    Mountain_TZ = pytz.timezone("US/Mountain")
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


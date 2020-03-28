


import selenium
import requests
import json


def addChart(type):
    retVal = ""
    if type == "Curve":
        retVal += "function drawChart() {\n"
        retVal += "var data = google.visualization.arrayToDataTable([\n"
        retVal += "['Date', 'Sales'],\n"
        retVal += "['2004',  1000],\n"
        retVal += "['2005',  1170],\n"
        retVal += "['2006',  660],\n"
        retVal += "['2007',  1030]\n"
        retVal += "]);\n"
        retVal += "var options = {\n"
        retVal += "title: 'Covid-19 Cases',\n"
        retVal += "curveType: 'function',\n"
        retVal += "legend: { position: 'bottom' }\n"
        retVal += "};\n"

        #retVal += "var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));\n"
        retVal += "var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));\n"
        retVal += "chart.draw(data, options);\n"
        retVal += "}\n"
    elif type == "Line":
        retVal += "function drawChart() {\n"

        retVal += "var data = new google.visualization.DataTable();\n"
        retVal += "data.addColumn('number', 'Day');\n"
        retVal += "data.addColumn('number', 'Guardians of the Galaxy');\n"
        retVal += "data.addColumn('number', 'The Avengers');\n"
        retVal += "data.addColumn('number', 'Transformers: Age of Extinction');\n"

        retVal += "data.addRows([\n"
        retVal += "[1,  37.8, 80.8, 41.8],\n"
        retVal += "[2,  30.9, 69.5, 32.4],\n"
        retVal += "[3,  25.4,   57, 25.7],\n"
        retVal += "[4,  11.7, 18.8, 10.5],\n"
        retVal += "[5,  11.9, 17.6, 10.4],\n"
        retVal += "[6,   8.8, 13.6,  7.7],\n"
        retVal += "[7,   7.6, 12.3,  9.6],\n"
        retVal += "[8,  12.3, 29.2, 10.6],\n"
        retVal += "[9,  16.9, 42.9, 14.8],\n"
        retVal += "[10, 12.8, 30.9, 11.6],\n"
        retVal += "[11,  5.3,  7.9,  4.7],\n"
        retVal += "[12,  6.6,  8.4,  5.2],\n"
        retVal += "[13,  4.8,  6.3,  3.6],\n"
        retVal += "[14,  4.2,  6.2,  3.4]\n"
        retVal += "]);\n"

        retVal += "var options = {\n"
        retVal += "chart: {\n"
        retVal += "title: 'Box Office Earnings in First Two Weeks of Opening',\n"
        retVal += "subtitle: 'in millions of dollars (USD)'\n"
        retVal += "},\n"
        retVal += "width: 900,\n"
        retVal += "height: 500\n"
        retVal += "};\n"

        retVal += "var chart = new google.charts.Line(document.getElementById('linechart_material'));\n"

        retVal += "chart.draw(data, google.charts.Line.convertOptions(options));\n"
        retVal += "}\n"
    return retVal


with open("daily_data.txt", "r") as fin:
    virus_daily_data = json.load(fin)

with open("total_data.txt", "r") as fin:
    virus_total_data = json.load(fin)

url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
dailyUrl = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/us-cases-epi-chart.json"
totalUrl = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/total-cases-onset.json"


#result = requests.request("GET", url)
#urlData = result.text

#with open("tmp.txt", "w", encoding="utf-8") as out:
#    out.write(result.text)

#idx = urlData.find("<table id=\"cdc-chart-1-data\"")

#print(idx)

# headers =
# page = requests.get()


#result = requests.request("GET", totalUrl)
#print(json.dumps(result.json(), indent=4))
# with open("total_data.txt", "w", encoding="utf-8") as out:
#     out.write(json.dumps(result.json(), indent=4))
# result = requests.request("GET", dailyUrl)
# print(json.dumps(result.json(), indent=4))
# with open("daily_data.txt", "w", encoding="utf-8") as out:
#     out.write(json.dumps(result.json(), indent=4))
# exit(0)
#print(json.dumps(virus_data, indent=4))

columns = virus_daily_data['data']['columns'][0]

daily_data = []
total_data = []
for i, col in enumerate(columns):
    if i >= 1:
        daily_data.append([col,0,0,0])
    # print(daily_data[-1])

vData = virus_daily_data['data']['columns'][1]

total = 0
for i,dat in enumerate(vData):
    if i >= 1:
        total += int(dat)
        daily_data[i-1] = [daily_data[i-1][0], dat, total,0]
        # print(daily_data[i])

columns = virus_total_data['data']['columns'][0]
vData = virus_total_data['data']['columns'][1]

for i, col in enumerate(columns):
    if i >= 1:
        total_data.append([col,0])

for i, dat in enumerate(vData):
    if i >= 1:
        total_data[i-1] = [total_data[i-1][0], dat]

for i, total_dat in enumerate(total_data):
    for j, dailyDat in enumerate(daily_data):
        if dailyDat[0] == total_dat[0]:
            daily_data[j] = [daily_data[j][0],daily_data[j][1],daily_data[j][2],total_dat[1]]

# for dat in daily_data:
#     print(dat)

# Create data.js file
out_data = ""
#    [2014,0, -.5,5.7],
from datetime import datetime
out_data += "row_data = [\n"
for row in daily_data:
    # print(row)
    tmp = row[0].split("/")
    entry_date = datetime(year=int(tmp[2]), month=int(tmp[0]), day=int(tmp[1]))
    out_data += "\t[" + str(entry_date.year) + "," + str(entry_date.month) + "," + str(entry_date.day) + "," + str(row[3]) + "],\n"
    # print(out_data)
    # break
out_data += "];\n"
with open("data1.js", "w", encoding="UTF-8") as out:
    out.write(out_data)
# print(out_data)

htmlout = ""
htmlout += '<!DOCTYPE HTML>\n'
htmlout += '<html>\n<head>\n'
htmlout += '<meta charset="UTF-8">\n'
#    htmlout += '<meta scriptVersion="' + __version__ + '">\n'
htmlout += '<title>Covid-19 chart</title>\n'
htmlout += '<meta http-equiv="refresh" content="300">\n'

htmlout += '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>\n'
htmlout += '<script type="text/javascript">\n'
htmlout += "google.charts.load('current', {'packages':['corechart']});\n"
htmlout += "google.charts.setOnLoadCallback(drawChart);\n"
htmlout += addChart("Line")
htmlout += "</script>\n"

htmlout += "</head>\n"
htmlout += "<body>\n"    

htmlout += '<div id="curve_chart" style="width: 900px; height: 500px"></div>\n'

htmlout += "</body>\n"
htmlout += "</html>\n"

# with open('covid-19.html', "w", encoding="UTF-8") as fout:
#     fout.write(htmlout)


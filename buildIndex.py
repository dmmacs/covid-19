
import glob2 as glob

import sys

def html_hdr():
    outStr = ""
    outStr += "<!DOCTYPE HTML>" + "\n"
    outStr += "<html>"  + "\n"
    outStr += '\t<head>' + "\n"
    outStr += '\t\t<title>Covid-19 </title>' + "\n"
    outStr += '\t\t<link rel="shortcut icon" href="../images/favicon.jpg">' + "\n"
    outStr += '\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>' + "\n"
    outStr += '\t\t<script src="../js/sortable.js"></script>' + "\n"
    outStr += '\t\t<link href="../css/dashboard.css" rel="stylesheet" media="screen" />' + "\n"
    outStr += '\t\t<link href="../css/sortable_table.css" rel="stylesheet" media="screen" />' + "\n"
    outStr += '\t\t<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 110%; padding: 5px;} th{text-align: center;}</style>' + "\n"
    outStr += '\t\t</head>' + "\n"
    outStr += '\t<body>' + "\n"
    outStr += "\n"
    outStr += "\n"
    outStr += '\t<div>' + "\n"
    outStr += '\t\t<h1><a href="https://www.cdc.gov/coronavirus/2019-ncov/index.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2Findex.html">CDC Covid-19<a><br/></h1>' + "\n"
    outStr += "\t</div>" + "\n"
    outStr += '<p><a href="covid_bar_race_total.html">Data Visualization Total Cases</a></p>\n'
    outStr += '<p><a href="covid_bar_race_per_pop.html">Data Visualization Cases 100,000 people</a></p>\n'
    outStr += '<p><a href="covid_bar_race_per_day.html">Data Visualization Cases per Day</a></p>\n'

    return outStr

def html_ftr():
    outStr = ""
    
    outStr += '</body>' + "\n"
    outStr += '</html>' + "\n"

    return outStr

def my_sort_func():
    pass


def get_state_list():
    files = glob.glob("index*.html")

    fList = set()   

    for fname in files:
        fname = fname.replace("index", "")
        fname = fname.replace(".html", "")
        if len(fname) == 2:
            fList.add(fname)


    # print(fList)

    tmp_list = []
    tmp_list = list(fList)

    tmp_list.sort()
    tmp_list.remove("US")
    tmp_list.remove("AZ")
    tmp_list.remove("IL")
    tmp_list.remove("MI")
    # print(tmp_list)

    area_list = []
    area_list.append("US")
    area_list.append("AZ")
    area_list.append("IL")
    area_list.append("MI")
    area_list += tmp_list
    # print(area_list)

    return(area_list)


def build_index():

    area_list = get_state_list()
    
    outStr = html_hdr()

    outStr += "\t<table>\n"

    col_hdr = ["Cumulative", "Daily", "Daily Cases", "Daily Deaths","Daily Cases/100k pop", "Positivity Rate"]
    col_fname = ["", "_Daily", "_Daily_cases","_Daily_deaths", "_Daily_cases_pop", "_positivity_rate"]

    # Add Header Row
    # Blank first
    outStr += "\t\t<tr>\n"
    outStr += "\t\t\t<th>&nbsp;</th>\n"
    for hdr in col_hdr:
        outStr += '\t\t\t<th>' + hdr + '</th>\n'
    outStr += "\t\t</tr>\n"

    for area in area_list:
        outStr += "\t\t<tr>\n"
        
        outStr += '\t\t\t<td>' + area + '</td>\n'
        print(area)
        for i,suffix in enumerate(col_fname):
            print("\t" + suffix)
            outStr += "\t\t\t<td>" + '<a href="index' + area + suffix + '.html">' + area + " " + col_hdr[i] + '</a>' + "</td>\n"
    
        outStr += "\t\t</tr>\n"



    outStr += "\t</table>\n"

    outStr += html_ftr()

    fname = "tmp.txt"
    fname = "index.html"
    with open(fname, "w", encoding="UTF-8") as fout:
        fout.write(outStr)

    return area_list
    
def create_state_pop(fname, area):
    print(fname, area)
    with open(fname, "r", encoding="UTF-8") as fin:
        template = fin.read()

    findStr = 'pop = getPop("AZ") / 100000'
    newStr = findStr.replace('"AZ"', '"' + area + '"')
    template = template.replace(findStr, newStr)
    template = template.replace("AZ", area, )
    fname = fname.replace("AZ", area)
    with open(fname, "w", encoding="UTF-8") as fout:
        fout.write(template)
    pass

def create_state_ratio(fname, area):
    print(fname, area)
    with open(fname, "r", encoding="UTF-8") as fin:
        template = fin.read()

    findStr = 'pop = getPop("AZ") / 100000'
    newStr = findStr.replace('"AZ"', '"' + area + '"')
    template = template.replace(findStr, newStr)
    template = template.replace("AZ", area, )
    fname = fname.replace("1", area)
    fname = "index" + area + "_positivity_rate" + ".html"
    with open(fname, "w", encoding="UTF-8") as fout:
        fout.write(template)

    pass

if __name__ == "__main__":

    create_per_pop = ""

    if len(sys.argv) > 2:
        if sys.argv[1] == "pop":
            create_per_pop = sys.argv[2]
            areas = get_state_list()
            for state in areas:
                create_state_pop(create_per_pop, state)
        elif sys.argv[1] == "ratio":
            areas = get_state_list()
            for state in areas:
                create_state_ratio(sys.argv[2], state)



    build_index()
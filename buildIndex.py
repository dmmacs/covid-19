
import glob2 as glob


def html_hdr():
    outStr = ""
    outStr += "<!DOCTYPE HTML>" + "\n"
    outStr += "<html>"  + "\n"
    outStr += '\t<head>' + "\n"
    outStr += '\t\t<title>Covid-19 </title>' + "\n"
    outStr += '\t\t<link rel="shortcut icon" href="https://www.cdc.gov/TemplatePackage/4.0/assets/imgs/favicon.ico">' + "\n"
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

    col_hdr = ["Cumulative", "Daily", "Daily Cases", "Daily Deaths"]
    col_fname = ["", "_Daily", "_Daily_cases","_Daily_deaths"]

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


    # # Create Table
    # for i in range(5): # Rows (5)
    #     if i == 0:
    #         outStr += "\t\t<tr>\n"
    #         outStr += "\t\t\t<th>&nbsp;</th>\n"
    #         for area in area_list:
    #             outStr += "\t\t\t<th>" + area + "</th>\n"
    #         outStr += "\t\t</tr>\n"
    #     else:
    #         outStr += "\t\t<tr>\n"
    #         outStr += "\t\t\t<td>" + row_hdr[i - 1] + "</td>\n"
    #         for area in area_list:
    #             outStr += "\t\t\t<td>" + '<a href="index' + area + row_fname[i - 1] + '.html">' + area + " " + row_hdr[i-1] + '</a>' + "</td>\n"
    #         outStr += "\t\t</tr>\n"

    outStr += "\t</table>\n"

    outStr += html_ftr()

    fname = "tmp.txt"
    fname = "index.html"
    with open(fname, "w", encoding="UTF-8") as fout:
        fout.write(outStr)

    return area_list
    
if __name__ == "__main__":
    build_index()
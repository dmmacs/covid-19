

import sys
import time
import covidTracking_historic
import buildIndex
import covid_19



if __name__ == "__main__":
    start = time.time()
    state_areas = []
    for i in range(1, len(sys.argv)):
        print (i, sys.argv[i])
        state_areas.append(sys.argv[i])
        ### Create HTML Files
        new_area = sys.argv[i]
        print("Building Files for " + new_area)

        fname = "indexAZ.html"
        with open(fname, "r", encoding="UTF-8") as fin:
            tmpStr = fin.read()

        tmpStr = tmpStr.replace("AZ", new_area)
        fname = fname.replace("AZ", new_area)
        with open(fname, "w", encoding="UTF-8") as fout:
            fout.write(tmpStr)


        fname = "indexAZ_Daily.html"
        with open(fname, "r", encoding="UTF-8") as fin:
            tmpStr = fin.read()

        tmpStr = tmpStr.replace("AZ", new_area)
        fname = fname.replace("AZ", new_area)
        with open(fname, "w", encoding="UTF-8") as fout:
            fout.write(tmpStr)


        fname = "indexAZ_Daily_cases.html"
        with open(fname, "r", encoding="UTF-8") as fin:
            tmpStr = fin.read()

        tmpStr = tmpStr.replace("AZ", new_area)
        fname = fname.replace("AZ", new_area)
        with open(fname, "w", encoding="UTF-8") as fout:
            fout.write(tmpStr)


        fname = "indexAZ_Daily_deaths.html"
        with open(fname, "r", encoding="UTF-8") as fin:
            tmpStr = fin.read()

        tmpStr = tmpStr.replace("AZ", new_area)
        fname = fname.replace("AZ", new_area)
        with open(fname, "w", encoding="UTF-8") as fout:
            fout.write(tmpStr)


        ###### Get Historic Data
        covidTracking_historic.getData(new_area)


    stateData = buildIndex.build_index()
    covid_19.getAllCurrentData(stateData)

    end = time.time()
    txt = 'Completed creating new states, {states}, collection in {elapsedTime:0.2f} s'
    print(txt.format(states=state_areas, elapsedTime=(end-start)))



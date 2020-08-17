

import json
import sys


if __name__ == "__main__":
    fname ="tmp.txt"
    for i in range(1,len(sys.argv)):
        fname = sys.argv[i]
        with open(fname, "r", encoding="UTF-8") as fin:
            jsonData = json.load(fin)
        
        with open(fname, "w", encoding="UTF-8") as fout:
            json.dump(jsonData, fout,indent=4)
        
        
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import urllib.request
import datetime
import logging
import argparse
import sys
import csv
import re

LOG_FILENAME = "errors.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)
assignment3 = logging.getLogger("assignment3")
# assignment2.debug('This message should go to the log file')

def downloadData(url):
    # url="http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv"
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    hits=0
    totalrows=0
    MSIE=0
    Chrome=0
    Firefox=0
    Safari=0
    hourlist=[]
    for row in cr:
        x = re.findall(".PNG$|.JPG$|.GIF$", row[0].upper())
        y = re.findall("MSIE|CHROME|FIREFOX|SAFARI", row[2].upper())
        if x:
            hits=hits+1
        if y:
            if y[0]=="MSIE":
                MSIE=MSIE+1
            elif y[0]=="CHROME":
                Chrome=Chrome+1
            elif y[0]=="FIREFOX":
                Firefox=Firefox+1
            elif y[0]=="SAFARI":
                Safari=Safari+1
        totalrows=totalrows+1
        format_str = "%Y-%m-%d %H:%M:%S"
        datetime_obj = datetime.datetime.strptime(row[1], format_str)
        hourlist.append(datetime_obj.hour)
    rate = hits / totalrows
    percentage = "{:.1%}".format(rate)
    print("Image requests account for "+percentage+" of all requests")
    browsers={"MSIE":MSIE,"Chrome":Chrome,"Firefox":Firefox,"Safari":Safari}
    print("MSIE: "+str(MSIE))
    print("Chrome: "+str(Chrome))
    print("Firefox: "+str(Firefox))
    print("Safari: "+str(Safari))
    print("The most popular browser is "+max(browsers, key=browsers.get))
    groupsortprint(hourlist)

def groupsortprint(l):
    xx={}
    for r in l:
        if str(r) in xx.keys():
            xx[str(r)] = xx[str(r)]+1
        else:
            xx[str(r)] = 0
    sort_orders = sorted(xx.items(), key=lambda x: x[1], reverse=True)

    for i in sort_orders:
        print("Hour "+i[0]+" has "+str(i[1])+" hits")

def main(url):
    try:
        downloadData(url)
    except:
        print("Connection error or there is a data glitch")
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Url')
    parser.add_argument('url', help='the url of the file, please enter it')
    args = parser.parse_args()
    main(args.url)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

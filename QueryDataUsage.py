import os
import sys
from os import path
from datetime import datetime


__author__ = 'sandeepd'


def getFilePathFromSSID(SSID):
    return path.join(os.environ['PROGRAMDATA'], "SDXTECH", "DataUsageLogger", "{}.csv".format(SSID))


def getFields(line):
    field = line.split(",")
    dt = datetime.strptime("{} {}".format(field[0], field[1]), "%d-%m-%Y %H:%M:%S")
    return dt, int(field[2]), int(field[3])


def totalUsage(dateFrom, dateTo, filePath):
    with open(filePath, "r") as f:
        lines = f.read().splitlines()

    lines = map(lambda x: getFields(x), lines[1:])
    lines = list(filter(lambda x: dateFrom <= x[0] <= dateTo, lines))

    date0, tx0, rx0 = lines[0]

    totalTx = tx0
    totalRx = rx0

    for line in lines[1:]:
        date1, tx1, rx1 = line

        if tx1 == 0 and rx1 == 0:
            continue

        dTx, dRx = tx1 - tx0, rx1 - rx0
        tx0, rx0 = tx1, rx1
        if dTx >= 0:
            totalTx += dTx
            totalRx += dRx
        else:
            totalTx += tx0
            totalRx += rx0

    return totalTx, totalRx


def main(args):
    try:
        SSID = args[1]
        dateFrom = datetime.strptime(args[2], "%d-%m-%Y,%H:%M:%S")
        dateTo = datetime.strptime(args[3], "%d-%m-%Y,%H:%M:%S")

        print("Total transmitted: {} MB\nTotal downloaded:  {} MB"
              .format(*totalUsage(dateFrom, dateTo, getFilePathFromSSID(SSID))))
    except IndexError:
        print("Syntax:-")
        print("\t{} <SSID> <date-from> <date-to>".format(args[0]))
        print("Example:-")
        print("\t{} SDN1 24-01-2015,16:51:38 24-01-2015,17:58:12".format(args[0]))

# print(totalUsage(getFilePathFromSSID("SDN1")))
if __name__ == "__main__":
    main(sys.argv)
from os import path
import os

__author__ = 'sandeepd'


def getFilePathFromSSID(SSID):
    return path.join(os.environ['PROGRAMDATA'], "SDXTECH", "DataUsageLogger", "{}.csv".format(SSID))


def getFields(line):
    field = line.split(",")
    return field[0], field[1], int(field[2]), int(field[3])


def totalUsage(filePath):
    lines = None
    with open(filePath, "r") as f:
        lines = f.read().splitlines()

    date0, time0, tx0, rx0 = getFields(lines[1])

    totalTx = tx0
    totalRx = rx0

    for line in lines[2:]:
        date1, time1, tx1, rx1 = getFields(line)

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


print(totalUsage(getFilePathFromSSID("SDN1")))
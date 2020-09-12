# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 08:43:31 2020

@author: Salman
"""

import csv
import matplotlib.pyplot as plt

lstdata = []
N = 14
columnNames = {}
RSIind = (50,70)
StochRSIind = (0.2,0.8)

def readStockFile(strfile):
    blnFlag = False
    with open(strfile, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not blnFlag:
                i = 0
                for item in row:
                    columnNames[item] = i
                    i = i + 1
                blnFlag = True
                continue
            else:
                lstdata.append(row)

def SMMA(array, N):
    tmpSMA = array[:]
    for i in range(len(array)-3,-1,-1):
        tmpSMA[i] = (tmpSMA[i+1]*(N-1)+tmpSMA[i])/N
    return tmpSMA

def fillPrice(lstdata, columnName):
    closeprices = []
    column = columnNames[columnName]
    for n in range(0,len(lstdata)):
        closeprice = lstdata[n][column]
        closeprices.append(float(closeprice))
    return closeprices

def calcRSI(closeprices, N):
    U = []
    D = []
    for i in range(0, len(closeprices)-1):
        difference = closeprices[i] - closeprices[i+1]
        if difference > 0:
            U.append(difference)
            D.append(0)
        elif difference < 0:
            D.append(-1*difference)
            U.append(0)
        else:
            U.append(0)
            D.append(0)
    RS = []
    RSI = []
    SMMAU = SMMA(U,N)
    SMMAD = SMMA(D,N)
    for n in range(0,len(SMMAU)):
        if not SMMAD[n] == 0:
            RS.append(SMMAU[n] / SMMAD[n])
        else:
            RS.append(1000000)
        RSI.append(100 - 100/(1+RS[n]))
    return RSI

def calcStochRSI(RSI, N):
    StochRSI = []
    for i in range(0,len(RSI)-N):
        minRSI = min(RSI[i:i+N])
        maxRSI = max(RSI[i:i+N])
        if not maxRSI == minRSI:
            StochRSI.append((RSI[i]-minRSI)/(maxRSI-minRSI))
    return StochRSI


def main():
    # This program calculates RSI for a stock
    readStockFile("Iran.Khodro.csv")
    closeprices = fillPrice(lstdata,"<CLOSE>")
    RSI = calcRSI(closeprices, N)
    print("RSI = ", RSI[0])
    if (RSI[1]<RSIind[0]) and (RSI[0]>RSIind[0]):
        print("RSI: Buy Signal")
        for i in range(2,len(RSI)):
            if RSI[i] > RSIind[0]:
                break
        print("Signal Strength: ", i-1, "days")
    elif (RSI[1]>RSIind[1]) and (RSI[0]<RSIind[1]):
        print("RSI: Sell Signal")
        for i in range(2,len(RSI)):
            if RSI[i] < RSIind[1]:
                break
        print("Signal Strength: ", i-1, "days")
    StochRSI = calcStochRSI(RSI, N)
    print("StochRSI = ", StochRSI[0:20])
    if (StochRSI[1]<StochRSIind[0]) and (StochRSI[0]>StochRSIind[0]):
        print("StochRSI: Buy Signal")
        for i in range(2,len(StochRSI)):
            if StochRSI[i] > StochRSIind[0]:
                break
        print("Signal Strength: ", i-1, "days")
    elif (StochRSI[1]>StochRSIind[1]) and (StochRSI[0]<StochRSIind[1]):
        print("StochRSI: Sell Signal")
        for i in range(2,len(StochRSI)):
            if StochRSI[i] < StochRSIind[1]:
                break
        print("Signal Strength: ", i-1, "days")
    highprices = fillPrice(lstdata,"<HIGH>")
    lowprices = fillPrice(lstdata,"<LOW>")
    volumeprices = fillPrice(lstdata,"<VOL>")
    MFI = calcMFI(lowprices,highprices,closeprices,volumeprices,N)
    print("MFI = ", MFI[0])
    
def plot(RSI, StochRSI):    
    fig, axs = plt.subplots(2, 1, figsize=(5, 5))
    axs[0].plot(RSI[0:50])
    axs[1].plot(StochRSI[0:50])
    plt.show()
    
def calcMFI(low, high, close, volume,N):
    typical=[]
    flow=[]
    MFI = []
    positive = []
    negative = []
    for i in range(0,len(low)):
        typical.append((low[i]+high[i]+close[i])/3)
        flow.append(typical[i] * volume[i])
    for i in range(0,len(low)-1):
        positive.append(0)
        negative.append(0)
        if typical[i] > typical[i+1]:
            positive[i] = positive[i] + flow[i]
        elif typical[i] < typical[i+1]:
            negative[i] = negative[i] + flow[i]
    for i in range(0,len(low)-N):
        sumPos = sum(positive[i:i+N])
        sumNeg = sum(negative[i:i+N])
        if sumNeg == 0:
            MFI.append(100)
        else:
            MFI.append(100-100/(1+sumPos/sumNeg))
    return MFI

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 08:43:31 2020

@author: Salman
"""

import csv
import matplotlib.pyplot as plt

lstdata = []
N = 14
closeprices = []

def readStockFile(strfile):
    blnFlag = False
    with open(strfile, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not blnFlag:
                blnFlag = True
                continue
            else:
                lstdata.append(row)

def SMMA(array, N):
    tmpSMA = array[:]
    for i in range(len(array)-3,-1,-1):
        tmpSMA[i] = (tmpSMA[i+1]*(N-1)+tmpSMA[i])/N
    return tmpSMA

def fillPrice():
    for n in range(0,len(lstdata)):
        closeprice = lstdata[n][5]
        closeprices.append(float(closeprice))

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
            #StochRSI.append(100000)
            StochRSI.append((RSI[i]-minRSI)/(maxRSI-minRSI))
    return StochRSI


def main():
    # This program calculates RSI for a stock
    readStockFile("Iran.Khodro.csv")
    fillPrice()
    RSI = calcRSI(closeprices, N)
    print("RSI = ", RSI[0])
    StochRSI = calcStochRSI(RSI, N)
    print("StochRSI = ", StochRSI[0])
    
    fig, axs = plt.subplots(2, 1, figsize=(5, 5))
    axs[0].plot(RSI[0:50])
    axs[1].plot(StochRSI[0:50])
    
    plt.show()

if __name__ == "__main__":
    main()

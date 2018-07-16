# -*- coding: utf-8 -*-
"""
@author: Ariane Sicard Ladouceur
"""

import csv
from decimal import Decimal, ROUND_HALF_UP
import plotly
import plotly.graph_objs as go
import scipy.stats

import numpy as np


with open('testSamples.csv') as samplesFile:
    samples = csv.reader(samplesFile, delimiter=',')
    sampleID = []
    testGroup = []
    testGroupCounter = [0, 0]
    for row in samples:
        sampleID.append(row[0])
        testGroup.append(row[1])
        if row[1] == '0':
            testGroupCounter[0] += 1
        elif row[1] == '1':
            testGroupCounter[1] += 1
    print("Total group 0 = ", testGroupCounter[0], " Total group 1 = ", testGroupCounter[1])
    

with open('transData.csv') as transactionsFile:
    transactions = csv.reader(transactionsFile, delimiter=',')
    
    transGroup = [0, 0]
    sumGroup = [Decimal(0), Decimal(0)]
    rebillCount = [0, 0]
    rebillData = [[0] * 20, [0] * 20]
    rebillDataCounter = 0
    cbCount = [0, 0]
    cbData = [[0] * 10, [0] * 10]
    cbDataCounter = 0
    refundCount = [0, 0]
    refundData = [[0] * 10, [0] * 10]
    refundDataCounter = 0
    
    totTransNum = [0,0]
    lastTrans = ['0', 'nothing']
    for row in transactions:
        try:
            thisTrans = [row[1], row[2]]
            
            sampleIndex = sampleID.index(row[1])
            group = testGroup[sampleIndex]
            if group == '0':
                totTransNum[0] +=1
                transGroup[0] += 1
                sumGroup[0] += Decimal(row[3]).quantize(Decimal('0.00'), rounding = ROUND_HALF_UP)
                if lastTrans == thisTrans:
                    if row[2] == 'REBILL':
                        rebillDataCounter += 1
                    elif row[2] == 'CHARGEBACK':
                        cbDataCounter += 1
                    else:
                        refundDataCounter += 1
                    continue
                
                lastTrans = thisTrans
                if thisTrans[1] == 'REBILL':
                    rebillData[0][rebillDataCounter] += 1
                elif thisTrans[1] == 'CHARGEBACK':
                    cbData[0][cbDataCounter] += 1 
                else:
                    refundData[0][refundDataCounter] += 1 
                
                
                rebillDataCounter = 0
                cbDataCounter = 0
                refundDataCounter = 0
                
                
                if thisTrans[1] == 'REBILL':
                    rebillCount[0] += 1
                    rebillDataCounter += 1
                elif thisTrans[1] == 'CHARGEBACK':
                    cbCount[0] += 1
                    cbDataCounter += 1
                else:
                    refundCount[0] += 1
                    refundDataCounter += 1
                        
            elif group == '1':
                totTransNum[1] +=1
                transGroup[1] += 1
                sumGroup[1] += Decimal(row[3]).quantize(Decimal('0.00'), rounding = ROUND_HALF_UP)
                if lastTrans == thisTrans:
                    if row[2] == 'REBILL':
                        rebillDataCounter += 1
                    elif row[2] == 'CHARGEBACK':
                        cbDataCounter += 1
                    else:
                        refundDataCounter += 1
                    continue
                
                lastTrans = thisTrans
                if thisTrans[1] == 'REBILL':
                    rebillData[1][rebillDataCounter] += 1 
                elif thisTrans[1] == 'CHARGEBACK':
                    cbData[1][cbDataCounter] += 1 
                else:
                    refundData[1][refundDataCounter] += 1  
                    
                rebillDataCounter = 0
                cbDataCounter = 0
                refundDataCounter = 0
                
                if thisTrans[1] == 'REBILL':
                    rebillCount[1] += 1
                    rebillDataCounter += 1
                elif thisTrans[1] == 'CHARGEBACK':
                    cbCount[1] += 1
                    cbDataCounter += 1
                else:
                    refundCount[1] += 1
                    refundDataCounter += 1
                    
        except Exception as e:
            continue
        
    print("TRANSACTIONS control group= ", transGroup[0], " test group = ", transGroup[1])
    print("SUMS control group = ", sumGroup[0], " test group 1 = ", sumGroup[1])
    print("At least 1 Rebill total = ", rebillCount[0] + rebillCount[1], 
          " control group = ", rebillCount[0], " test group = ", rebillCount[1])
    print("Chargebacks total = ", cbCount[0] + cbCount[1], 
          " control group = ", cbCount[0], " test group = ", cbCount[1])
    print("refunds total = ", refundCount[0] + refundCount[1], 
          " control group = ", refundCount[0], " test group = ", refundCount[1])
    
    print(totTransNum)
    
rebillControlTrace = go.Scatter(
        x=np.linspace(1, 20, 20), 
        y=rebillData[0], 
        name='control'
)
rebillTestTrace = go.Scatter(
        x=np.linspace(1, 20, 20), 
        y=rebillData[1], 
        name='test'
)    
cbControlTrace = go.Scatter(
        x=np.linspace(1, 10, 10), 
        y=cbData[0], 
        name='control'
)
cbTestTrace = go.Scatter(
        x=np.linspace(1, 10, 10), 
        y=cbData[1], 
        name='test'
)
refundControlTrace = go.Scatter(
        x=np.linspace(1, 10, 10), 
        y=refundData[0], 
        name='control'
)
refundTestTrace = go.Scatter(
        x=np.linspace(1, 10, 10), 
        y=refundData[1], 
        name='test'
)

plotly.offline.plot({
    "data": [rebillControlTrace, rebillTestTrace],
    "layout": go.Layout(title="Rebill Distribution", 
                        xaxis=dict(title='Number of Rebills'),
                        yaxis=dict(title='Number of People'))
}, auto_open=True, filename = 'Rebill Distribution.html')
    
plotly.offline.plot({
    "data": [cbControlTrace, cbTestTrace],
    "layout": go.Layout(title="Chargeback Distribution",
                        xaxis=dict(title='Number of Chargeback'),
                        yaxis=dict(title='Number of People'))
}, auto_open=True, filename = 'Chargeback Distribution.html')
    
plotly.offline.plot({
    "data": [refundControlTrace, refundTestTrace],
    "layout": go.Layout(title="Refund Distribution",
                        xaxis=dict(title='Number of Refund'),
                        yaxis=dict(title='Number of People'))
}, auto_open=True, filename = 'Refund Distribution.html')
    
    
rebillResults = scipy.stats.ttest_ind(rebillData[0], rebillData[1])
cbResults = scipy.stats.ttest_ind(cbData[0], cbData[1])
refundResults = scipy.stats.ttest_ind(refundData[0], refundData[1])

rebillMatrix = [
    ['', 'Test Statistic', 'p-value'],
    ['Sample Data', rebillResults[0], rebillResults[1]]
]
rebillTable = plotly.figure_factory.create_table(rebillMatrix, index=True)
plotly.offline.plot(rebillTable, filename='rebillTable.html', auto_open=True)  

cbMatrix = [
    ['', 'Test Statistic', 'p-value'],
    ['Sample Data', cbResults[0], cbResults[1]]
]
cbTable = plotly.figure_factory.create_table(cbMatrix, index=True)
plotly.offline.plot(cbTable, filename='cbTable.html', auto_open=True)

refundMatrix = [
    ['', 'Test Statistic', 'p-value'],
    ['Sample Data', refundResults[0], refundResults[1]]
]
refundTable = plotly.figure_factory.create_table(refundMatrix, index=True)
plotly.offline.plot(refundTable, filename='refundTable.html', auto_open=True)

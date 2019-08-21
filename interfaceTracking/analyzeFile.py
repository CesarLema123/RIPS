import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import outputAnalyzer as OA
import outputReader as OR

dreader = OR.DumpReader()             #OR.DumpReader()
df = OR.LogReader('log.Bulkmod','Step Atoms Temp Press TotEng').getDataframe()

OA.LogAnalyzer(df,100).plotColumnAgainstRT('TotEng')
OA.LogAnalyzer(df,100).plotColumnAgainstRT('Temp')
OA.LogAnalyzer(df,100).plotColumnAgainstRT('Press')




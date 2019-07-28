import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import outputAnalyzer as OA
import outputReader as OR

df = OR.LogReader('log.Bulkmod','Step Atoms Temp Press TotEng').getDataframe()

OA.LogAnalyzer(df,100).plotColumn('TotEng')



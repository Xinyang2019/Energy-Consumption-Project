import pandas as pd
import numpy as np
import string

def stripStr(name):
	return name.rstrip(string.digits)

#read csv file
file = pd.read_csv("./ahs2017n.csv", quotechar = "'")


# Get all the valid column name:
columnNameSet = set()
f = open('./column_name')
for line in f.readlines():
	line = line.strip()
	if len(line) > 3 and line[-3:] == 'XXX':
		columnNameSet.add(line[:-3])
	else:
		columnNameSet.add(line)

#Get all the data with valid column from the csv
columnList = []
for i in range(len(file.columns)):
	if file.columns[i] in columnNameSet or stripStr(file.columns[i]) in columnNameSet:
		columnList.append(file.columns[i])

#replace all the non-applicable data
for j in range(-9, -5):
	file.replace(j, np.nan, inplace = True)

#drop columns where all the values are NaN
df = file[columnList]
df.dropna(axis = 1, how = 'all', thresh = 40051, inplace = True)

#drop columns which only contain 1 unique values. (variance ＝ 0)
df = df[[col for col in df if not df[col].nunique()==1]]

df.to_csv('./cleanData.csv', index = False)

#drop columns with low variance
import pandas
from sklearn.feature_selection import VarianceThreshold
sel =VarianceThreshold(threshold=1)
sel.fit_transform(data)

m=0
for i in sel.get_support(True):
	print(data.columns[i])
	m+=1
print(m)


#use selectFromModel
data=pandas.read_csv('/Users/sherry/Desktop/python/energyProject/cleanData.csv',quotechar="'")
data=data.astype('float64', inplace = True)
data.dropna(inplace=True)

feature = data[[col for col in data.columns if col!="GASAMT"]]
lrModel = LinearRegression()
selectFromModel = SelectFromModel(lrModel)
selectFromModel.fit_transform(feature,data['GASAMT'])

nums = selectFromModel.get_support(True)
lists=[]
for i in nums:
	lists.append(data.columns[i])
print(lists)

#use RFE
import pandas
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression

data=pandas.read_csv('/Users/sherry/Desktop/python/energyProject/cleanData.csv',quotechar="'")
data=data.astype('float64', inplace = True)
data.dropna(inplace=True)
data=data.loc[1:9]

feature =data[['TOTROOMS','TOTHCAMT','PERPOVLVL','DIVISION','BLD','HHMAR','HHAGE','HHGRAD','HHNATVTY']]

rfe =RFE(
    estimator=LinearRegression(),
    n_features_to_select=5
)
sFeature = rfe.fit_transform(
    feature,
    data['ELECAMT']
)

rfe.get_support()



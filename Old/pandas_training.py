import numpy as np
import pandas as pd
#dataSet = pd.read_csv('melb_data.csv')
#len(dataSet)
#dataSet.describe()
#dataSet.info()
#dataSet.head()
#Just for Test
import numpy as np
import pandas as pd
animals = ['Lion', 'Bear', 'Cat']
p_animals=pd.Series(animals)
print(p_animals.to_string())
print(type(p_animals))
print(p_animals[2])
matrix1 = {
	'C1':1,
    'C2':2,
    'C3':3
}
matrix2 = {
	'C1':4,
    'C2':5,
    'C3':6
}
matrix3 = {
	'C1':7,
    'C2':8,
    'C3':9
}
pandas_matrix1 = pd.Series(matrix1)
pandas_matrix2 = pd.Series(matrix2)
pandas_matrix3 = pd.Series(matrix3)
dataFrame_matrix = pd.DataFrame([pandas_matrix1, pandas_matrix2 , pandas_matrix3], index = ['R1', 'R2', 'R3'])
print(dataFrame_matrix.to_string())
print(dataFrame_matrix.loc['R1':'R2'].to_string())
print("The Lenght of the matrix is",len(dataFrame_matrix))
print(dataFrame_matrix.describe())
print(dataFrame_matrix.info())

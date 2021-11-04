import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Load dataset
dataset = pd.read_csv('heart.csv')

###############
# Pre process #
###############
pre_processed_cols = []

# Age
ages = set([x for x in dataset['Age']])
dataset['PRE_AGE'] = [1. if x >= 50 else (x - min(ages)) / (50 - min(ages))
                      for x in dataset['Age']]  # Linear normalization
pre_processed_cols.append('PRE_AGE')

# Sex
dataset['PRE_SEX_M'] = [1 if x == 'M' else 0 for x in dataset['Sex']]
dataset['PRE_SEX_F'] = [1 if x == 'F' else 0 for x in dataset['Sex']]

# ChestPainType
types = set([x for x in dataset['ChestPainType']])
for _type in types:
    dataset[f'PRE_CHEST_PAIN_TYPE_{_type}'] = [
        1 if x == _type else 0
        for x in dataset['ChestPainType']
    ]
    pre_processed_cols.append(f'PRE_CHEST_PAIN_TYPE_{_type}')

# RestingBP -> 139 = High Normal (borderline)
resting_bps = set([x for x in dataset['RestingBP']])
dataset['PRE_RESTING_BP'] = [
    1. if x > 139 else (139 - min(resting_bps))/(139 - min(resting_bps))
    for x in dataset['RestingBP']
]  # Linear normalization
pre_processed_cols.append('PRE_RESTING_BP')

# Cholesterol -> 239 is the borderline
# ref: www.healthline.com/health/high-cholesterol/why-is-cholesterol-needed
# TODO: Try with 0 and 1
cholesterol = set([x for x in dataset['Cholesterol']])
dataset['PRE_CHOLESTEROL'] = [
    1. if x > 239 else (239 - min(cholesterol)) / (239 - min(cholesterol))
    for x in dataset['Cholesterol']
]  # Linear normalization
pre_processed_cols.append('PRE_CHOLESTEROL')

# FastingBS -> Already as binary (0 and 1)
dataset['PRE_FASTING_BP'] = [x for x in dataset['FastingBS']]
pre_processed_cols.append('PRE_FASTING_BP')

# RestingECG
dataset['PRE_RESTING_ECG'] = [1 if x != 'Normal' else 0
                              for x in dataset['RestingECG']]
pre_processed_cols.append('PRE_RESTING_ECG')

# MaxHR
# TODO: Try with 0 and 1
max_hrs = set([x for x in dataset['MaxHR']])
dataset['PRE_MAX_HR'] = [
    1 if x > 128 else (x - min(max_hrs)) / (max(max_hrs) - min(max_hrs))
    for x in dataset['MaxHR']
]  # Linear normalization
pre_processed_cols.append('PRE_MAX_HR')

# ExerciseAngina
dataset['PRE_EXERCISE_ANGINA'] = [1 if x == 'Y' else 0
                                  for x in dataset['ExerciseAngina']]
pre_processed_cols.append('PRE_EXERCISE_ANGINA')

# Oldpeak
oldpeaks = set([x for x in dataset['Oldpeak']])
dataset['PRE_OLDPEAK'] = [(x - min(oldpeaks)) / (max(oldpeaks) - min(oldpeaks))
                          for x in dataset['Oldpeak']]  # Linear normalization
pre_processed_cols.append('PRE_OLDPEAK')

# ST_Slope
dataset['PRE_ST_SLOPE'] = [1 if x != 'Flat' else 0
                           for x in dataset['ST_Slope']]
pre_processed_cols.append('PRE_ST_SLOPE')

#########################################
# Separate data to training and testing #
#########################################
y = dataset['HeartDisease']  # Target
x = dataset.loc[:, pre_processed_cols]  # Pre-processed data

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=845
)

# DecisionTree
dtree = DecisionTreeClassifier(criterion='entropy', max_depth=5,
                               min_samples_split=30, random_state=845)
dtree.fit(X_train, y_train)

##############
# Prediction #
##############
# DecisionTree
y_pred_train_DT = dtree.predict(X_train)
y_pred_test_DT = dtree.predict(X_test)
y_pred_train_DT_P = dtree.predict_proba(X_train)
y_pred_test_DT_P = dtree.predict_proba(X_test)

# Performance evaluation
Error_DT_Classification = np.mean(np.absolute(y_pred_test_DT - y_test))
Error_DT_MSE = np.mean((y_pred_test_DT_P[:, 1] - y_test) ** 2)

print()
print('--------- Classification Error ---------')
print(f'DTree: {Error_DT_Classification}')
print('------------------ MSE -----------------')
print(f'DTree: {Error_DT_MSE}')

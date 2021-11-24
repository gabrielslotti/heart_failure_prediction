import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
dataset = pd.read_csv('heart.csv')

###############
# Pre process #
###############
pre_processed_cols = []

# TODO: Setar o minimo.

# Age
ages = set([x for x in dataset['Age']])
dataset['PRE_AGE'] = [1. if x >= 50 else (x - min(ages)) / (50 - min(ages))
                      for x in dataset['Age']]  # Linear normalization
pre_processed_cols.append('PRE_AGE')

# Sex
dataset['PRE_SEX_M'] = [1 if x == 'M' else 0 for x in dataset['Sex']]
dataset['PRE_SEX_F'] = [1 if x == 'F' else 0 for x in dataset['Sex']]

# ChestPainType
types = ['NAP', 'ATA', 'ASY', 'TA']
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
dataset['PRE_CHOLESTEROL_CAT'] = [1 if x > 239 else 0
                                  for x in dataset['Cholesterol']]
pre_processed_cols.append('PRE_CHOLESTEROL_CAT')

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
dataset['PRE_MAX_HR_CAT'] = [1 if x > 128 else 0
                             for x in dataset['MaxHR']]
pre_processed_cols.append('PRE_MAX_HR_CAT')

max_hrs = set([x for x in dataset['MaxHR']])
dataset['PRE_MAX_HR'] = [
    1. if x > 128 else (x - min(max_hrs)) / (max(max_hrs) - min(max_hrs))
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

##########################################
# Separate data for training and testing #
##########################################
y = dataset['HeartDisease']  # Target
x = dataset.loc[:, pre_processed_cols]  # Pre-processed data

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=845
)

# DecisionTree
dtree = DecisionTreeClassifier(criterion='entropy', max_depth=5,
                               min_samples_split=30, random_state=845)
dtree.fit(X_train, y_train)


# RandomForest
random_forest = RandomForestClassifier(n_estimators=10, max_depth=5,
                                       min_samples_split=30, random_state=845)
random_forest.fit(X_train, y_train)

# ExtraTrees
extra_trees = ExtraTreesClassifier(n_estimators=10, max_depth=5,
                                   min_samples_split=30, random_state=845)
extra_trees.fit(X_train, y_train)

# Bagging DecisionTree
bagging_dtree = BaggingClassifier(base_estimator=dtree, n_estimators=10,
                                  random_state=845)
bagging_dtree.fit(X_train, y_train)

# Naive-Bayes
nb = MultinomialNB()
nb.fit(X_train, y_train)

# Bagging Naive-Bayes
bagging_nb = BaggingClassifier(base_estimator=nb, n_estimators=10,
                               random_state=845)
bagging_nb.fit(X_train, y_train)

# RNA
RNA = MLPClassifier(
    activation='tanh', alpha=1e-05, batch_size='auto',
    beta_1=0.9, beta_2=0.999, early_stopping=True,
    epsilon=1e-08, hidden_layer_sizes=(17, 3), learning_rate='constant',
    learning_rate_init=0.001, max_iter=2000000, momentum=0.9,
    nesterovs_momentum=True, power_t=0.5, random_state=845, shuffle=True,
    solver='lbfgs', tol=0.0001, validation_fraction=0.3, verbose=False,
    warm_start=False
)
RNA.fit(X_train, y_train)


##############
# Prediction #
##############
# DecisionTree
y_pred_train_DT = dtree.predict(X_train)
y_pred_test_DT = dtree.predict(X_test)
y_pred_train_DT_P = dtree.predict_proba(X_train)
y_pred_test_DT_P = dtree.predict_proba(X_test)

# RandomForest
y_pred_train_RF = random_forest.predict(X_train)
y_pred_test_RF = random_forest.predict(X_test)
y_pred_train_RF_P = random_forest.predict_proba(X_train)
y_pred_test_RF_P = random_forest.predict_proba(X_test)

# ExtraTress
y_pred_train_ETC = extra_trees.predict(X_train)
y_pred_test_ETC = extra_trees.predict(X_test)
y_pred_train_ETC_P = extra_trees.predict_proba(X_train)
y_pred_test_ETC_P = extra_trees.predict_proba(X_test)

# Bagging DecisionTree
y_pred_train_BAG_DT = bagging_dtree.predict(X_train)
y_pred_test_BAG_DT = bagging_dtree.predict(X_test)
y_pred_train_BAG_DT_P = bagging_dtree.predict_proba(X_train)
y_pred_test_BAG_DT_P = bagging_dtree.predict_proba(X_test)

# Bagging NB
y_pred_train_BAG_NB = bagging_nb.predict(X_train)
y_pred_test_BAG_NB = bagging_nb.predict(X_test)
y_pred_train_BAG_NB_P = bagging_nb.predict_proba(X_train)
y_pred_test_BAG_NB_P = bagging_nb.predict_proba(X_test)

# Naive-Bayes
y_pred_train_NB = nb.predict(X_train)
y_pred_test_NB = nb.predict(X_test)
y_pred_train_NB_P = nb.predict_proba(X_train)
y_pred_test_NB_P = nb.predict_proba(X_test)

# RNA
y_pred_train_RNA = RNA.predict(X_train)
y_pred_test_RNA = RNA.predict(X_test)
y_pred_train_RNA_P = RNA.predict_proba(X_train)
y_pred_test_RNA_P = RNA.predict_proba(X_test)


##########################
# Performance evaluation #
##########################
# DecisionTree
Error_DT_Classification = np.mean(np.absolute(y_pred_test_DT - y_test))
Error_DT_MSE = np.mean((y_pred_test_DT_P[:, 1] - y_test) ** 2)

# RandomForest
Error_RF_Classification = np.mean(np.absolute(y_pred_test_RF - y_test))
Error_RF_MSE = np.mean((y_pred_test_RF_P[:, 1] - y_test) ** 2)

# ExtraTrees
Error_ETC_Classification = np.mean(np.absolute(y_pred_test_ETC - y_test))
Error_ETC_MSE = np.mean((y_pred_test_ETC_P[:, 1] - y_test) ** 2)

# Bagging DecisionTree
Error_BAG_DT_Classification = np.mean(np.absolute(y_pred_test_BAG_DT - y_test))
Error_BAG_DT_MSE = np.mean((y_pred_test_BAG_DT_P[:, 1] - y_test) ** 2)

# Bagging Naive-Bayes
Error_BAG_NB_Classification = np.mean(np.absolute(y_pred_test_BAG_NB - y_test))
Error_BAG_NB_MSE = np.mean((y_pred_test_BAG_NB_P[:, 1] - y_test) ** 2)

# Naive-Bayes
Error_NB_Classification = np.mean(np.absolute(y_pred_test_NB - y_test))
Error_NB_MSE = np.mean((y_pred_test_NB_P[:, 1] - y_test) ** 2)

# RNA
Error_RNA_Classification = np.mean(np.absolute(y_pred_test_RNA - y_test))
Error_RNA_MSE = np.mean((y_pred_test_RNA_P[:, 1] - y_test) ** 2)


print()
print('--------- Classification Error ---------')
print(f'DecisionTree: {Error_DT_Classification}')
print(f'ExtraTrees: {Error_ETC_Classification}')
print(f'RandomForest: {Error_RF_Classification}')
print(f'Bagging DecisionTree: {Error_BAG_DT_Classification}')
print(f'Bagging Naive-Bayes: {Error_BAG_NB_Classification}')
print(f'Naive-Bayes: {Error_NB_Classification}')
print(f'RNA: {Error_RNA_Classification}')
print('------------------ MSE -----------------')
print(f'DecisionTree: {Error_DT_MSE}')
print(f'ExtraTrees: {Error_ETC_MSE}')
print(f'RandomForest: {Error_RF_MSE}')
print(f'Bagging DecisionTree: {Error_BAG_DT_MSE}')
print(f'Bagging Naive-Bayes: {Error_BAG_NB_MSE}')
print(f'Naive-Bayes: {Error_NB_MSE}')
print(f'RNA: {Error_RNA_MSE}')


for title, y_pred_test in (('Naive-Bayes', y_pred_test_NB),
                           ('DecisionTree', y_pred_test_DT),
                           ('ExtraTrees', y_pred_test_ETC),
                           ('RandomForest', y_pred_test_RF),
                           ('Bagging DecisionTree', y_pred_test_BAG_DT),
                           ('Bagging Naive-Bayes', y_pred_test_BAG_NB),
                           ('RNA', y_pred_test_RNA)):
    print(f'###### {title} ######')
    print('## REPORT ##')
    print(classification_report(y_test,
                                y_pred_test,
                                target_names=['Negativo', 'Positivo']))
    print('##### MATRIZ DE CONFUSÃO #####')
    print(confusion_matrix(y_test, y_pred_test))

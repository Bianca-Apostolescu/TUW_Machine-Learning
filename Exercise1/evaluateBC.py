import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

# Import and prepare data
data_bc = pd.read_csv('breast-cancer-diagnostic.shuf.lrn.csv')
data_bc.columns = data_bc.columns.str.strip()
y = data_bc[['ID', 'class']].copy()
X = data_bc.drop(['ID', 'class'], axis=1)
X_comp = pd.read_csv('breast-cancer-diagnostic.shuf.tes.csv')
X_comp.columns = X_comp.columns.str.strip()
y_comp = X_comp['ID'].copy()
X_comp = X_comp.drop(['ID'], axis=1)

# Prepare training and test sets using holdout method
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

# Define scaling method
scaler_s = StandardScaler()
scaler_n = Normalizer()
list_scaler = [scaler_s, scaler_n]

# Define outlier detection
iso = IsolationForest(contamination=0.1)
iso_ol = iso.fit_predict(X_train)
mask_iso = iso_ol != -1

ee = EllipticEnvelope(contamination=0.1)
ee_ol = ee.fit_predict(X_train)
mask_ee = ee_ol != -1

lof = LocalOutlierFactor()
lof_ol = lof.fit_predict(X_train)
mask_lof = lof_ol != -1

svm = OneClassSVM(nu=0.01)
svm_ol = svm.fit_predict(X_train)
mask_svm = svm_ol != -1

list_outlier_masks = [mask_iso, mask_ee, mask_lof, mask_svm]

#y_train = y_train[mask]
#X_train = X_train[mask]

# Scaling and preparation of classifier
pipe = make_pipeline(scaler_s, KNeighborsClassifier(n_neighbors=17, weights='distance'))
pipe.fit(X_train, y_train['class'])
y_pred = pipe.predict(X_test)

# Output performance metrics
print('K-NN')
accuracy = accuracy_score(y_test['class'], y_pred)
print(f'Accuracy: {accuracy}')

conf_mat = confusion_matrix(y_test['class'], y_pred)
print(conf_mat)

class_report = classification_report(y_test['class'], y_pred)
print("Classification Report:\n", class_report)

# Prepare training and test sets for cross-validation
scores = cross_val_score(pipe, X, y['class'], cv=5)
print(f'Cross-validation scores: {scores}')
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

# Scaling and preparation of classifier
pipe = make_pipeline(scaler_s, RandomForestClassifier())
pipe.fit(X_train, y_train['class'])
y_pred = pipe.predict(X_test)

# Output performance metrics
print('RANDOM FOREST')
accuracy = accuracy_score(y_test['class'], y_pred)
print(f'Accuracy: {accuracy}')

class_report = classification_report(y_test['class'], y_pred)
print("Classification Report:\n", class_report)

# Prepare training and test sets for cross-validation
scores = cross_val_score(pipe, X, y['class'], cv=5)
print(f'Cross-validation scores: {scores}')
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

# Scaling and preparation of classifier
pipe = make_pipeline(scaler_s, MLPClassifier(solver='lbfgs', alpha=0.0001, activation='tanh', random_state=5))
pipe.fit(X_train, y_train['class'])
y_pred = pipe.predict(X_test)

# Output performance metrics
print('MULTI LAYER PERCEPTRON')
accuracy = accuracy_score(y_test['class'], y_pred)
print(f'Accuracy: {accuracy}')

class_report = classification_report(y_test['class'], y_pred)
print("Classification Report:\n", class_report)

# Prepare training and test sets for cross-validation
scores = cross_val_score(pipe, X, y['class'], cv=5)
print(f'Cross-validation scores: {scores}')
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

# Predict unclassified test set
pipe.fit(X, y['class'])
y_pred = pipe.predict(X_comp)

# Write output file
out = pd.DataFrame(y_pred, y_comp)
out.rename({0: 'class'}, axis='columns', inplace=True)
out.to_csv('result.csv')
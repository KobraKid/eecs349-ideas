import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder

pd.set_option('display.width', 1000)

enc = OneHotEncoder(handle_unknown='ignore')
# data = pd.read_csv('D:\\Downloads\\cleaned\\Kickstarter_2017-05-15T22_21_11_300Z.csv')
data = pd.read_csv('D:\\Downloads\\cleaned\\Kickstarter_Full.csv')
print(data.head())
data.describe().transpose()

data = data.drop('/data/usd_pledged', axis=1)

one_hot = pd.get_dummies(data['/data/launched_at'], prefix='launched_at')
data = data.drop('/data/launched_at', axis=1)
data = data.join(one_hot)

# one_hot = pd.get_dummies(data['/data/created_at'], prefix='created_at')
data = data.drop('/data/created_at', axis=1)
# data = data.join(one_hot)

one_hot = pd.get_dummies(data['/data/deadline'], prefix='deadline')
data = data.drop('/data/deadline', axis=1)
data = data.join(one_hot)

one_hot = pd.get_dummies(data['/data/category/slug'])
data = data.drop('/data/category/slug', axis=1)
data = data.join(one_hot)

one_hot = pd.get_dummies(data['/data/currency'])
data = data.drop('/data/currency', axis=1)
data = data.join(one_hot)

one_hot = pd.get_dummies(data['/data/country'])
data = data.drop('/data/country', axis=1)
data = data.join(one_hot)

print(data.head)
print(data.columns)

X = data.drop('/data/state', axis=1)
y = data['/data/state']
X_train, X_test, y_train, y_test = train_test_split(X, y)
print("X_train.shape")
print(X_train.shape)
print("X_test.shape")
print(X_test.shape)
print("y_train.shape")
print(y_train.shape)
print("y_test.shape")
print(y_test.shape)
scaler = StandardScaler()

# Fit only to the training data
scaler.fit(X_train)
StandardScaler(copy=True, with_mean=True, with_std=True)

# Now apply the transformations to the data:
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
mlp = MLPClassifier(hidden_layer_sizes=(8, 4, 8), max_iter=500, batch_size=100)
mlp.fit(X_train, y_train)
predictions = mlp.predict(X_test)
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

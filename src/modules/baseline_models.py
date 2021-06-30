import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

def scale_data(data):
    scaler = StandardScaler()
    return scaler.fit_transfrom(data)

def linear_model(type, x_train, y_train, x_test, hyperparams={}):

    if type.lower() == 'linear':
        model = LinearRegression()
    elif type.lower() == 'ridge':
        model = Ridge(**hyperparams)
    elif type.lower() == 'lasso':
        model = Lasso(**hyperparams)
    elif type.lower() == 'polynomial':
        poly = PolynomialFeatures(**hyperparams)
        x_train = poly.fit_transform(x_train)

    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    return model.coef_, y_pred

def polynomial_regression(x, y, hyperparams={}):
    polyreg = PolynomialFeatures(**hyperparams)
    x = polyreg.fit_transform(x)

    X = scale_data(x)
    y = scale_data(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75)

    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)

    return linreg.coef_, y_pred

def random_forest(type, x_train, y_train, x_test, hyperparams={}):

    if type.lower() == 'classification':
        model = RandomForestClassifier(**hyperparams)
    elif type.lower() == 'regression':
        model = RandomForestRegressor(**hyperparams)
    
    model.fit(x_train, y_train)
    y_pred = model.pred(x_test)

    return y_pred

def gradient_boost(type, x_train, y_train, x_test, hyperparams={}):

    if type.lower() == 'classification':
        model = GradientBoostingClassifier(**hyperparams)
    elif type.lower() == 'regression':
        model = GradientBoostingRegressor(**hyperparams)
    
    model.fit(x_train, y_train)
    y_pred = model.pred(x_test)
    
    return y_pred

def evaluate_binary_classification(model_name, y_test, y_pred):

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1_score = recall_score(y_test, y_pred)
    rocauc_score = roc_auc_score(y_test, y_pred)

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True)
    plt.tight_layout()
    plt.title(f'{model_name}', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.show()

    return accuracy, precision, recall, f1_score, rocauc_score

def evaluate_regression(y_test, y_pred):

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return mae, mse, r2


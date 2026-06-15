import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
import shared
def logistik_reg(data):
    
    global predict
    #============== Загружаем данные ==============#
    x, y = load_breast_cancer(return_X_y=True)

    #============== Делим данные на обучающую и тестовую выборки ==============#
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=43)

    #============== Масштабируем данные ==============#
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #============== Обучаем логистическую регрессию ==============#
    model = LogisticRegression(max_iter=10000)
    model.fit(X_train_scaled, y_train)

    #============== Предсказания ==============#
    
    
    input_data = np.array(shared.data).reshape(1,-1)
    
    data_for_predict = scaler.transform(input_data)
    
    predict = model.predict(data_for_predict)
    
    return predict

print(shared.data)

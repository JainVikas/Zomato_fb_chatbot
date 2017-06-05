'''
Created on Jun 1, 2017

@author: abhinav.jhanwar
'''


from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint

#flower petal
import pandas
from pandas.tools.plotting import scatter_matrix
import numpy as np
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

#for category predict
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import datetime
from astropy.version import debug
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/members/<string:name>/")
def getMember(name):
    return "Hello %s"%name

@app.route("/flowerpetal/")
def flowerpetal():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pandas.read_csv(url, names=names)
    
    array = dataset.values
    X = array[:,0:4]
    Y = array[:,4]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    
    #to predict predic data
    predic = np.array([[5.0, 2.0, 4.0, 1.9]])
    #print(predic,predic.shape)
    
    scoring = 'accuracy'
    
    models = []
    models.append(('LR', LogisticRegression()))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))
    # evaluate each model in turn
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
        
    model = SVC()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))
    print(model.predict(predic))
    
    cs = open("C:/Users/abhinav.jhanwar/Desktop/flowerPetals.csv","w+")
    cs.write("Y_validations,predictions\n")
    for i in range(0,len(predictions)):
        cs.write(Y_validation[i])
        cs.write(",")
        cs.write(predictions[i])
        cs.write("\n")
    cs.close()
    
    return render_template('flowerpetal.html')
 
@app.route("/predict/")
def predict():
    return render_template('categorypredict.html')

@app.route("/categoryprediction/",methods = ['post','get'])
def categorypredict(): 
    
    if request.method == 'POST': 
        file = request.files['Database']
        file.save(secure_filename(file.filename))
        group_field = request.form['Predict']
    
    loc = file.filename#'C:/Users/abhinav.jhanwar/Desktop/NATIONWIDE_IncidentsRawdata.xlsx'
    raw_data = pd.read_excel(loc)
    
    #SubCategory
    sort_field = 'Open Date & Time' #input("Enter field for sorting data: ",)   #Open Date & Time
    sorted_data = raw_data.sort_values([sort_field], ascending=True)
    open_date = sorted_data[sort_field].dropna()
    
    #group_field = 'Category'
    category = sorted_data[group_field].dropna()
    category = category.tolist()

    #print(category)
    
    sample = 'd'
    df = pd.DataFrame({group_field:category}, open_date)
    group = df.groupby(group_field).resample(sample).count()
    df = group.unstack(level=0).dropna()
    df = df[(df.T != 0).any()]
    
    #print(df)
    #plt.plot(df)
    #plt.show()
    
    column_name = df.columns.values.tolist()
    #print(column_name[0])
    Xtrain = []
    Xtest = []
    ytrain = []
    ytest = []
    train = []
    test = []
    
    for i in range(0,len(column_name)):
        Xtrain.append(1)
        Xtest.append(1)
        ytrain.append(1)
        ytest.append(1)
        train.append(1)
        test.append(1)
    
    #print(Xtrain,Xtest,train,test)
    #df.to_csv("C:/Users/abhinav.jhanwar/Desktop/Category_Class.csv")
    
    # evaluate an ARIMA model for a given order (p,d,q) and return RMSE
    def evaluate_arima_model(train, arima_order,test):    
        #prepare training dataset
        #X = X.astype('float32')
        #train_size = int(len(X) * 0.80)
        #train, test = X[0:train_size], X[train_size:]
        #print('train: %d, test: %d' %(len(train),len(test)))
        history = [x for x in train]    
        # make predictions
        predictions = list()    
        for t in range(len(test)):  # test is global variable
            #print("dsf.", len(test)) #53
            model = ARIMA(history, order=arima_order)        
            #model_fit = model.fit(disp=0)
            model_fit = model.fit(trend='nc', disp=0)
            yhat = model_fit.forecast()[0]        
            predictions.append(yhat)        
            history.append(test[t])
        # calculate out of sample error
        mse = mean_squared_error(test, predictions)
        rmse = np.sqrt(mse)
        return rmse
    
    best_cfg = None
    # evaluate combinations of p, d, and q values for an ARIMA model
    def evaluate_model(dataset, p_values, d_values, q_values):
        #dataset = dataset.astype('float32')
        best_score = float("inf") 
        global best_cfg  
        for p in p_values:        
            for d in d_values:            
                for q in q_values:                
                    order = (p,d,q)                
                    try:
                        #print("msewe:")
                        mse = evaluate_arima_model(dataset, order,test[0])                    
                        if mse < best_score:
                            best_score, best_cfg = mse, order
                        print('ARIMA%s, RMSE=%.3f' %(order,mse))
                    except:
                        continue
        print('Best ARIMA%s RMSE=%.3f' %(best_cfg, best_score))            
    
    warnings.filterwarnings("ignore")
    
    
    best_cfg = [(0, 1, 1),(2, 1, 1),(0, 1, 1),(0, 1, 1)]
    
    '''add new data to be predicted'''
    st = datetime.datetime(2017, 12, 1)
    
    for num in range(0,len(column_name)):
        
        df['cat']  = df[column_name[num]]
        
        df_cat = pd.DataFrame({'cat': df['cat']},df.index)
        Xtrain[num], Xtest[num], ytrain[num], ytest[num] = train_test_split(df_cat, df_cat, random_state=0, train_size=0.8)
        Xtest[num].loc[st] = [4]
        ytest[num].loc[st] = [4]
        train[num] = Xtrain[num].values.astype('float32')
        test[num] = ytest[num].values.astype('float32')
    
    #print(Xtest[0],type(Xtest),len(Xtest[0]))
    # evaluate parameters
    #p_values = range(0,3)
    #d_values = range(0,2)
    #q_values = range(0,3)
    #evaluate_model(train[0], p_values, d_values, q_values)
    #Best ARIMA(0, 1, 1) RMSE=4.389 for environment
    #Best ARIMA(2, 1, 1) RMSE=0.168 for hardware
    #Best ARIMA(0, 1, 1) RMSE=0.405 for process
    #Best ARIMA(0, 1, 1) RMSE=25.112 for software
    
    for num in range(0,len(column_name)):
        best_arima_order = best_cfg[num]
        history = [x for x in train[num]]
        predictions = list()
        for i in range(len(test[num])):
            # Predict
            model = ARIMA(history, order=best_arima_order)
            model_fit = model.fit(trend='nc', disp=0)    
            yhat = model_fit.forecast()[0]
            predictions.append(yhat)
            # Observation
            obs = test[num][i]
            history.append(obs) 
        
        # errors
        residuals = [test[num][i] - predictions[i] for i in range(len(test[num]))]
        mean_residual_error = np.mean(residuals) 
        history = [x for x in train[num]]
        predictions = list()
        for i in range(len(test[num])):
            # Predict
            model = ARIMA(history, order=best_arima_order)
            model_fit = model.fit(trend='nc', disp=0)    
            yhat = mean_residual_error + float(model_fit.forecast()[0]) # added bias or error
            predictions.append(yhat)
            obs = test[num][i]
            history.append(obs) 
        mse = mean_squared_error(test[num], predictions)
        rmse = np.sqrt(mse)
        residuals = [test[num][i] - predictions[i] for i in range(len(test[num]))]
        residuals = pd.DataFrame(residuals)
        
        model = ARIMA(train[num], best_arima_order)
        model_fit = model.fit(trend='nc', disp=0)
        bias = mean_residual_error
        yhat = bias + float(model_fit.forecast()[0])
        predictions = list()
        yhat = bias + float(model_fit.forecast()[0])
        predictions.append(yhat)
        history = [x for x in train[num]]
        y = test[num]
        history.append(y[0])
        
        # rolling forecasts
        for i in range(1, len(y)):
            # Predict
            model = ARIMA(history, order=best_arima_order)
            model_fit = model.fit(trend='nc', disp=0)
            yhat = bias + float(model_fit.forecast()[0])
            predictions.append(yhat)
            # Observation
            obs = y[i]
            history.append(obs)
        mse = mean_squared_error(y, predictions)
        
        rmse = np.sqrt(mse)
        
        predictions = [int(round(x)) for x in predictions]
        predictions = np.array(predictions)
        ytest[num]['Predicted ARIMA'] = predictions[:, np.newaxis]
    
    DF_column = {}  #{'Software': ytest[3]['cat'],'Environment':ytest[0]['cat'], 'Hardware':ytest[1]['cat'],'Process':ytest[2]['cat']}
    for i in range(0,len(column_name)):
        DF_column[column_name[i]] = ytest[i]['Predicted ARIMA'] 
    
    df = pd.DataFrame(DF_column,df.index)
    
    df = df.dropna()
    df['Max Category'] = df.idxmax(axis=1)
    df = pd.DataFrame({'Max Category':df['Max Category']},df.index)
    
    #print("Predicted values:",)
    #print(df)
    df.to_csv("C:/Users/abhinav.jhanwar/Desktop/Category_Predict.csv")
    
    return render_template('categorypredicted.html')

@app.route("/hello/<string:user>/")
def hello(user):
#    return name
    return render_template(
        'test.html',**locals()) 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
    
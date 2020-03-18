#Use 10,30,90 day moving averages with Linear Regression to predict the stock market
#Moving averages of the Dow Jones Industrial Average are used to create the data
#Scikit-Learn LinearRegression used to fit the data with MAD and MSE as error statistics

#Import needed libraries 
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

#read in csv and sort by date
df = pd.read_csv(r"/home/dq/scripts/sphist.csv", parse_dates = ["Date"])
df = df.sort_values(axis = 0, by = "Date", ascending = True).reset_index(drop = True)

#create series of moving averages for DJIA value at the market close  (10d, 30d, 90d)
ma_10 = df["Close"].rolling(10).sum().rename( "10dayma")
ma_10 = pd.DataFrame(ma_10)  
ma_10 = ma_10.shift(1)
ma_30 = df["Close"].rolling(30).sum().rename( "30dayma")
ma_30 = pd.DataFrame(ma_30)
ma_30 = ma_30.shift(1)
ma_90 = df["Close"].rolling(90).sum().rename( "90dayma")
ma_90 = pd.DataFrame(ma_90)
ma_90 = ma_90.shift(1)

#create series of moving averages for market volume (5d, 365d)
v_5 = df["Volume"].rolling(3).sum().rename( "5dayavgvol")
v_5 = pd.DataFrame(v_5)
v_5 = v_5.shift(1)
v_365 = df["Volume"].rolling(365).sum().rename( "365dayavgvol")
v_365 = pd.DataFrame(v_365)
v_365 = v_365.shift(1)

#concantenate market close series onto main df and separately concantenate volume onto main df
df_ma = pd.concat([df,ma_10,ma_30,ma_90], axis = 1)
df_ma_v = pd.concat([df_ma, v_5, v_365], axis =1)

#remove pre 1951 data
df_clean_ma= df_ma[df_ma["Date"] > datetime(year = 1951, month = 1, day= 2)].dropna(axis = 0)
df_clean_ma_v= df_ma_v[df_ma_v["Date"] > datetime(year = 1951, month = 1, day= 2)].dropna(axis = 0)

#split the df's into train/test sets
df_train_ma = df_clean_ma[df_clean_ma["Date"] < datetime(year = 2013, month = 1, day= 1)]
df_test_ma = df_clean_ma[df_clean_ma["Date"] >= datetime(year = 2013, month = 1, day= 1)]
df_train_ma_v = df_clean_ma_v[df_clean_ma_v["Date"] < datetime(year = 2013, month = 1, day= 1)]
df_test_ma_v = df_clean_ma_v[df_clean_ma_v["Date"] >= datetime(year = 2013, month = 1, day= 1)]

#fit LinearRegression on both df's and get error statistics
lr = LinearRegression()
lr.fit(df_train_ma[['10dayma', '30dayma', '90dayma']], df_train_ma["Close"])
test_predictions_ma = lr.predict(df_test_ma[['10dayma', '30dayma', '90dayma']])
mae_ma = mean_absolute_error(df_test_ma["Close"], test_predictions_ma)
mse_ma = mean_squared_error(df_test_ma["Close"], test_predictions_ma)

lr.fit(df_train_ma_v[['10dayma', '30dayma', '90dayma', "5dayavgvol", "365dayavgvol"]], df_train_ma_v["Close"])
test_predictions_ma_v = lr.predict(df_test_ma_v[['10dayma', '30dayma', '90dayma', "5dayavgvol", "365dayavgvol"]])
mae_ma_v = mean_absolute_error(df_test_ma_v["Close"], test_predictions_ma_v)
mse_ma_v = mean_squared_error(df_test_ma_v["Close"], test_predictions_ma_v)

#print error statistics
mae_dict = {"3 ma model": mae_ma}
mse_dict = {"3 ma model": mse_ma}

mae_dict["3ma 2v model"] = mae_ma_v
mse_dict["3ma 2v model"] = mse_ma_v

print("mae:",mae_dict)
print("mse:", mse_dict)


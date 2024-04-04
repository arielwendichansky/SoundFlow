import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

class pregame():
   
    def __init__(self, df):
        self.df = df
    def checks(self):
        # descriptives
        print("INFO: ")
        print(self.df.info())
        print("DESCRIPTION: ")
        print(self.df.describe())
        #check for null values
        print("NULL VALUE COUNT: ")
        print(self.df.isnull().sum())
        #check for duplicates
        dups = self.df.duplicated().sum()
        print("DUPLICATE COUNT: ", dups)
        if dups != 0:
            self.df = self.df.drop_duplicates() 
            print("duplicates dropped")
        else:
            pass



    def foreplay(self, column_name, fill_strategy): #call function for every column
        #fill missing values with specified strategy
        #fill_strategy = fill_strategy.lower()
        if fill_strategy == "mean":  
            self.df[column_name].fillna(self.df[column_name].mean(), inplace = True)
        elif fill_strategy == "median":  
            self.df[column_name].fillna(self.df[column_name].median(), inplace = True)
        elif fill_strategy == "mode":  
            self.df[column_name].fillna(self.df[column_name].mode(), inplace = True)
        elif fill_strategy == "0":
            self.df[column_name].fillna(0, inplace = True)
        else:
            try: 
                self.df[column_name].fillna(fill_strategy, inplace = True)
            except: 
                print("not a valid fill strategy. Choose mean, median, 0, or a string")
        
        return self.df
   
    def micdrop(self, what_to_drop, column_list): #dropping duplicates, entire columns or nulls
        if what_to_drop == "columns":
            for column in column_list:
            #drop name columns with not value
                self.df.drop(column, axis = 1, inplace = True)
        elif what_to_drop == "na":
            self.df.dropna(subset=column_list, inplace = True)
        else:
            print("not valid dropping option. Choose to drop duplicates, columns or na")

        return self.df
    
    def remove_outliers(self, col_name, lower_bound, upper_bound):
        self.df = self.df[(self.df[col_name] >= lower_bound) & (self.df[col_name] <= upper_bound)]
        return self.df

    def check_outliers(self):
        column_list = self.df.select_dtypes(include =['number', 'float', 'integer'])
        print("numeric columns: ", column_list)
        for col_name in column_list:
            Q1 = self.df[col_name].quantile(0.25)
            Q3 = self.df[col_name].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.remove_outliers(col_name, lower_bound, upper_bound)
        return self.df

    
    def binary_exchange(self, string1, string2):
        column_list = [col for col in self.df.columns if self.df[col].nunique() == 2]
        for column in column_list:
            self.df[column].replace({string1: 1, string2: 0}, inplace = True)
        return self.df
    
    def ordinal_exchange(self, column_list):
        for column in column_list:
            unique_values = self.df[column].unique()
            unique_list = list(unique_values)
            encoder = OrdinalEncoder(categories=[unique_list])
            encoded_data = encoder.fit_transform(self.df[[column]])
            self.df[column] = encoded_data
        return self.df

    def smartie(self):
        nominal_column_list = [col for col in self.df.columns if 'Yes' in self.df[col].values]
        self.df = pd.get_dummies(self.df, columns=nominal_column_list)

        return self.df

    def toScaleOrNotToScale(self, scale_strategy, column_name):
        if scale_strategy == "standard":
            scaler = StandardScaler()
            # Fit the scaler to the data and transform it
            scaled_data = scaler.fit_transform(self.df)

            # Convert the scaled data back to a DataFrame
            scaled_df = pd.DataFrame(scaled_data, columns=self.df.columns)
        elif scale_strategy == "minmax":
            scaler = MinMaxScaler()
            self.df[column_name + "scaled"] = scaler.fit_transform(self.df[[column_name]])

        
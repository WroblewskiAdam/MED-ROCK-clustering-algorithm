import csv
from scipy.io import arff
import pandas as pd

class Data_Converter:
    def convert_data_types(self, df):
        # konwersja typu danych klasy
        df_mod = df.select_dtypes([object]).stack().str.decode('utf-8').unstack()
        df["class"] = df_mod["class"]
        
        # konwersja danych do int
        df = df.astype(int)
        return df

    def split_multi_arg_attribute(self, df , column_name, attributes_list, bin_data = False):
        column = df[column_name]
        column_index = df.columns.tolist().index(column_name)
        df = df.drop(columns = [column_name])
        
        if bin_data:
            values = []
            for point in column:
                values.append(1) if point == attributes_list[0] else values.append(0)
            df.insert(column_index, str(column_name), values)

        else:
            for i in range(len(attributes_list)):
                values = []
                attribute_value = attributes_list[i]
                for point in column:
                    values.append(1) if point == attribute_value else values.append(0)
                df.insert(column_index + i, str(column_name) + str(attribute_value), values)
        
        return df
   
    def separate_class_from_data(self, arr_data, class_index):
        for i in range(len(arr_data)):
            point_class = arr_data[i][class_index]
            arr_data[i].pop(class_index)
            arr_data[i] = [arr_data[i], point_class]
        return arr_data

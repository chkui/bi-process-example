# -- coding: utf-8 --

import datetime
import os
import pandas as pd
from pandas import DataFrame
import sqlalchemy

dt = datetime.datetime
print('Begin time: ')
print(dt.now())

# 从NOAA的csv文件中夹在数据
# pandas提供从各种文件抽取数据的功能
print('Read The Data From ${project}/data/2015.csv')
projectRootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
weatherDataPath = projectRootPath + "/data/2015.csv"
stationsPath = projectRootPath + "/data/ghcnd-stations.txt"

print 'Begin load weather data from ' + weatherDataPath
print(dt.now())
weather_data = pd.read_csv(weatherDataPath,
                           header=None, index_col=False,
                           names=['station_identifier',
                                  'measurement_date',
                                  'measurement_type',
                                  'measurement_flag',
                                  'quality_flag',
                                  'source_flag',
                                  'observation_time'],
                           parse_dates=['measurement_date'])

print('Load weather_data: ')
print(dt.now())
print(weather_data)

'''
对数据进行初步过滤清洗。取得原始数据的子集
1.仅仅需要以下类型的数据：
    PRCP：Precipitation，降水（mm）。 
    SNOW：Snowfall，降雪（mm）。
    SNWD：Snow depth，大雪（mm）。
    TMAX：Maximum temperature，最高温度（C）。 
    TWIN：Minimum temperature，最低温度（C）。
2.仅仅需要'station_identifier', 'measurement_date', 'measurement_type', 'measurement_flag'字段。
'''
weather_data_subset = weather_data[weather_data.measurement_type.isin(['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TWIN'])][
    ['station_identifier', 'measurement_date', 'measurement_type', 'measurement_flag']]
# print(weather_data_subset)

print('Subset length: ')
__len = weather_data_subset.__len__()
print(__len)

'''
下面将数据遍历入库。
原文没有使用遍历，而是一次性使用to_sql入库近2000万条数据。执行时会卡死。使用分批方式入库
'''
chunkSize = 2000000 #to_sql方法的分块大小
start = 0 #遍历的开始位置
end = 0 #遍历的结束位置
execute = True #执行标记

'''
以下为数据库连接串，sqlAlchemy
'''
db_name = 'postgres'
connection_string = "postgresql://postgres:123456@localhost:5432/postgres"
conn = sqlalchemy.create_engine(connection_string) #conn是连接实例
print conn
table_name = 'weather_data'
column_type_dict = {'measurement_flag': sqlalchemy.types.Integer}


while (execute):
    end = start + chunkSize
    if end > __len:
        end = __len
        execute = False
    truncateSet = weather_data_subset.truncate(start, end)
    print('TruncateSet :')
    print(truncateSet)
    truncateSet.to_sql(table_name, conn,
                       chunksize=chunkSize + 1,
                       index_label='id',
                       dtype=column_type_dict,
                       if_exists='replace' if 0 == start else 'append')
    start = end


print 'Stations Ghcnd Data Path: ' + weatherDataPath
#读取标记的元数据
station_metadata = pd.read_csv(stationsPath, sep='\s+', usecols=[0, 1, 2, 3], na_values=[-999.9],
                               header=None, names=['station_id', 'latitude', 'longitude', 'elevation'])
station_metadata.head()
print(station_metadata)
print(len(station_metadata[station_metadata['elevation'].isnull()]))

metadata_table_name = 'station_metadata'
station_metadata.to_sql(metadata_table_name, conn, index_label='id')

weather_type_dict = {'PRCP': 'Precipitation', 'SNOW': 'Snowfall', 'SNWD': 'Snow Depth',
                     'TMAX': 'Maximum temperature', 'TMIN': 'Minimum temperature'}
weather_type_df = DataFrame(weather_type_dict.items(), columns=['weather_type', 'weather_description'])
description_table_name = 'weather_types'
weather_type_df.to_sql(description_table_name, conn, index_label='id')#元数据入库

print('EXIT')
print('End time: ')
print(dt.now())

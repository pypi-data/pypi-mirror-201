# import libraries
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
import urllib3
import pyarrow as pa
import pyarrow.parquet as pq

pd.options.mode.chained_assignment = None
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DataAccess:

    def __init__(self, userID, url,cache_path):
        self.userID = userID
        self.url = url
        self.cache_path = cache_path

    def check_data_incache(self, device_id, sensors, start_time, end_time):
        before_date_in_cache = []
        after_date_in_cache = []

        msg = ''
        date_list = []
        str_dates = []
        incache = []
        nocache = []

        # Sort dates based on year
        def sort_dates(dates):
            def date_key(date_string):
                return datetime.strptime(date_string, '%Y-%m-%d')
            return sorted(dates, key=date_key)

        # Extract date from datetime
        match_start_str = re.search(r'\d{4}-\d{2}-\d{2}', start_time)
        match_end_str = re.search(r'\d{4}-\d{2}-\d{2}', end_time)

        startT = (datetime.strptime(match_start_str.group(), '%Y-%m-%d').date())
        endT = (datetime.strptime(match_end_str.group(), '%Y-%m-%d').date())
        curr_date = startT

        while curr_date <= endT:
            date_list.append(curr_date)
            curr_date += timedelta(days=1)
        for i_s in date_list:
            i_s = str(i_s)
            str_dates.append(i_s)


        # Check if data exists in path
        for j in sensors:
            for i in str_dates:
                try:
                    path = self.cache_path + device_id + "/sensor=" + j + "/Date=" + i + "/"
                    dir = os.listdir(path)
                    isExist = os.path.isdir(path)
                    if isExist:
                        incache.append(i)
                except OSError as e:
                    nocache.append(i)

        incache = [*set(incache)]
        nocache = [*set(nocache)]
        sorted_dates = sort_dates(nocache)
        incache = sort_dates(incache)

        for val in sorted_dates:
            for val1 in incache:
                if val < val1:
                    before_date_in_cache.append(val)
                if val > val1:
                    after_date_in_cache.append(val)

        before_date_in_cache = [*set(before_date_in_cache)]
        before_date_in_cache = sort_dates(before_date_in_cache)
        after_date_in_cache = [*set(after_date_in_cache)]
        after_date_in_cache = sort_dates(after_date_in_cache)

        if len(incache) != 0:
            msg = 'yes'
        else:
            msg = 'no'

        return msg, incache, nocache, sensors

    def get_data_from_cache(self, incache, sensor_list, device_id):
        df_new = pd.DataFrame(columns=["time", "del", "value", "sensor"])
        for i in range(len(incache)):
            sys.stdout.write('\r')
            sys.stdout.write("Please Wait ...")
            sys.stdout.flush()

        for k in sensor_list:
            for l in incache:
                try:
                    path = self.cache_path + device_id + "/sensor=" + k + "/Date=" + l + "/"
                    df = pd.read_parquet(path)
                    df['sensor'] = k
                    df_new = pd.concat([df_new, df])
                except OSError as e:
                    pass
        return df_new

    def store_data_incache(self, device_id, df, sensors):

        if len(df.columns) == 2:
            df['sensor'] = sensors[0]
        path = self.cache_path
        dir = os.listdir(path)

        df['Date'] = pd.to_datetime(df['time']).dt.date

        if len(dir) == 0:
            table = pa.Table.from_pandas(df)
            pq.write_to_dataset(
                table,
                root_path=path + device_id + '/',
                partition_cols=['sensor', 'Date'])
        else:
            table = pa.Table.from_pandas(df)
            pq.write_to_dataset(
                table,
                root_path=path + device_id + '/',
                partition_cols=['sensor', 'Date'])

    def get_device_metadata(self, device_id):
        """

        :param device_id: string
        :return: Json

         Every detail related to a particular device like device added date, m,c,min,max values, sensor id, sensor alias and so on

        """
        try:
            url = "https://" + self.url + "/api/metaData/device/" + device_id
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)
            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch device Metadata')
            print(e)

    def get_sensor_alias(self, device_id, df,raw_metadata):
        """

        :param raw_metadata: json of device metadata
        :param device_id: string
        :param df: Dataframe
        :return: dataframe with columns having sensor alias

        Maps sensor_alias/ sensor name with corresponding sensor ID
        replaces column names with sensor_alias_sensor_id

        """

        list1 = list(df['sensor'].unique())
        if len(raw_metadata) == 0:
            raw_metadata = DataAccess.get_device_metadata(self, device_id)
        sensor_spec = 'sensors'

        sensor_param_df = pd.DataFrame(raw_metadata[sensor_spec])

        for i in list1:
            sensor_param_df1 = sensor_param_df[sensor_param_df['sensorId'] == i]
            if len(sensor_param_df1) != 0:
                # print('sensor_param_df',sensor_param_df1)
                sensor_name = sensor_param_df1.iloc[0]['sensorName']
                sensor_name = sensor_name + " (" + i + ")"
                df['sensor'] = df['sensor'].replace(i, sensor_name)
        return df,raw_metadata

    def get_caliberation(self,device_id,metadata,df):
        """

        :param df_raw: Dataframe
        :param device_id: string
        :return: Calibrated dataframe

        Perform cal on original data
             y = mx + c
             if y is greater than max value replace y with max value
             if y is less than min value replace y with min value

        """
        sensor_name_list = list(df.columns)
        sensor_name_list.remove('time')
        # print(sensor_name_list)
        sensor_id_list = [s[s.rfind("(") + 1:s.rfind(")")] for s in sensor_name_list]
        if len(metadata) == 0:
            metadata = DataAccess.get_device_metadata(self,device_id)
        data = metadata['params']

        for (value1, value2) in zip(sensor_id_list, sensor_name_list):
            # print(value1, value2)
            # print(data[str(value1)])
            df_meta = pd.DataFrame(data[str(value1)])
            # print(df_meta)
            df_meta = df_meta.set_index('paramName').transpose()
            if 'm' in df_meta.columns and 'c' in df_meta.columns:
                # print(df_meta.iloc[0]['m'],type(df_meta.iloc[0]['m']))
                m = float(df_meta.iloc[0]['m'])
                c = int(df_meta.iloc[0]['c'])
                # print(m, type(c))
                # print(df[str(value2)])
                df[str(value2)] =  df[str(value2)].replace('BAD 255', '-99999').replace('-','99999').replace('BAD undefined', '-99999').replace('BAD 0', '-99999')
                df[str(value2)] = df[str(value2)].astype('float')
                # print('==',df[str(value2)])
                df[str(value2)] = (df[str(value2)] * m) + c
                if 'min' in df_meta.columns:
                    min = int(df_meta.iloc[0]['min'])
                    df[str(value2)] = np.where(df[str(value2)] <= min, min, df[str(value2)])
                if 'max' in df_meta.columns:
                    max = int(str(df_meta.iloc[0]['max']).replace('-', '99999').replace(
                        '1000000000000000000000000000', '99999').replace('100000000000', '99999'))
                    df[str(value2)] = np.where(df[str(value2)] >= max, max, df[str(value2)])
        return df

    def time_grouping(self, df, bands):
        """

        :param df: DataFrame
        :param bands: 05,1W,1D
        :return: Dataframe

        Group time series DataFrame
        Example: The values in Dataframe are at 30s interval we can group and change the 30s interval to 5 mins, 10 mins, 1 day or 1 week.
        The resultant dataframe contains values at given interval.
        """

        df['Time'] = pd.to_datetime(df['time'])
        df.sort_values("Time", inplace=True)
        df = df.drop(['time'], axis=1)
        df = df.set_index(['Time'])
        df.index = pd.to_datetime(df.index)
        df = df.groupby(pd.Grouper(freq=str(bands) + "Min", label='right')).mean()
        df.reset_index(drop=False, inplace=True)
        return df

    def get_cleaned_table(self, df):
        """

        :param df: Raw Dataframe
        :return: Pivoted DataFrame

        The raw dataframe has columns like time, sensor, values.
        The resultant dataframe will be time sensor alias - sensor id along with their corresponding values

        """

        df = df.sort_values('time')
        df.reset_index(drop=True, inplace=True)
        results = df.pivot(index='time', columns='sensor', values='value')
        results.reset_index(drop=False, inplace=True)
        return results

    def get_device_details(self):
        """

        :return: Details Device id and Device Name of a particular account

        Dataframe with list of device ids and device names.

        """
        try:
            url = "https://" + self.url + "/api/metaData/allDevices"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                df_raw = pd.DataFrame(raw_data)
                return df_raw

        except Exception as e:
            print('Failed to fetch device Details')
            print(e)

    def get_userinfo(self):
        """
        :return: Json

        Details like phone,name,gender,emailed etc are fetched
        """
        try:
            url = "https://" + self.url + "/api/metaData/user"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch user Information')
            print(e)

    def get_dp(self, device_id, sensors, n=1, cal=True, end_time=datetime.now(), IST=True):
        """

        :param device_id: string
        :param sensors: list of sensors
        :param n: number of data points (default: 1)
        :param cal: bool (default: True)
        :param end_time: 'YYYY:MM:DD HH:MM:SS'
        :param IST: bool (default: True)
        :return: Dataframe with values

        Get Data Point fetches data containing values of last n data points of given sensor at given time.

        """
        try:
            metadata = {}
            end_time = pd.to_datetime(end_time)
            if IST:
                end_time = end_time - timedelta(hours=5, minutes=30)
            end_time = int(round(end_time.timestamp()))
            if type(sensors) == list:
                len_sensors = len(sensors)
                if len_sensors == 0:
                    raise Exception('Message: No sensors provided')
                if n < 1:
                    raise ValueError('Incorrect number of data points')
                n = int(n) * len_sensors
                delimiter = ","
                sensor_values = delimiter.join(sensors)
            else:
                raise Exception('Message: Incorrect type of sensors')
            header = {}
            cursor = {'end': end_time, 'limit': n}
            payload = {}
            df = pd.DataFrame()
            counter = 0
            while True:
                for record in range(counter):
                    sys.stdout.write('\r')
                    sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                    sys.stdout.flush()
                url = "https://" + self.url + "/api/apiLayer/getLimitedDataMultipleSensors/?device=" + device_id + "&sensor=" + sensor_values + "&eTime=" + str(
                    cursor['end']) + "&lim=" + str(cursor['limit']) + "&cursor=true"
                response = requests.request("GET", url, headers=header, data=payload)
                raw = json.loads(response.text)
                if response.status_code != 200:
                    raise ValueError(response.status_code)
                if 'success' in raw:
                    raise ValueError(raw)
                else:
                    raw_data = json.loads(response.text)['data']
                    cursor = json.loads(response.text)['cursor']
                    if len(raw_data) != 0:
                        df = pd.concat([df, pd.DataFrame(raw_data)])
                    counter = counter + 1
                if cursor['end'] == None:
                    break
            if len(df) == 0:
                raise ValueError('No Data')
            if IST:
                df['time'] = pd.to_datetime(df['time'], utc=False)
                df['time'] = df['time'].dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
            df, metadata = DataAccess.get_sensor_alias(self, device_id, df, metadata)
            df = DataAccess.get_cleaned_table(self, df)
            if str(cal).lower() == 'true':
                df = DataAccess.get_caliberation(self, device_id, metadata, df)
            return df
        except Exception as e:
            print(e)

    def fetch_data(self,device_id, start_time, end_time=datetime.now(), sensors=None, cal=True, bands=None, IST=True ,echo=True):
        metadata = {}
        rawdata_res = []
        temp = ''
        s_time = pd.to_datetime(start_time)
        e_time = pd.to_datetime(end_time)
        if IST:
            s_time = s_time - timedelta(hours=5, minutes=30)
            e_time = e_time - timedelta(hours=5, minutes=30)
        st_time = int(round(s_time.timestamp())) * 10000
        en_time = int(round(e_time.timestamp())) * 10000
        header = {}
        payload = {}
        counter = 0
        cursor = {'start': st_time, 'end': en_time}
        while True:
            if echo:
                for record in range(counter):
                    sys.stdout.write('\r')
                    sys.stdout.write("Approx Records Fetched %d" % (10000 * record))
                    sys.stdout.flush()
            if sensors is None:
                url_api = "https://" + self.url + "/api/apiLayer/getDataByStEt?device="
                if counter == 0:
                    temp = url_api + device_id + "&sTime=" + str(st_time) + "&eTime=" + str(
                        en_time) + "&cursor=true&limit=50000"
                else:
                    temp = url_api + device_id + "&sTime=" + str(cursor['start']) + "&eTime=" + str(
                        cursor['end']) + "&cursor=true&limit=50000"
            if sensors is not None:
                url_api = "https://" + self.url + "/api/apiLayer/getAllData?device="
                if counter == 0:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(
                        st_time) + "&eTime=" + str(
                        en_time) + "&cursor=true&limit=50000"
                else:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(
                        cursor['start']) + "&eTime=" + str(cursor['end']) + "&cursor=true&limit=50000"

            response = requests.request("GET", temp, headers=header, data=payload)
            raw = json.loads(response.text)
            # print(raw)
            if response.status_code != 200:
                raise ValueError(raw)
            if 'success' in raw:
                raise ValueError(raw)

            else:
                raw_data = json.loads(response.text)['data']
                # print('====================',raw_data)
                cursor = json.loads(response.text)['cursor']
                if len(raw_data) != 0:
                    rawdata_res = rawdata_res + raw_data
                counter = counter + 1
            if cursor['start'] is None or cursor['end'] is None:
                break
        # print(rawdata_res)
        df_raw = pd.DataFrame(rawdata_res)
        return df_raw

    def data_query(self, device_id, start_time, end_time=datetime.now(), sensors=None, cal=True, bands=None, IST=True ,echo=True):
        metadata = {}
        df_raw = pd.DataFrame()
        if sensors == None:
            metadata = DataAccess.get_device_metadata(self, device_id)
            data_sensor = metadata['sensors']
            df_sensor = pd.DataFrame(data_sensor)
            sensor_id_list = list(df_sensor['sensorId'])
            sensors = sensor_id_list
        msg, incache, nocache, sensors_list = DataAccess.check_data_incache(self, device_id, sensors, start_time, end_time)
        if len(nocache) == 0 and msg == 'yes':
            df_raw = DataAccess.get_data_from_cache(self, incache, sensors_list, device_id)
            df_raw.reset_index(drop=True, inplace=True)
            df_raw.sort_values("time", inplace=True)
            df_raw.reset_index(drop=True, inplace=True)

        if len(incache) == 0 and msg != 'yes' and len(nocache) != 0:
            df_raw = DataAccess.fetch_data(self,device_id, start_time, end_time, sensors, cal=True, bands=None, IST=True ,echo=True)
            if len(df_raw) != 0:
                DataAccess.store_data_incache(self, device_id, df_raw, sensors)

        if len(incache) !=0 and len(nocache) !=0 and msg == 'yes':
            if len(incache) == 1 and len(nocache) ==1:
                if incache[0] != nocache[0]:
                    if min(nocache) == max(nocache):
                        start_time = str(min(nocache)) + " 00:00:00"
                        end_time = str(min(nocache)) + " 23:59:00"
                    else:
                        start_time = str(min(nocache))
                        end_time = str(max(nocache))
                    df_raw2 = DataAccess.fetch_data(self, device_id, start_time, end_time, sensors_list, cal=True,bands=None, IST=True, echo=True)
                    if len(df_raw2) != 0:
                        DataAccess.store_data_incache(self, device_id, df_raw2, sensors)
                    df_raw1 = DataAccess.get_data_from_cache(self, incache, sensors_list, device_id)
                    df_raw = pd.concat([df_raw1,df_raw2])
                else:
                    df_raw = DataAccess.fetch_data(self, device_id, start_time, end_time, sensors_list, cal=True,bands=None, IST=True, echo=True)
            else:
                if min(nocache) == max(nocache):
                    start_time = str(min(nocache)) + " 00:00:00"
                    end_time = str(min(nocache)) + " 23:59:00"
                else:
                    start_time = str(min(nocache))
                    end_time = str(max(nocache))
                df_raw2 = DataAccess.fetch_data(self, device_id, start_time, end_time, sensors_list, cal=True,bands=None, IST=True, echo=True)
                if len(df_raw2) != 0:
                    DataAccess.store_data_incache(self, device_id, df_raw2, sensors)
                df_raw1 = DataAccess.get_data_from_cache(self, incache, sensors_list, device_id)
                df_raw = pd.concat([df_raw1, df_raw2])
        # print(df_raw)
        if len(df_raw) != 0:
            if IST:
                df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
                df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)
            if len(df_raw.columns) == 2:
                df_raw['sensor'] = sensors[0]
                # #qq=qq[~qq['value'].isin(['','BAD 255','BAD 0','BAD undefined','-'])]
            df_raw, metadata = DataAccess.get_sensor_alias(self, device_id, df_raw, metadata)
            df_raw = DataAccess.get_cleaned_table(self, df_raw)

            if cal or cal == 'true' or cal == "TRUE":
                df_raw = DataAccess.get_caliberation(self, device_id, metadata, df_raw)
            if bands is not None:
                df_raw = DataAccess.time_grouping(self, df_raw, bands)
        return df_raw

    def publish_event(self, title, message, meta_data, hover_data, event_tags, created_on):
        """

        :param title: string
        :param message: string
        :param meta_data: string
        :param hover_data: string
        :param event_tags: string
        :param created_on: date string
        :return: json

        Fetches Data of published events based on input parameters

        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/publishEvent"
            header = {'userID': self.userID}
            payload = {
                "title": title,
                "message": message,
                "metaData": meta_data,
                "eventTags": [event_tags],
                "hoverData": "",
                "createdOn": created_on
            }
            response = requests.request('POST', url, headers=header, json=payload, verify=True)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Details')
            print(e)
        return raw_data

    def get_events_in_timeslot(self, start_time, end_time):
        """

        :param start_time: date string
        :param end_time: date string
        :return: Json

        Fetches events data in given timeslot

        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/fetchEvents/timeslot"
            header = {'userID': self.userID}
            payload = {
                "startTime": start_time,
                "endTime": end_time
            }
            response = requests.request('PUT', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Details')
            print(e)

        return raw_data

    def get_event_data_count(self, end_time=time.time(), count=None):
        """

        :param end_time: date string
        :param count: integer
        :return: Json
        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag/fetchEvents/count"
            header = {'userID': self.userID}
            payload = {
                "endTime": end_time,
                "count": count
            }
            response = requests.request('PUT', url, headers=header, json=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)
                return raw_data

        except Exception as e:
            print('Failed to fetch event Count')
            print(e)

        return raw_data

    def get_event_categories(self):
        """

        :return: Event Categories Details
        """
        raw_data = []
        try:
            url = "https://" + self.url + "/api/eventTag"
            header = {'userID': self.userID}
            payload = {}
            response = requests.request('GET', url, headers=header, data=payload, verify=False)

            if response.status_code != 200:
                raw = json.loads(response.text)
                raise ValueError(raw['error'])
            else:
                raw_data = json.loads(response.text)['data']
                return raw_data

        except Exception as e:
            print('Failed to fetch event Count')
            print(e)

        return raw_data


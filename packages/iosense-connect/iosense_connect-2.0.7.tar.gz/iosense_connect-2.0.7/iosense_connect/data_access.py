# import libraries
import json
import sys
import time
from datetime import datetime,timedelta

import numpy as np
import pandas as pd
import requests
import urllib3

pd.options.mode.chained_assignment = None
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DataAccess:

    def __init__(self, userID, url):
        self.userID = userID
        self.url = url

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
            # print(response.text)
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

    def get_dp(self, device_id, sensors=['D29'], n=1, cal=True, end_time=datetime.now(),IST=True):
        """

        :param device_id: string
        :param sensors: list of sensors. Sensors is not None
        :param n: number of data points
        :param cal: True/False
        :param end_time: 'year-month-day hours:minutes:seconds'
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
                    raise ValueError(raw)
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
            if len(df) != 0:
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

    def data_query(self, device_id, start_time, end_time=datetime.now(), sensors=None, cal=True, bands=None, IST=True ,echo=True):
        # df = pd.DataFrame()
        metadata = {}
        if sensors == None:
            metadata = DataAccess.get_device_metadata(self, device_id)
            data_sensor = metadata['sensors']
            df_sensor = pd.DataFrame(data_sensor)
            sensor_id_list = list(df_sensor['sensorId'])
            sensors = sensor_id_list
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
                    temp = url_api + device_id + "&sTime=" + str(st_time) + "&eTime=" + str(en_time) + "&cursor=true&limit=50000"
                else:
                    temp = url_api + device_id + "&sTime=" + str(cursor['start']) + "&eTime=" + str(
                        cursor['end']) + "&cursor=true&limit=50000"
            if sensors is not None:
                url_api = "https://" + self.url + "/api/apiLayer/getAllData?device="
                if counter == 0:
                    str1 = ","
                    sensor_values = str1.join(sensors)
                    temp = url_api + device_id + "&sensor=" + sensor_values + "&sTime=" + str(st_time) + "&eTime=" + str(
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
                if len(raw_data) !=0:
                    rawdata_res = rawdata_res + raw_data
                counter = counter + 1
            if cursor['start'] is None or cursor['end'] is None:
                break
        # print(rawdata_res)
        df_raw = pd.DataFrame(rawdata_res)

        if len(df_raw) != 0 :
            if IST:
                df_raw['time'] = pd.to_datetime(df_raw['time'], utc=False)
                df_raw['time'] = df_raw['time'].dt.tz_convert('Asia/Kolkata').dt.tz_localize(None)

            if len(df_raw.columns) == 2:
                df_raw['sensor'] = sensors[0]

            df, metadata = DataAccess.get_sensor_alias(self, device_id, df_raw, metadata)
            df = DataAccess.get_cleaned_table(self, df)

            if cal or cal == 'true' or cal == "TRUE":
                # #qq=qq[~qq['value'].isin(['','BAD 255','BAD 0','BAD undefined','-'])]
                df = DataAccess.get_caliberation(self, device_id, metadata, df)

            if bands is not None:
                df = DataAccess.time_grouping(self, df, bands)
        else:
            df = df_raw
        return df

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


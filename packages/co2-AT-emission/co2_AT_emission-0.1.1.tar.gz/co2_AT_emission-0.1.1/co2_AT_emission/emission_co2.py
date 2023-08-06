import pandas as pd
import datetime as dtime
import pytz
import re
from eco2ai import set_params, Tracker

default_timezone = pytz.timezone("Europe/Berlin")


class Co2Emission:

    def __init__(self, output_path: str, output_file: str, output_format: str, project_name: str,
                 experiment_description=None):
        """
        default path to the output file Emission.csv
        :param output_path: path to the output file that contains emission information
        :param output_file: by default its Emission
        :param output_format: .csv
        :param project_name: project name
        :param experiment_description: optional
        """
        self.output_path = output_path
        self.output_file = output_file
        self.output_format = output_format
        self.project_name = project_name
        self.experiment_description = experiment_description

        set_params(
            project_name= project_name,
            experiment_description=experiment_description,
            file_name= output_file + ".csv"
        )

    @staticmethod
    def tracker_initialize():
        """
        Initializes the tracker from eco2ai library
        :return: returns tracker instance
        """
        tracker = Tracker()
        return tracker

    @staticmethod
    def extract_date_time(col):
        """
        Extracts the date and time from the timestamp column
        :param col: Timestamp column
        :return: returns dd-mm-yyyy HH:MM:SS format
        """
        regex2 = r'^[^.]+'
        text = str(col)
        result = re.search(regex2, text)
        if result:
            return pd.to_timedelta(result.group(0))
        else:
            return pd.Timedelta(0)

    def emission_hourly(self, flag_duration: int):
        """
        Computes the total carbon emission, power consumption and duration as per the flag_duration parameter

        :param flag_duration: total hours to be considered
        :return: Dataframe with carbon emission, power consumption and duration
        """
        df = pd.read_csv(self.output_path + self.output_file + self.output_format)

        df['start_time'] = pd.to_datetime(df['start_time'])
        df['time_diff'] = dtime.datetime.now() - df['start_time']

        df["time_diff"] = df["time_diff"].apply(Co2Emission.extract_date_time)
        df_hourly = df.loc[df['time_diff'] <= dtime.timedelta(hours=flag_duration)]

        duration_sum = df_hourly["duration(s)"].sum()
        power_sum = df_hourly['power_consumption(kWh)'].sum()
        co2_sum = df_hourly["CO2_emissions(kg)"].sum()

        df_dict = dict()
        df_dict["Duration"] = duration_sum
        df_dict["Power"] = power_sum
        df_dict["Co2_Emission"] = co2_sum

        df_hourly_emission = pd.DataFrame(df_dict,  index=[0])

        return df_hourly_emission

    def emission_daily(self, flag_duration: int):
        """
        Computes the total carbon emission, power consumption and duration as per the flag_duration parameter

        :param flag_duration: total days to be considered
        :return: Dataframe with carbon emission, power consumption and duration
        """

        df = pd.read_csv(self.output_path + self.output_file + self.output_format)

        df['start_time'] = pd.to_datetime(df['start_time'])
        df['time_diff'] = dtime.datetime.now() - df['start_time']
        df["time_diff"] = df["time_diff"].apply(Co2Emission.extract_date_time)
        df_daily = df.loc[df['time_diff'] <= dtime.timedelta(days=flag_duration)]

        duration_sum = df_daily["duration(s)"].sum()
        power_sum = df_daily["power_consumption(kWh)"].sum()
        co2_sum = df_daily["CO2_emissions(kg)"].sum()

        df_dict = dict()
        df_dict["Duration"] = duration_sum
        df_dict["Power"] = power_sum
        df_dict["Co2_Emission"] = co2_sum

        df_daily_emission = pd.DataFrame(df_dict, index=[0])

        return df_daily_emission

    def emission_weekly(self, flag_duration: int):
        """
        Computes the total carbon emission, power consumption and duration as per the flag_duration parameter

        :param flag_duration: total weeks to be considered
        :return: Dataframe with carbon emission, power consumption and duration
        """

        df = pd.read_csv(self.output_path + self.output_file + self.output_format)

        df['start_time'] = pd.to_datetime(df['start_time'])
        df['time_diff'] = dtime.datetime.now() - df['start_time']
        df["time_diff"] = df["time_diff"].apply(Co2Emission.extract_date_time)
        df_weekly = df.loc[df['time_diff'] <= dtime.timedelta(weeks=flag_duration)]

        duration_sum = df_weekly["duration(s)"].sum()
        power_sum = df_weekly["power_consumption(kWh)"].sum()
        co2_sum = df_weekly["CO2_emissions(kg)"].sum()

        df_dict = dict()
        df_dict["Duration"] = duration_sum
        df_dict["Power"] = power_sum
        df_dict["Co2_Emission"] = co2_sum

        df_weekly_emission = pd.DataFrame(df_dict, index=[0])

        return df_weekly_emission

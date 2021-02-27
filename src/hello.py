# import sys
# import os
# from systemutils.util import UtilMethods
# import platform
import datetime
# print(UtilMethods.get_project_root())
# print(platform.platform())
# # print(util.get_project_root())
# # from data_scrubber.data_scrub import DS
# # import pandas as pd


# # # historical_data_folder_is = 'C:\WorkSpace\Python\hist_astronomia'

# # # data = pd.read_csv(historical_data_folder_is+'\zeel.csv',
# # #                    parse_dates=True, index_col='date')


# # # # print(data.index)
# # # data = DS.clean_dataframe(data)

# # # data = DS.resample_dataframe(df=data, time_window='15min')
# # # data['pOpen'], data['pHigh'], data['pLow'], data['pClose'] = DS.NPreviousDaysOHLC(
# # #     data, prev_days=2)
# # # print(data.tail())
# from pathlib import Path, PureWindowsPath
# import os
# import datetime
# from utils import util

# start_time = int(9) * 60 + int(30)  # specify in int (hr) and int (min) foramte
# end_time = int(15) * 60 + int(10)  # do not place fresh order
# stop_time = int(15) * 60 + int(15)  # square off all open positions

# print(datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)


# print(util.get_project_root().parent)

# # print(get_project_root())
# trigger_minutes = datetime.datetime.now(
# ).minute-(datetime.datetime.now().minute % 5+5)
# print(trigger_minutes)

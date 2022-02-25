from ltp_analysis import *

# ltp分析

input_xlsx = './data/二上口语.xlsx'
ltp_file = './data/二上口语_ltp.pickle'
svo_file = './data/二上口语_svo.pickle'
index_file = './data/二上口语_index.xlsx'

xlsx2ltp(input_xlsx, ltp_file)
ltp2svo(ltp_file, svo_file)


# 特征提取
from feature import *
ltp2index(ltp_file, svo_file, index_file)


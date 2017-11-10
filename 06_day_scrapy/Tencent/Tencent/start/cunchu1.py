# coding=utf-8
import csv
import json


json_file = file('tencent.json','r')
pytype_list = json.load(json_file)

# print pytype_list
# csv_file = file('tencent_data.csv','w')
# csv_writer = csv.writer(csv_file)
#
# head_list = pytype_list[0].keys()
# data_list = [i.values() for i in pytype_list]
#
# csv_writer.writerow(head_list)
# # writerows() 写多行数据,给多层嵌套列表
# csv_writer.writerows(data_list)
#
# csv_file.close()
# json_file.close()
# print '执行成功!'

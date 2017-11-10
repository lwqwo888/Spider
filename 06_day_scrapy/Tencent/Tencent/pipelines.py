# -*- coding: utf-8 -*-
import json
from scrapy.exporters import CsvItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TencentPipeline(object):
    def __init__(self):
        self.f = open("tencent.json", "w")
        self.list = []
    def process_item(self, item, spider):
        print "--" * 20

        content = json.dumps(item) + ","
        self.list.append(content)
        self.f.write(content)
        print content
        return item

    def close_spider(self, spider):
        self.f.close()




        # # -*- coding: utf-8 -*-
        # import csv
        # import sys
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        #
        # class TecentCsvPipeline(object):
        #     def __init__(self):
        #         self.csv_file = file('tencent222.csv', 'w')  # 文件打开第一步,执行一次
        #         self.flag = True
        #
        #     def process_item(self, item, spider):  # 有item返回就执行一次
        #
        #
        #         print "--" * 20
        #         print item
        #         print "--" * 20
        #         '''
        #         {'        people_number': u'1',
        #                  'position_link': u'http://hr.tencent.com/position_detail.php?id=33399&keywords=&tid=0&lid=0',
        #                  'position_name': u'15614-\u6b21\u4e16\u4ee3\u5c04\u51fb\u6e38\u620f\u5e02\u573a\u63a8\u5e7f\uff08\u4e0a\u6d77\uff09',
        #                  'position_type': u'\u4ea7\u54c1/\u9879\u76ee\u7c7b',
        #                  'publish_times': u'2017-10-17',
        #                  'work_location': u'\u4e0a\u6d77'}
        #         '''
        #
        #         # 创建关键csv读写对象
        #         csv_writer = csv.writer(self.csv_file)
        #
        #         # 取出所有的键作为第一行
        #         head_list = item.keys()
        #         # 取出所有的值作为第二行
        #         data_list = item.values()
        #
        #         # 只有一个表头,所以第一次才进行表头写入
        #         if self.flag:
        #             csv_writer.writerow(head_list)
        #             self.flag = False
        #         # 写入数据 每次item返回的都是一条职位信息的数据,所以每次都只把各项数据写到一行,不需要使用写入多行
        #         csv_writer.writerow(data_list)
        #
        #     def close(self, spider):
        #         self.csv_file.close()  # 文件关闭在最后一步,只执行一次






    def open_spider(self, spider):
        # 创建csv文件对象
        self.f = open("tencent.csv", "w")

        #创建csv文件读写对象
        self.csv_exporter = CsvItemExporter(self.f)

        # 开始执行item数据的读写操作
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 停止item数据的读写操作
        self.csv_exporter.finish_exporting()
        self.f.close()

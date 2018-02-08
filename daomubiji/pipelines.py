# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
# 当前工程的设置信息
from scrapy.utils.project import get_project_settings
class DaomubijiPipeline(object):
    def __init__(self):

        self.file = open('./小说1.xls','w',encoding='gbk')


    def process_item(self, item, spider):
        item = dict(item)
        json_str = json.dumps(item,ensure_ascii=False)
        self.file.write(json_str+'\n')
        return item


    def close_spider(self,spider):
        self.file.close()


class Daomubiji2MsqlPipeline(object):
    def __init__(self):
    # 打开数据库
        settings = get_project_settings()
        host = settings.get('DB_HOST')
        port = settings.get('DB_PORT')
        user = settings.get('DB_USER')
        password = settings.get('DB_PWD')
        db = settings.get('DB_NAME')
        charset = settings.get('DB_CHARSET')

        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        sql = "insert into xiaoshuo1(chapter_name,chapter_urls,chapter_content) values('%s','%s','%s')" \
              % (item['chapter_name'], item['chapter_urls'],json.dumps(item['chapter_content'],ensure_ascii=False))
        self.cursor.execute(sql)

        self.conn.commit()
        return item


    def close_spider(self,spider):
        self.conn.close()
        self.cursor.close()


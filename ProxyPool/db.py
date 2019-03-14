import pymongo
from ProxyPool.error import PoolEmptyError
from ProxyPool.setting import MONGO_HOST, MONGO_PORT
from ProxyPool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re


class MongoClient(object):
    def __init__(self, host=MONGO_HOST, port=MONGO_PORT):
        """
        初始化
        :param host: mongo 地址
        :param port: mongo 端口
        :param password: mongo密码
        """
        client = pymongo.MongoClient(host=host, port=port)
        self.db = client.ProxyDB
        self.collection=self.db.proxies


    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return

        if self.collection.find_one({'proxy':proxy}) == None:
            return self.collection.insert_one({'proxy':proxy,'score':score})



    def random(self):
        """
        先按照降序获取所有代理,然后
        :return: 随机代理
        """

        results = self.collection.find().sort('SCORE',pymongo.ASCENDING)
        if not results==None:
            p=[]
            for result in results:
                p.append(result.get('proxy'))
            return choice(p)
        else:
            raise PoolEmptyError



    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        result = self.collection.find_one({'proxy':proxy})
        score=result['score']
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            result['score']=score-1
            condition={'proxy':proxy}#更新条件
            return self.collection.update(condition, result)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.collection.remove({'proxy':proxy})

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.collection.find_one({'proxy':proxy}) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        condition={'proxy':proxy}
        return self.collection.update(condition, {'proxy': proxy, 'score': MAX_SCORE})

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.collection.find().count()

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.collection.find()

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        result = self.collection.find().sort('score', pymongo.ASCENDING)
        return [result[i].get('proxy') for i in range(start, stop)]


if __name__ == '__main__':
    conn = MongoClient()
    r = conn.batch(680, 688)
    print(r)

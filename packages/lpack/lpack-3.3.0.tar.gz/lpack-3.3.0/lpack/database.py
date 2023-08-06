import json
import time

from .utils import cprint
import pymysql
import pymongo
import redis
import oss2
import elasticsearch as es
import urllib3
import pika
from clickhouse_driver import Client
import kafka
from kafka.admin.new_partitions import NewPartitions

urllib3.disable_warnings()


def check_sock(func):
    """

    重置连接装饰器, 连接池的底层实现逻辑
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        if not self.ping():
            self.reconnect()
        return func(self, *args, **kwargs)

    return wrapper


class Database:
    """
    该class集成pymssql和pymysql的使用方法，主要做了对insert功能的封装
    其中 1 表示 mysql， 2 表示 sqlserver

    :param host         :       服务器地址
    :param user         :       用户名
    :param password     :       密码
    :param dbname       :       数据库名
    :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver

    连接形式如下 :
        db_config={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
    """

    def __init__(self, host='localhost', port=3306, user='root', password='321', mode=1, dbname='mysql', tbname='db',
                 charset='utf8', db_config=None, **kwargs):
        if db_config:
            self.mode = int(db_config['mode']) if db_config.get('mode') else mode
            self.host = db_config['host'] if db_config.get('host') else host
            if self.mode == 2:
                self.port = 1433
            else:
                self.port = 3306
            self.user = db_config['user'] if db_config.get('user') else user
            self.password = db_config['password'] if db_config.get('password') else password
            self.dbname = db_config['dbname'] if db_config.get('dbname') else dbname
            self.tbname = db_config['tbname'] if db_config.get('tbname') else tbname
            self.charset = db_config['charset'] if db_config.get('charset') else charset
        else:
            self.mode = int(mode)
            self.host = host
            self.port = port
            if self.mode == 2:
                self.port = 1433
            self.user = user
            self.password = password
            self.dbname = dbname
            self.tbname = tbname
            self.charset = charset
        self.db_config = {'mode': self.mode, 'host': self.host, 'port': self.port, 'user': user,
                          'password': password if password else '',
                          'dbname': dbname, 'tbname': tbname}
        self.con = self.get_con(host=self.host, port=self.port, user=self.user, password=self.password, mode=self.mode,
                                dbname=self.dbname, tbname=self.tbname, charset=self.charset)
        self.cur = self.con.cursor()

    @staticmethod
    def get_con(host='localhost', port=3306, user='root', password='321', mode=1, dbname='main', tbname='log',
                charset='utf8', **kwargs):
        """
        :param host         :       服务器地址
        :param user         :       用户名
        :param password     :       密码
        :param dbname       :       数据库名
        :param mode         :       连接方式，1表示连接mysql，2表示连接sqlserver
        形式如下 :
            db_config={'host': 'localhost', 'user': 'root', 'password': 'xxx', 'dbname': 'test', 'mode': 1}
        """

        if mode == 1:
            con = pymysql.connect(host='%s' % host, user='%s' % user, port=int(port),
                                  password='%s' % password, charset=charset, database=dbname)
        else:
            assert 1 == 0, 'mode is must be 1 !'
        # sqlserver
        # elif mode == 2:
        #     con = pymssql.connect(server='%s' % host, user='%s' % user, port='%s' % port,
        #                           password='%s' % password, database='%s' % dbname, charset=charset)
        #     pymssql.set_max_connections(200000)
        return con

    def build(self, dbname, tbname, data, mode):
        """
           插入方法sql语句封装
           @:param see method "insert"

           data: [(field1, field2, field3, ....), [(data1, data2, data3,...), (data1, data2, data3,...), ......]]
        """
        if isinstance(data, dict):
            assert 1 == 0, '不允许是字典！！！'
        if isinstance(data, list) and isinstance(data[0], dict):
            field = tuple(data[0].keys())
            values = [tuple(sub_data[x] for x in sub_data) for sub_data in data]
        else:
            field = data[0]
            if not isinstance(field, tuple):
                field = tuple(field)
            values = data[1]

        if mode == 1:

            field_char = str(field).replace("'", '`')
            if len(field) == 1:
                field_char = field_char.replace(',', '')
            sql = """insert into `%s`.`%s` %s values ({})""" % (
                dbname,
                tbname,
                field_char
            )
            sql = sql.format(('%s,' * len(field))[:-1])

            return sql, values

        # sqlserver
        # elif mode == 2:
        #     sql = """insert into %s.dbo.%s %s values ({})""" % (
        #         dbname,
        #         tbname,
        #         str(field).replace("'", '')
        #     )
        #     sql = sql.format(('%s,' * len(field))[:-1])
        #     return sql, values

    def insert(self, data, dbname=None, tbname=None, mode=None, size=10000):
        try:
            self.con.ping()
        except:
            self.con.ping(reconnect=True)
        """

        2019-08-05 全部改用insertmany方法，速度提升约五倍

        封装插入方法，以字典或列表包含字典或列表包含元组形式.
        :param dbname       :          库名
        :param tbname       :          表明
        :param data         :          数据集，为如下形式

                                       data = [(field1, field2, field3, ......),
                                               [(data1, data2, data3, ...), (data1, data2, data3, ...), (data1, data2, data3, ...)]

        :param mode         :          mode, different mode leads to different database system

        insert into dbname.tbname (field1, field2, field3) values (%s, %s, %s)

        """
        if mode is None:
            mode = self.mode

        if not dbname:
            dbname = self.dbname

        if not tbname:
            tbname = self.tbname

        if tbname.find('.') > 0:
            tbname = tbname.split('.')[-1]

        # type list with dict or tuple
        result = self.build(dbname, tbname, data, mode)
        columns, values = result
        for i in range(len(values) // size + 1):
            self.cur.executemany(columns, values[i * size: (i + 1) * size])
            self.con.commit()

    def execute(self, sql, *params):
        try:
            self.con.ping()
        except:
            self.con.ping(reconnect=True)
        self.cur.execute(sql, *params)
        return self.cur

    def commit(self):
        self.con.commit()

    def fetchall(self):
        self.cur.fetchall()

    def fetchone(self):
        self.cur.fetchone()

    def close(self):
        self.con.close()

    def ping(self):
        return True if self.con._sock else False

    def reconnect(self):
        self.con = self.get_con(**self.db_config)
        self.cur = self.con.cursor()


class RedisCon(redis.Redis):
    def __init__(self, host='localhost', port=6379, password='', db=0, *args, **kwargs):
        self.params = dict({'host': host, 'port': port, 'password': password, 'db': db, 'decode_responses': True},
                           **kwargs)
        super(RedisCon, self).__init__(**self.params)

    def change_db(self, db=0):
        self.params['db'] = db
        self.execute_command("""select %s""" % db)
        self.params['db'] = int(db)

    def select(self, db=0):
        return self.change_db(db)

    def __repr__(self):
        return "%s<%s>" % (
            type(self).__name__, self.params
        )


class MongoCon:

    def __init__(self, host='localhost', port=27017, user='root', password='321', auth_db='admin', dbname='tmp',
                 colname='tmp',
                 charset='utf8', db_config=None, use_uri=False, uri=None, **kwargs):
        self.auth_db = auth_db
        self.colname = colname
        self.dbname = dbname
        if isinstance(port, str):
            port = int(port)

        if uri:
            self.mongo_con = pymongo.MongoClient(uri)
        elif use_uri and not uri:
            self.mongo_con = pymongo.MongoClient(
                'mongodb://%(user)s:%(password)s@%(host)s:%(port)s/?authSource=%(dbname)s' % {'user': user,
                                                                                              'password': password,
                                                                                              'host': host,
                                                                                              'port': port,
                                                                                              'dbname': auth_db})
        else:
            self.mongo_con = pymongo.MongoClient(host=host, port=port, username=user, password=password,
                                                 authSource=auth_db)

    def db(self, dbname=None):
        dbname = dbname or self.dbname or 'tmp'
        return self.mongo_con[dbname]

    def col(self, colname=None, dbname=None):
        dbname = dbname or self.dbname or 'tmp'
        colname = colname or self.colname
        return self.db(dbname)[colname]


MysqlCon = Database


class OssCon:
    def __init__(self, AccessKeyId, AccessKeySecret, BucketRegion=None, BucketName=None):
        """
        params:
            AccessKeyId:        oss AccessKeyId
            AccessKeySecret:    oss AccessKeySecret
            BucketRegion:       a url like:http://oss-cn-hongkong-internal.aliyuncs.com,
                                hongkong means region of your bucket, if not use internal
                                internet, remove "-internal"
            BucketName:         your bucket name
        """
        self.auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        self.AccessKeyId, self.AccessKeySecret = AccessKeyId, AccessKeySecret
        self.BucketRegion = BucketRegion
        self.BucketName = BucketName
        if BucketRegion and BucketName:
            self.bucket = oss2.Bucket(self.auth, BucketRegion, BucketName)

    def get_bucket(self, BucketRegion: str = None, BucketName: str = None):
        """
        function to set bucket whenever you want if BucketRegion and BucketName not set when initializing
        """
        BucketRegion = BucketRegion or self.BucketRegion
        BucketName = BucketName or self.BucketName
        self.bucket = oss2.Bucket(self.auth, BucketRegion, BucketName)

    def push_bytes(self, name, data):
        """
        params:
            name:       file name in oss bucket
            data:       bytes data of anything, like images, mp4 and so on
        """
        self.bucket.put_object(name, data)

    def push_file(self, name, file_name):
        """

        upload your local file(file_name) to oss with a new "name"
        """
        self.bucket.put_object_from_file(name, file_name)


class ESCon:
    """
    # 批量更新
    # for i in range(10):
    #     lis.append({'_index': 'test-index5', 'name': f'that{i*10}, yes', 'age': i, '_id': i, 'text': f'that ooo {i}'})
    # helpers.bulk(client, lis)


    # 有则更新，无责创建
    # resp = client.index(index="test-index", id='10086', body={"name": '2', 'id': 4})
    # print(resp['result'])

    # version < 8
    # resp = client.search(index="dev_wss_es_law", body={"query": {"match_all": {}}}, size=100)
    # for hit in resp['hits']['hits']:
    #     print(hit['_source'])

    # version >= 8
    # 精准匹配，分词，例如：可匹配"hahaha this is a test10 gogogog"
    # resp = client.search(index="test-index5", query={"match_phrase": {'name': 'this is a test10'}})
    # for hit in resp['hits']['hits']:
    #     print(hit)

    # 精准匹配2，不分词，例如：不可匹配"hahaha this is a test10 gogogog"
    # resp = client.search(index="test-index5", query={"term": {'name': 'this is a test10'}})
    # for hit in resp['hits']['hits']:
    #     print(hit)

    # 分词匹配，查询包含 this 或 is 或 a 或 test 的文档
    # resp = client.search(index="test-index5", query={"match": {'name': 'this is a test'}})
    # for hit in resp['hits']['hits']:
    #     print(hit)

    # 大于小于
    # resp = client.search(index="test-index5", query={"range": {'age': {'gte': 3, 'lt': 9}}})
    # for hit in resp['hits']['hits']:
    #     print(hit)

    # # must， 计算分值
    # resp = client.search(index="test-index5", query={"bool": {"must": {'term': {'age': 3}}}})
    # print(resp)
    # for hit in resp['hits']['hits']:
    #     print(hit)
    #
    #
    # # filter，不计算分值
    # resp = client.search(index="test-index5", query={"bool": {"filter": {'term': {'age': 3}}}})
    # print(resp)
    # for hit in resp['hits']['hits']:
    #     print(hit)


    # should，或逻辑
    # resp = client.search(index="test-index5", query={"bool": {"should": [{'range':{'age': {'gte': 7}}}, {'range':{'age': {'lte': 2}} }]}})
    # # print(resp)
    # for hit in resp['hits']['hits']:
    #     print(hit)


    # must，且逻辑
    # resp = client.search(index="test-index5", query={"bool": {"must": [{'range':{'age': {'gte': 2}}}, {'range':{'age': {'lte': 7}} }]}})
    # # print(resp)
    # for hit in resp['hits']['hits']:
    #     print(hit)
    """

    def __init__(self, host, port, password):
        if es.VERSION[0] <= 7:
            self.es_con = es.Elasticsearch([host, ], http_auth=('elastic', password), scheme="http", port=port, )
        else:
            self.es_con = es.Elasticsearch(hosts=[{'host': host, 'port': port, 'scheme': 'https'}, ],
                                           basic_auth=('elastic', password), request_timeout=30, verify_certs=False)

    @property
    def client(self):
        return self.es_con


class MQCon:
    def __init__(self, host: str, port: int, user: str, password: str, vhost='/', queue_name: str = '',
                 arguments: dict = {}, publish_type='normal', exchange='', router=''):
        if exchange:
            if router:
                publish_type = 'fanout'
            else:
                publish_type = 'direct'
        self.exchange = exchange
        self.router = router
        self.publish_type = publish_type
        self.queue_name = queue_name
        self.arguments = arguments
        credentials = pika.PlainCredentials(username=user, password=password)
        parameters = pika.ConnectionParameters(host=host,
                                               port=port,
                                               virtual_host=vhost,
                                               credentials=credentials,
                                               heartbeat=0,
                                               socket_timeout=10,
                                               retry_delay=10,
                                               )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        if self.exchange:
            self.declare_exchange(self.exchange, self.publish_type)
        if self.queue_name:
            assert self.queue_name and self.arguments, 'queue_name and arguments mush be both not None or both None'
            if not self.router:
                self.declare_queue(self.queue_name, '', self.arguments)
            else:
                self.declare_queue(self.queue_name, self.router, self.arguments)

    def declare_exchange(self, exchange: str, publish_type: str):
        assert exchange or self.exchange, 'Exchange must be declared during initialization or here!'
        assert publish_type or self.publish_type, 'Publish type must be declared during initialization or here!'
        if not self.exchange:
            self.exchange = exchange
        if not exchange:
            exchange = self.exchange
        if publish_type:
            self.publish_type = publish_type
        publish_type = self.publish_type
        self.channel.exchange_declare(exchange=exchange, exchange_type=publish_type)

    def declare_queue(self, queue_name: str = '', router: str = None, arguments: dict = {}):
        # x-max-priority x-expires x-message-ttl
        self.queue_name = queue_name
        if self.publish_type == 'normal':
            result = self.channel.queue_declare(queue=queue_name, durable=True, arguments=arguments)
        elif self.publish_type in {'fanout', 'direct'}:
            result = self.channel.queue_declare(queue=queue_name, durable=True, arguments=arguments, exclusive=True)
            self.bind_exchange(exchange=self.exchange, queue_name=queue_name, router=router)
        queue_name = result.method.queue
        return queue_name

    def publish(self, data: dict, delivery_mode=2, expiration=None, priority=None, exchange='', router='', **kwargs):
        if expiration and isinstance(expiration, int):
            expiration = str(expiration)
        new_data = bytes(json.dumps(data), encoding='utf8')
        if self.publish_type == 'normal':
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=new_data,
                                       properties=pika.BasicProperties(
                                           **dict(
                                               {'delivery_mode': delivery_mode, 'expiration': expiration,
                                                'priority': priority},
                                               **kwargs)))
        elif self.publish_type in {'fanout', 'direct'}:
            # assert exchange and not router, 'Exchange must be declared and router must be empty!'
            if not exchange:
                exchange = self.exchange
            if not router:
                router = self.router
            self.channel.basic_publish(exchange=exchange, routing_key=router, body=new_data,
                                       properties=pika.BasicProperties(
                                           **dict(
                                               {'delivery_mode': delivery_mode, 'expiration': expiration,
                                                'priority': priority},
                                               **kwargs)))

    def bind_exchange(self, exchange: str = '', router: str = None, queue_name: str = ''):
        self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=router)

    def delete_queue(self, queue_name: str):
        self.channel.queue_delete(queue_name)

    def close(self):
        self.connection.close()


class ClickhouseCon:

    def __init__(self, host: str, port: int, user: str, password: str, dbname: str = 'default', tbname: str = None):
        self.dbname = dbname
        self.tbname = tbname
        self.client = Client(host=host, port=port, user=user, password=password, database=dbname)

    def use(self, dbname: str):
        self.client.execute(f'use {dbname}')
        return True

    @staticmethod
    def build(char: str):
        if isinstance(char, str):
            return f'{char}'
        elif isinstance(char, int):
            return char
        elif isinstance(char, list):
            return char

    def insert(self, columns: list, values: list, dbname: str = 'default', tbname: str = None):
        """
        example:
        1. create table test
            (
                name String,
                age UInt32,
                info Nested(
                    name String,
                    age UInt32
                )
            ) engine=MergeTree()
            order by name

        2.
        from llpack import database
        ck_con = database.ClickhouseCon(host='localhost', port=8123, user='test', password='test', dbname='default', tbname='test')

        lis = []
        keys = ['name', 'age', 'info.name', 'info.age']
        for i in range(100):
            lis.append((f'luoyoyo{i}', 28, [f'luoyoyo{i}', f'{i}'], [28, i]))

        ck_con.insert(tbname='test', columns=keys, values=lis)

        """
        if not tbname:
            tbname = self.tbname
        if not dbname:
            dbname = self.dbname
        q1 = f"""insert into {dbname}.{tbname} ({", ".join(columns)}) values """
        q2 = list(map(lambda x: str(tuple(map(lambda y: self.build(y), x))), values))
        q2 = ' '.join(q2)
        result = self.client.execute(q1 + q2)
        return result

    def execute(self, q: str):
        return self.client.execute(q)

    def show_tb_info(self, dbname: str = None, tbname: str = None):
        if not dbname:
            dbname = self.dbname
        if not dbname:
            assert dbname is not None, 'database name must not be None'
        if not tbname:
            tbname = self.tbname
        if not tbname:
            assert tbname is not None, 'table name must not be None'
        result = self.client.execute(f"""desc {tbname}""")
        title = 'column\t\t\t\t\t\ttype\t\t\t\t\t\tttl\t\t\t\t\t\t\t\t\t\tdesc'
        cprint(title, c='y')
        for i in result:
            char = f'{i[0]}{" " * (28 - len(i[0]))}{i[1]}'
            if i[-1]:
                char += f'{" " * (39 - len(i[0]) - len(i[1]))}{i[-1]}'
            if i[4]:
                char += f'{" " * (56 - len(i[0]) - len(i[1]) - len(i[-1]))}{i[4]}'
            print(char)
        table_comment = self.client.execute(
            f"""SELECT comment FROM system.tables WHERE database = '{dbname}' AND name = '{tbname}';""")[0][0]
        if table_comment:
            cprint('\nTable Comment: \t', table_comment, c='y')
        return result

    def show_create_info(self, dbname: str = None, tbname: str = None):
        if not dbname:
            dbname = self.dbname
        if not dbname:
            assert dbname is not None, 'database name must not be None'
        if not tbname:
            tbname = self.tbname
        if not tbname:
            assert tbname is not None, 'table name must not be None'
        result = self.client.execute(f"""show create {tbname}""")[0][0]
        print(result)
        return result


class KafkaCon:

    def __init__(self, host: str, port: int, username: str, password: str, hosts=None, group_id: str = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.hosts = hosts
        if self.host and self.port and not self.hosts:
            self.hosts = [f'{self.host}:{self.port}']
        self.conf = {
            'bootstrap_servers': self.hosts,
            'sasl_mechanism': 'PLAIN',
            'security_protocol': 'SASL_PLAINTEXT',
            'sasl_plain_username': self.username,
            'sasl_plain_password': self.password,
        }
        self.admin = kafka.KafkaAdminClient(**self.conf)

    @property
    def producer(self):
        return kafka.KafkaProducer(**self.conf)

    def get_consumer(self, group_id: str = None):
        return kafka.KafkaConsumer(**dict(self.conf, **{'group_id': group_id}))

    def partition(self, mapping: dict or list):
        if isinstance(mapping, dict):
            partition_mapping = {
                topic: NewPartitions(mapping[topic]) for topic in mapping
            }
        elif isinstance(mapping, list):
            partition_mapping = {
                x[0]: NewPartitions(x[1]) for x in mapping
            }
        else:
            assert isinstance(mapping, dict) or isinstance(mapping, list), 'Mapping must be dict or list'
        self.admin.create_partitions(partition_mapping)

    def send(self, topic: str, data: dict, key: str = None, partition: int = None):
        data = bytes(json.dumps(data), encoding='utf8')
        key = bytes(key, encoding='utf8')
        result = self.producer.send(topic=topic, value=data, key=key, partition=partition)
        self.producer.flush()
        return result

    def consume(self, topics: list or str, group_id: str = None):
        if isinstance(topics, str):
            topics = [topics]
        self.consumer = self.get_consumer(group_id)
        self.consumer.subscribe(topics)
        for message in self.consumer:
            topic = message.topic
            partition = message.partition
            offset = message.offset
            timestamp = message.timestamp
            key = message.key
            value = message.value
            yield json.loads(value.decode('utf8'))

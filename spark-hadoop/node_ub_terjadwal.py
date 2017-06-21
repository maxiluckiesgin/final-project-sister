import cql
from pyspark import SparkContext,SQLContext
from pyspark.sql import Row
from apscheduler.schedulers.blocking import BlockingScheduler


sc = SparkContext.getOrCreate()
sc.setLogLevel("ERROR")
sqlContext = SQLContext(sc)


db = cql.connect('192.168.43.66', 9160,  'sister', cql_version='3.0.0')

def proses() :
    curs = db.cursor()
    curs.execute("SELECT node,suhu FROM suhu_ub")
    suhu = curs.fetchall()
    curs.execute("SELECT node,kelembaban FROM kelembaban_ub limit 100")
    kelembaban =  curs.fetchall()
    data = {'suhu_max' : [], 'kelembaban_max' : [], 'suhu_avg' : [] , 'kelembaban_avg' : []}

    #print suhu
    # Load dari textFile
    rddsuhu = sc.parallelize(suhu)
    rddkelembaban = sc.parallelize(kelembaban)
    rddsuhu_ = rddsuhu.map(lambda x: Row(node=x[0], suhu=x[1]))
    rddkelembaban_ = rddkelembaban.map(lambda x: Row(node=x[0], kelembaban=x[1]))
    df_suhu = sqlContext.createDataFrame(rddsuhu_)
    df_kelembaban = sqlContext.createDataFrame(rddkelembaban_)

    df_suhu.write.format('com.databricks.spark.csv').mode('overwrite').option("header", "true").save("/datastore/suhu.csv")
    df_kelembaban.write.format('com.databricks.spark.csv').mode('overwrite').option("header", "true").save("/datastore/kelembaban.csv")
    print "berhasil menulis ke hadoop"

    df_suhu_in = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load('/datastore/suhu.csv')
    df_kelembaban_in = sqlContext.read.format('com.databricks.spark.csv').options(header='true').load('/datastore/kelembaban.csv')
    print "berhasil load dari hadoop"
    suhu_groupbyNode = df_suhu_in.groupby('node')
    kelembaban_groupbyNode = df_kelembaban_in.groupby('node')
    print "kalkulasi data"
    suhu_max = suhu_groupbyNode.agg({'suhu': 'max'}).rdd.map(list).collect()
    suhu_avg = suhu_groupbyNode.agg({'suhu': 'mean'}).rdd.map(list).collect()
    kelembaban_max = kelembaban_groupbyNode.agg({'kelembaban': 'max'}).rdd.map(list).collect()
    kelembaban_avg = kelembaban_groupbyNode.agg({'kelembaban': 'mean'}).rdd.map(list).collect()
    data['suhu_max'].append(suhu_max)
    data['kelembaban_max'].append(kelembaban_max)
    data['suhu_avg'].append(suhu_avg)
    data['kelembaban_avg'].append(kelembaban_avg)

    #print data
    #[[u'Surabayaub', u'30.0'], [u'Pasuruanub', u'39.0'], [u'Malangub', u'24.0']]
    #[[u'Surabayaub', u'66.0'], [u'Pasuruanub', u'62.0'], [u'Malangub', u'68.0']]
    print "update cassandra"
    for kolom,baris in data.items():
        for node in baris:
            for nilai in node:
                sql = "UPDATE dummy set "+kolom+"="
                sql += str(nilai[1])
                sql += " where node='"
                sql += str(nilai[0])
                sql +="'"
                print sql
                curs.execute(sql)



scheduler = BlockingScheduler()
interval = 2
print "menjalankan dengan interval ",interval,"detik"
scheduler.add_job(proses, 'interval', seconds=interval)
scheduler.start()

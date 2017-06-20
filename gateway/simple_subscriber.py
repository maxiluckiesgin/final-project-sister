# Import library paho-mqtt
from flask import Flask
import cql, json
import paho.mqtt.client as mqtt
from thread import start_new_thread

# Definisikan app flask
app = Flask(__name__)

# Koneksi ke cassandra dengan key sister
db = cql.connect('192.168.43.66', 9160,  'sister', cql_version='3.0.0')

# Inisiasi mqtt client
mqttc = mqtt.Client("sub1", clean_session=False)

# Buat koneksi ke broker
mqttc.connect("iot.eclipse.org", 1883)

# Format data json

# Definisi fungsi route 127.0.0.1/node
@app.route('/node', methods=['GET'])
def semua():
    curs = db.cursor()
    curs.execute("SELECT * FROM dummy")
    data = curs.fetchall()
    return json.dumps(data, sort_keys=True)

# Inisiasi callback function
def on_message(mqttc, obj, msg):
    topic_split = msg.topic.split("/") #node/humidity = ["node","1","suhu"]
    curs = db.cursor()

    value = 0
    node = ""
    if topic_split[1] == "humidity" :
        curs.execute("SELECT count(*) FROM kelembaban_ub")
        sql = "INSERT into kelembaban_ub(id, "
        sql += "kelembaban,"
        value = msg.payload
    else :
        curs.execute("SELECT count(*) FROM suhu_ub")
        sql = "INSERT into suhu_ub(id,"
        sql += "suhu,"
        value = msg.payload
    id_cur = curs.fetchall()
    id_ = id_cur[0][0]+1
    sql +="node,waktu) values("
    sql += "'"+str(id_)+"'"
    sql += ","
    sql += str(value)
    sql += ","
    sql += "'"+topic_split[0]+"'"
    sql += ",toTimestamp(now())"
    sql += ")"
    #print sql
    curs.execute(sql)
    print "Berhasil update data ", topic_split[1] ," pada ", topic_split[0]
    #except:
    #    print "Error: gagal melakukan update database"
    #print "Topik "+msg.topic+" Payload "+msg.payload + " QoS " + str(msg.qos)

#Registrasi callback function
mqttc.on_message = on_message

# Subscribe dengan topik tertentu
#mqttc.subscribe("/node/1/suhu", qos=1)

#wildcard
#mqttc.subscribe("/node/#", qos=1)
mqttc.subscribe("Malangub/#", qos=0)
mqttc.subscribe("Pasuruanub/#", qos=0)
mqttc.subscribe("Surabayaub/#", qos=0)

# Looping subscriber
start_new_thread(mqttc.loop_forever, ())
app.run(debug=True, port=5566)

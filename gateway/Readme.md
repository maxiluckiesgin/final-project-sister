<b> subscriber - cassandra - webservice </b> <br/>

<b> Require </b> <br/>
1. cql <br/>
pip install cql <br/> <br/>
2. paho-mqtt <br/>
pip install paho-mqtt <br/> <br/>
3. flask <br/>
pip install flask <br/> <br/>
<b>JSON format to consume</b><br/>
```python
{ "node" : [
    {
      'wilayah' : '',
      'kelembaban_avg' :0,
      'kelembaban_max' :0,
      'suhu_avg' :0,
      'suhu_max' : 0
    }]
}

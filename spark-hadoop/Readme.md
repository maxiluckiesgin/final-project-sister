<b> cassandra - hadoop - spark - cassandra </b> <br/>
<b>node_ub</b> - run only once <br/>
<b>node_ub_terjadwal</b> - run scheduled by 30 min <br/>
<br/>
<b> Require </b> <br/>
cql <br/>
pip install cql <br/>
apscheduler <br/>
pip install apscheduler <br/>
run it with <br/>
spark-submit --packages com.databricks:spark-csv_2.11:1.5.0 node_ub_terjadwal.py<br/>
or add --master option to run it in cluster mode

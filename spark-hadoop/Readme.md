<b> cassandra - hadoop - spark - cassandra </b> <br/>
node_ub - run only once <br/>
node_ub_terjadwal - run scheduled by 30 min <br/>
<br/>
<b> Require </b> <br/>
cql <br/>
pip install cql <br/>
apscheduler <br/>
pip install apscheduler <br/>
run it with <br/>
spark-submit --packages com.databricks:spark-csv_2.11:1.5.0 node_ub_terjadwal.py<br/>
or add --master option to run it in cluster mode

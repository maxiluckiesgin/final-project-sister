<b> cassandra - hadoop - spark - cassandra </b> <br/>
<b>node_ub</b> - run only once <br/>
<b>node_ub_terjadwal</b> - run scheduled by 30 min <br/>
<br/>
<b> Require </b> <br/>
1. cql <br/>
pip install cql <br/> <br/>
2. apscheduler <br/>
pip install apscheduler <br/><br/>

<h4>run it with </h4>
spark-submit --packages com.databricks:spark-csv_2.11:1.5.0 node_ub_terjadwal.py<br/>
or add --master option to run it in cluster mode

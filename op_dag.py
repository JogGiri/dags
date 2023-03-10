from airflow import DAG
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

from airflow.sensors.filesystem import FileSensor
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    "retry": 5,
    "retry_delay": timedelta(minutes=5)
}

def _downloading_data(**kwargs):
    with open("my_file.txt","w") as f:
        f.write("my_data")

with DAG(dag_id="op_dag", default_args=default_args, start_date=datetime(2022,1,1), schedule_interval="@daily", catchup=True) as dag:

    downloading_data = PythonOperator(
        task_id="downloading_data",
        python_callable= _downloading_data
        #op_kwargs={"my_param":42}
    )

    waiting_for_data = FileSensor(
        task_id="waiting_for_data",
        fs_conn_id="fs_default",
        filepath="my_file.txt",
        poke_interval=30 #seconds to check sensors
    )

    processing_data = BashOperator(
        task_id = "processing_data",
        bash_command= "exit 0"
    )


    downloading_data.set_downstream(waiting_for_data)
    waiting_for_data.set_downstream(processing_data)

import sys
from airflow import DAG
from random import randint
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


def _training_model(ti):
    ti.xcom_push(key='model_accuracy', value= randint(1, 10))
    return


def _choose_best_model(ti):
    accuracies = ti.xcom_pull(key='model_accuracy', task_ids=['Training_Model_A', 'Training_Model_B','Training_Model_C'])
    print("Accuracies: "+str(accuracies))
    best_accuracy = accuracies[0]
    if best_accuracy > 5:
        return 'Accurate'
    else:
        return 'Not_Accurate'


with DAG("my_dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", catchup=False) as dag:
    training_model_A = PythonOperator(task_id="Training_Model_A", python_callable=_training_model)
    training_model_B = PythonOperator(task_id="Training_Model_B", python_callable=_training_model)
    training_model_C = PythonOperator(task_id="Training_Model_C", python_callable=_training_model)

    choose_best_model = BranchPythonOperator(task_id="Choose_Best_Model", python_callable=_choose_best_model)

    accurate = BashOperator(task_id="Accurate",
                            bash_command="printf '============\n\nAccurate\n\n=============' ")
    not_accurate = BashOperator(task_id="Not_Accurate",
                                bash_command="printf '============\n\nNot Accurate\n\n=============' ")

    [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, not_accurate]

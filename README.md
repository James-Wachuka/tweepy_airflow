###### tweepy-airflow
Using airflow and tweepy to show trending hashtags 20 minutes

###### getting started with tweepy_airflow
First, create a new folder called tweepy_airflow.
Run this command:
```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml``` to download the docker compose file. The file contains several services definitions, including airflow-scheduler, airflow-webserver, airflow-worker, airflow-init, postgres, and redis

###### adding data volumes to docker-compose file
volumes will be used to store data. 

```volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    # volume to store data
    - ./data:/opt/airflow/data
```

###### initialize airflow and run the dags
Ensure docker is running then run ```docker-compose up airflow-init```. Dags are contained/put in the dags folder.
After airflow is initialized start services ->run ```docker-compose up```
use ```docker ps``` to confirm that the services are running then navigate to ```localhost:8080```

###### tweepy_dag.py (trending_hashtags dag)
The dag that contains functions to connect to twitter.The dag uses  ```PythonVirtualvenvOperator``` to create and activate the venv that uses tweepy module.
All the operations are wrapped in one callable function to avoid Xcom issues.

The dag contains two tasks 
```
get_api_2 = PythonVirtualenvOperator(
    task_id='connecting_to_twitter_api',
    python_callable = get_api,
    requirements = ["tweepy"],
    system_site_packages=False,
    dag = trending_hashtags,
)

message_out = PythonOperator(
    task_id = 'task_complete_message',
    python_callable = message,
    dag = trending_hashtags,
)
```

###### airflow web UI
Using the web UI access the  ```trending hashtags dag``` unpause and trigger the dag. Use any of theview options to monitor the progress of dag. check logs for ouput and possibe errors

use ```docker-compose``` to the services




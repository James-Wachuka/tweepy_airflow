#importing libraries
from datetime import timedelta
import airflow
import os 

#from app import tweepy
from airflow import DAG
from airflow.operators.python import PythonOperator # for executing python functions
from airflow.operators.python import PythonVirtualenvOperator # for working with venvs airflow

# function to get twitter API, get trending topics for Nairobi and log them
def get_api():
    # importing a package in the function ensures that it is accessible when the venv is created
    import tweepy
    # api credentials - input yours
    consumer_key = "Vc8kfWvaGtbPTqyBkA2AuKcxo"
    consumer_secret = "J2oDrXCLfPVJKSfG7g7JpYuAO1n7rtaOTLoEGpdmfxBNfeebBf"
    access_token = "1357221708541939714-cR46HEPE3SKDJuGx1HMQaReM6OQGks"
    access_token_secret = "qCtyFv0CmO8ZhvfkfAk3STLizu995TNQJSxTOLGO6a0Yh"

    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # authentication of access token and secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print("successfuly activated virtual env and connected to twitter API")
    # cordinates for Nairobi city
    lat= 1.2921
    long= 36.8219
    # methods to get trends- tweepy==4.6.0
    closest_loc = api.closest_trends(lat, long)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    trends_ = trends[0]["trends"]
    hashtags = [trend["name"] for trend in trends_ if "#" in trend["name"]]
    # print hashtags
    for elem in hashtags:
        print(elem) 

    
def message():
    print("task complete")

default_args = {
 'owner':'airflow',
 'depends_on_past' : False,
 'start_date': airflow.utils.dates.days_ago(7),
}

trending_hashtags = DAG(
    'trending_hashtags', #name of the dag
    default_args = default_args,
    schedule_interval = timedelta(minutes=20),
    catchup = False
)

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

get_api_2 >> message_out
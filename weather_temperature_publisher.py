import os
import time
import requests
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the current working directory and credentials file from environment variables
current_dir = os.getcwd()
credentials_file = os.getenv("CREDENTIALS_FILE")
credentials_path = os.path.join(current_dir, credentials_file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

publisher = pubsub_v1.PublisherClient()
topic_path = os.getenv("TOPIC_PATH")
publisher_id = "Publisher_C0001"  # Define a unique Publisher ID


def fetch_temperature_data():
    url = "https://cuaca-gempa-rest-api.vercel.app/weather/jawa-barat/bandung"  # /cimahi, /lembang
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            # Extract all temperature data points
            for param in data["data"]["params"]:
                if param["id"] == "t":
                    return param["times"]
    return []


# Fetch all temperature data points
temperature_data_points = fetch_temperature_data()

# Publish each temperature data point to the topic
for temp_data in temperature_data_points:
    temperature = temp_data["celcius"]
    data_suhu = f"Temperature: {temperature}".encode("utf-8")

    future = publisher.publish(topic_path, data_suhu, publisher_id=publisher_id)

    print(f"Published message id : {future.result()}")
    print(f"Publisher ID: {publisher_id}")
    print(f"Data: {data_suhu.decode('utf-8')}")
    time.sleep(10)

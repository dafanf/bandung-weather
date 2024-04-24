import os
import random
import time
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the current working directory and credentials file from environment variables
current_dir = os.getcwd()
credentials_file = os.getenv('CREDENTIALS_FILE')
credentials_path = os.path.join(current_dir, credentials_file)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    
publisher = pubsub_v1.PublisherClient()
topic_path = os.getenv('TOPIC_PATH')

# Publish 5 messages to the topic with randomize temperature in range 15 to 35
for _ in range(5):
    temperature = random.randint(15, 35)
    data = f"Temperature: {temperature}"
    data_encoded = data.encode("utf-8")
    future = publisher.publish(topic_path, data_encoded)
    print(f"Published message id : {future.result()}")
    print(f"Data: {data}")
    time.sleep(10)
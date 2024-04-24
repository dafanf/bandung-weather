import os
from dotenv import load_dotenv
import time
from google.cloud import pubsub_v1

# Load environment variables from .env file
load_dotenv()

# Get the current working directory and credentials file from environment variables
current_dir = os.getcwd()
credentials_file = os.getenv('CREDENTIALS_FILE')
credentials_path = os.path.join(current_dir, credentials_file)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

timeout = 60.0  # Set the timeout duration

# Create a subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscriber_path = os.getenv('SUBSCRIBER_PATH')

def callback(message):
    print(f"Received message: {message}")
    print(f"Data: {message.data}")
    message.ack()

# Subscribe to the topic and listen for messages
streaming_pull_future = subscriber.subscribe(subscriber_path, callback=callback)
print(f"Listening for messages on {subscriber_path}")

with subscriber:
    try:
        # Wait for the specified timeout duration
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        # Handle timeout situations
        print(f"Streaming pull future timeout of {timeout} seconds.")
        streaming_pull_future.cancel()
        streaming_pull_future.result()

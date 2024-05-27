import os
from dotenv import load_dotenv
import time
from google.cloud import pubsub_v1

# Load environment variables from .env file
load_dotenv()

# Get the current working directory and credentials file from environment variables
current_dir = os.getcwd()
credentials_file = os.getenv("CREDENTIALS_FILE")
credentials_path = os.path.join(current_dir, credentials_file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

timeout = 600.0  # Set the timeout duration

# Create a subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscriber_path = os.getenv("SUBSCRIBER_PATH")

# Dictionary to store temperatures for each publisher
publisher_temperatures = {}


def callback(message):
    publisher_id = message.attributes.get("publisher_id", "Unknown")
    data = message.data.decode("utf-8")
    print(f"Received message from Publisher ID: {publisher_id}")
    print(f"Data: {data}")

    # Extract temperature value from the data
    try:
        temperature = float(data.split(": ")[1].replace(" C", ""))
    except (IndexError, ValueError) as e:
        print(f"Failed to extract temperature: {e}")
        message.ack()
        return

    # Update temperature list for the publisher
    if publisher_id not in publisher_temperatures:
        publisher_temperatures[publisher_id] = []
    publisher_temperatures[publisher_id].append(temperature)

    # Calculate and display the average temperature for the publisher
    average_temperature = sum(publisher_temperatures[publisher_id]) / len(
        publisher_temperatures[publisher_id]
    )
    print(
        f"Publisher ID: {publisher_id}, Average Temperature: {average_temperature:.2f} C"
    )

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

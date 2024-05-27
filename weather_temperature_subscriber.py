import os
import time
from google.cloud import pubsub_v1
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the current working directory and credentials file from environment variables
current_dir = os.getcwd()
credentials_file = os.getenv("CREDENTIALS_FILE")
credentials_path = os.path.join(current_dir, credentials_file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

subscriber = pubsub_v1.SubscriberClient()
subscription_path = os.getenv("SUBSCRIBER_PATH")

# Check if subscription_path is correctly set
if not subscription_path:
    raise ValueError("SUBSCRIPTION_PATH environment variable is not set.")

# Store temperature readings by client for calculating the average
temperature_by_client = {}
all_temperatures = []


def callback(message):
    data_str = message.data.decode("utf-8")
    temperature_str = data_str.split(": ")[1].rstrip(" C")
    temperature = float(temperature_str)

    client_id = message.attributes["publisher_id"]
    if client_id not in temperature_by_client:
        temperature_by_client[client_id] = []
    temperature_by_client[client_id].append(temperature)
    all_temperatures.append(temperature)

    print(f"======================= CLIENT {client_id} ======================")
    print(f"Suhu: {temperature_str}")

    # Calculate and print the average temperature for the current client
    temps_client = temperature_by_client[client_id]
    avg_temp_client = sum(temps_client) / len(temps_client)
    print(f"Rata-rata suhu untuk Client ID {client_id}: {avg_temp_client:.2f}")
    print("=====================================================================\n")

    # Calculate and print the average temperature for all clients
    avg_temp_all = sum(all_temperatures) / len(all_temperatures)
    print("========================= SUHU KOTA BANDUNG =========================")
    print(f"Rata-rata Suhu: {avg_temp_all:.2f}")
    print("=====================================================================\n")

    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

# Keep the main thread alive to keep receiving messages
try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()

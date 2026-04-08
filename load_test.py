import requests
import threading
import os

# GitHub Secrets থেকে URL এবং ইউজার সংখ্যা নেওয়া হবে
URL = os.getenv('TARGET_URL', 'https://example.com')
NUM_USERS = int(os.getenv('NUM_USERS', 10))

def send_request():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        print(f"Status: {response.status_code} | URL: {URL}")
    except Exception as e:
        print(f"Error: {e}")

threads = []
print(f"Starting load test on {URL} with {NUM_USERS} users...")

for _ in range(NUM_USERS):
    thread = threading.Thread(target=send_request)
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()

print("Load test complete.")
      

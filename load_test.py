import requests
import threading
import os
import time

# GitHub Secrets বা এনভায়রনমেন্ট থেকে URL এবং থ্রেড সংখ্যা নেওয়া
URL = os.getenv('TARGET_URL', 'https://example.com')
# কতগুলো সমান্তরাল থ্রেড চলবে (একই সাথে কতগুলো লুপ চলবে)
NUM_THREADS = int(os.getenv('NUM_THREADS', 10))

def send_infinite_requests(thread_id):
    print(f"Thread-{thread_id} started...")
    count = 0
    while True:
        try:
            # ব্রাউজার হেডার যুক্ত করা হলো যাতে সহজে ব্লক না করে
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
            response = requests.get(URL, headers=headers, timeout=10)
            count += 1
            # প্রতি ১০টি রিকোয়েস্ট পর পর স্ট্যাটাস প্রিন্ট করবে (কনসোল ক্লিন রাখার জন্য)
            if count % 10 == 0:
                print(f"Thread-{thread_id}: Sent {count} requests. Last Status: {response.status_code}")
        
        except requests.exceptions.RequestException:
            # সার্ভার ডাউন হলে বা কানেকশন এরর হলে এখানে আসবে
            print(f"Thread-{thread_id}: Server might be down or blocking. Retrying...")
            time.sleep(1) # এরর হলে ১ সেকেন্ড বিরতি
        except Exception as e:
            print(f"Thread-{thread_id} Error: {e}")
            break

if __name__ == "__main__":
    print(f"🚀 Starting infinite load test on: {URL}")
    print(f"🧵 Total Threads: {NUM_THREADS}")
    
    threads = []
    for i in range(NUM_THREADS):
        # প্রতিটি থ্রেড আলাদা আলাদা ভাবে অনন্তকাল রিকোয়েস্ট পাঠাবে
        t = threading.Thread(target=send_infinite_requests, args=(i,))
        t.daemon = True # মেইন প্রোগ্রাম বন্ধ হলে থ্রেডও বন্ধ হবে
        t.start()
        threads.append(t)

    # মেইন থ্রেডকে জীবিত রাখা
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping load test...")
        

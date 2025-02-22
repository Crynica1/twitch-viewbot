import threading
import time
import random
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

# Default Proxies List
PROXIES = [
   
]

# Function to create a viewer session
def create_viewer(stream_url, viewer_id, proxy_enabled):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")

    # Use proxy if enabled
    if proxy_enabled:
        proxy = PROXIES[viewer_id % len(PROXIES)]
        options.add_argument(f"--proxy-server=http://{proxy}")

    # Remove headless mode for Twitch detection
    # options.add_argument("--headless")

    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(stream_url)
        print(f"👀 Viewer {viewer_id} started on {stream_url}")

        # Simulate real behavior (scroll, click)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(5, 10))

        # Stay on stream for 1-5 minutes
        stay_duration = random.randint(60, 300)
        time.sleep(stay_duration)

    except Exception as e:
        print(f"⚠️ Error in Viewer {viewer_id}: {e}")
    finally:
        driver.quit()
        print(f"🚪 Viewer {viewer_id} session closed.")

# Function to start bot from GUI
def start_bot():
    stream_url = url_entry.get()
    num_viewers = int(viewers_entry.get())
    proxy_enabled = proxy_var.get()

    if not stream_url.startswith("https://www.twitch.tv/"):
        messagebox.showerror("Error", "Please enter a valid Twitch URL!")
        return

    messagebox.showinfo("Started", f"Starting {num_viewers} viewers for {stream_url}")

    threads = []
    for i in range(num_viewers):
        t = threading.Thread(target=create_viewer, args=(stream_url, i+1, proxy_enabled))
        t.start()
        threads.append(t)
        time.sleep(random.randint(2, 5))  # Delay to avoid detection

    for t in threads:
        t.join()

    messagebox.showinfo("Completed", "All viewers have been started!")

# Create GUI
root = tk.Tk()
root.title("Twitch Viewbot")
root.geometry("400x300")

tk.Label(root, text="Twitch Stream URL:").pack()
url_entry = tk.Entry(root, width=40)
url_entry.pack()

tk.Label(root, text="Number of Viewers:").pack()
viewers_entry = tk.Entry(root, width=10)
viewers_entry.pack()
viewers_entry.insert(0, "5")  # Default value

proxy_var = tk.BooleanVar()
proxy_check = tk.Checkbutton(root, text="Enable Proxies", variable=proxy_var)
proxy_check.pack()

start_button = tk.Button(root, text="Start Bot", command=start_bot)
start_button.pack()

root.mainloop()

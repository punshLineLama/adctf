import schedule
import time
import configuration

# Checks the services
def checker():

    return 
# places new flags
def placer():

    return
# invalidates old flags
def invalidate():

    return

def tick():
    checker()
    # Replace this with the task you want to perform
    print("Placing new flags and invalidating old ones.")

# Schedule the task to run every 3 minutes
schedule.every(3).minutes.do(do_task)

while True:
    schedule.run_pending()
    time.sleep(1)
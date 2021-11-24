import time
import sys

from api.db_client import init_db

def schedule_db_init(delay, repeat):
    current_time = time.time()
    target_time = current_time + delay

    while True:
        current_time = time.time()
        if current_time >= target_time:
            break
        else:
            time.sleep(60)
    
    filename = init_db()

    print(f"Successfully created a new DB and saved it as '{filename}'.")


if __name__ == "__main__":
    delay = float(sys.argv[1])
    repeat = bool(sys.argv[2])
    schedule_db_init(delay, repeat)
    
    if repeat:
        schedule_db_init(delay, repeat)

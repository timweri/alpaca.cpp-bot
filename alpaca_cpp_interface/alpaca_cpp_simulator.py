import time
import random

if __name__ == "__main__":
    count = 0

    # for _ in range(5):
    while True:
        input_str = input("> ") + '\n'

        print("This is", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(" just", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(" a test", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(f" number {count}", flush=True)

        print("This is", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(" just", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(" a test", end="", flush=True)
        time.sleep(random.uniform(0.1,1))
        print(f" number {count}", flush=True)

        count += 1

        if "EOF\n" == input_str:
            break

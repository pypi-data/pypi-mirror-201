import requests

import ext

urls = [
    "https://google.com",
    "https://yahoo.com",
    "https://bing.com",
    "https://jasdiojioajds.com",
    "https://duckduckgo.com",
    "https://ask.com",
    "https://aol.com",
    "https://wikipedia.org",
    "https://github.com",
    "https://stackoverflow.com",
]


def main():
  print("version '1.5.2'")
  ext.exec_ext()

  for url in urls:
    try:
      r = requests.get(url)
      print(f"{url} - {r.status_code}")
    except requests.exceptions.ConnectionError:
      print(f"{url} - DOWN")


# def intro_app():
#   print("Hello, World!")
#   exec()


# ================



# if __name__ == "__main__":
#   intro_app()


# import asyncio
# import time


# async def async_task(num):
#   # This is an example asynchronous task that takes a number as input
#   # and returns its square after a delay of 1 second

#   await asyncio.sleep(1)
#   await time.sleep(1)
#   return num**2


# async def async_task_list(nums):
#   # This function takes a list of numbers as input and returns a list
#   # of their squares after running the async_task for each number
#   coroutines = [async_task(num) for num in nums]
#   results = await asyncio.gather(*coroutines)
#   return results

# # Example usage
# nums = [1, 2, 3, 4, 5]

# start_time = time.time()

# results = asyncio.run(async_task_list(nums))
# print(results)

# print(f"Time taken: {time.time() - start_time}")

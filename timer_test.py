def fn():
    print("Hello, world")

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone="Europe/London")
scheduler.start()
job = scheduler.add_job(fn, trigger='interval', seconds=1)
job.modify(max_instances = 1)

import time
import pygame

pygame.init() 
screen = pygame.display.set_mode((600, 400))

start_time = time.perf_counter()
time.sleep(2)
print(time.perf_counter()-start_time)


start_pygame = pygame.time.get_ticks()
time.sleep(2)
print((pygame.time.get_ticks()-start_pygame)/1000)

start_pygame = pygame.time.get_ticks()
start_time = time.perf_counter()
while (time.perf_counter()-start_time) < 2.0:
    waiting = True
print((pygame.time.get_ticks()-start_pygame)/1000)



#5-Q

from random import random
import asyncio
import time

# coroutine to generate work


async def producer(queqe,id):
    print(f'{time.ctime()} Producer {id}: Running')
    # generate work
    for i in range(10):
        # generate work
        value = random()
        # block to simulate work
        await asyncio.sleep(id*0.1)
        # add to the queqe
        await queqe.put(value)
    print(f'{time.ctime()} Producer {id}: Done')


async def consumer(queqe):
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit for work
        item = await queqe.get()
        # report
        print(f'{time.ctime()} >got {item}')
        # block while processing
        if item:
            await asyncio.sleep(item)
        # mark as completed
        queqe.task_done()
    # all done
    print(f'{time.ctime()} Consumer: Done')

# entry point coroutine


async def main():
    # create the shared queqe
    queue = asyncio.Queue(2)
    # start the consumer
    _ = asyncio.create_task(consumer(queue))
    # create many product
    product = [producer(queue,_) for _ in range(5)]
    # run and wait for the producers to finish
    await asyncio.gather(*product)
    # wait for the consumer to process all item
    await queue.join()
# start the asyncio program
asyncio.run(main())
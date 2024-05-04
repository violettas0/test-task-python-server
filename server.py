import asyncio
import random
import datetime

num_answ = 0
CLIENTS = []


async def handle_client(reader, writer):
    client_id = len(CLIENTS) + 1
    CLIENTS.append(writer)
    global num_answ
    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode().strip()
        if message.startswith("["):
            if random.random() < 0.1:
                log_message(datetime.datetime.now(), message, "", "")
                response = '(РїСЂРѕРёРіРЅРѕСЂРёСЂРѕРІР°РЅРѕ)'
                writer.write(response.encode() + b'\n')
                await writer.drain()
            else:
                delay = random.randint(100, 1000) / 1000
                await asyncio.sleep(delay)
                num_req = int(message.split("[")[1].split()[0])
                response = f"[{num_answ}/{num_req} PONG] ({client_id})"
                writer.write(response.encode() + b'\n')
                num_answ += 1
                await writer.drain()
                log_message(datetime.datetime.now(), message,
                            datetime.datetime.now() + datetime.timedelta(seconds=delay), response)
    writer.close()


async def send_keepalive():
    global num_answ
    while True:
        await asyncio.sleep(5)
        for writer in CLIENTS:
            if not writer.is_closing():
                response = f"[{num_answ}] keepalive"
                writer.write(response.encode() + b'\n')
                await writer.drain()
                num_answ += 1


def log_message(received_time, request, response_time, response):
    with open('server_log.txt', 'a') as log_file:
        response_time_str = response_time.strftime("%H:%M:%S.%f") if response_time else ""
        response_str = response if response else "(РїСЂРѕРёРіРЅРѕСЂРёСЂoРІР°РЅРѕ)"
        log_file.write(f"{received_time.date()};{received_time.time()};{request};{response_time_str};{response_str}\n")


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        await asyncio.gather(server.serve_forever(), send_keepalive())


asyncio.run(main())

import asyncio
import random
import datetime


async def tcp_client(log_file):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    try:
        num = 0
        while True:
            await asyncio.sleep(random.uniform(0.3, 3))
            message = f"[{num} PING]"
            writer.write(message.encode() + b'\n')
            await writer.drain()
            timestamp_req = datetime.datetime.now().strftime("%H:%M:%S.%f")
            data = await reader.readline()
            if not data:
                break
            response = data.decode().strip()
            timestamp_resp = datetime.datetime.now().strftime("%H:%M:%S.%f")
            log_message(log_file, datetime.datetime.now().date(), timestamp_req, message, timestamp_resp, response)
            num += 1
    finally:
        writer.close()


def log_message(log_file, date, request_time, request, response_time, response):
    with open(log_file, 'a') as log:
        if 'keepalive' in response:
            log.write(f"{date};{response_time};{response}\n")
        elif '(РїСЂРѕРёРіРЅРѕСЂРёСЂРѕРІР°РЅРѕ)' in response:
            log.write(f"{date};{request_time};{request};{response_time};(С‚Р°Р№РјaСѓС‚)\n")
        else:
            log.write(f"{date};{request_time};{request};{response_time};{response}\n")


async def main():
    await asyncio.gather(tcp_client('first-client_log.txt'), tcp_client('second-client_log.txt'))


asyncio.run(main())

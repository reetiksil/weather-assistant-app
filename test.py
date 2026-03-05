import edge_tts
import asyncio

async def list_voices():
    voices = await edge_tts.list_voices()
    for v in voices:
        print(v["Name"])

asyncio.run(list_voices())
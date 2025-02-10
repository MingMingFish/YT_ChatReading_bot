import pytchat
import asyncio # 執行序同步執行

async def main():
  livechat = pytchat.LiveChatAsync("Owke6Quk7T0", callback = func)
  while livechat.is_alive():
    await asyncio.sleep(3)
    #other background operation.

  # If you want to check the reason for the termination, 
  # you can use `raise_for_status()` function.
  try:
    livechat.raise_for_status()
  except pytchat.ChatDataFinished:
    print("Chat data finished.")
  except Exception as e:
    print(type(e), str(e))

#callback function is automatically called periodically.
async def func(chatdata):
  for c in chatdata.items:
    print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
    await chatdata.tick_async()


if __name__=='__main__':
  try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
  except asyncio.exceptions.CancelledError:
    pass
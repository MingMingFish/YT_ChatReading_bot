# pip install pytchat
import pytchat
while True:
    chat = pytchat.create(video_id="Owke6Quk7T0")
    while chat.is_alive():
        for c in chat.get().sync_items():
            print(f"{c.datetime} [{c.author.name}]: {c.message}")
    chat.terminate()
    print("Chat connection ended, reconnecting...")
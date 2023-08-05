async def start_banall(Legend, message):
   chat = message.chat
   x = Legend.send_message(chat.id, "Hey it's Legend Bot Spam")
   done = 0
   failed = 0
   async for u in Legend.get_chat_members(chat.id):
      user = u.user
      try:
         await Legend.ban_chat_member(chat.id, user.id)
         done += 1
      except Exception as err:
         print(f"Legend Bot Spam- [INFO]: {str(err)}")
         failed += 1
   await x.delete()
   await Legend.send_message(chat.id, f"Members Banned ✓ \n\n Banned {done} users\n failed {failed}")

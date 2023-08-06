from tinydb import TinyDB, Query
import time
import os
# from importlib.resources import files
# print(__file__)
# print("HI")
# chat_history_path = os.path.join(os.path.dirname(__file__), 'db', "gpt_chatbot_chat_history.json")
# print(chat_history_path)
# chat_history_path = files("gptchatbotcli.db").joinpath("gpt_chatbot_chat_history.json").read_text()
home_dir = os.path.expanduser("~")
chat_history_path = os.path.join(home_dir, ".gpt_chatbot_chat_history.json")
if not os.path.exists(chat_history_path):
  with open(chat_history_path, "x") as f:
    f.write("")
db = TinyDB(chat_history_path)

def init_chat_history(message, preset, model):
  # generate random string
  _id = str(time.time()).replace(".", "")
  # print("Saving chat history...")
  db.insert({"_id": _id, "preset": preset, "model": model, 'messages': message})
  return _id

def update_chat_history(id, message):
  db.update({'messages': message}, Query()._id == id)
  return True

def get_all_chat_history():
  return db.all()

def defind_chat_title(id, title):
  db.update({'title': title}, Query()._id == id)

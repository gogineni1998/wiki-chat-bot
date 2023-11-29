import queue

import wikipedia
import json
import os
import re

wikipedia.set_lang('en')

topics = ['Health','Environment','Technology','Economy','Entertainment','Sports','Politics','Education','Travel','Food']

dict_main ={}
dict_main['title'] = []
dict_main['revision_id'] = []
dict_main['summary'] = []
dict_main['description'] = []
dict_main['url'] = []
dict_main['topic'] = []

duplicate_check = set()

def create_document(content_json,topic):
  summary = re.sub("[^a-zA-Z ]+", '', content_json.summary).strip()
  content = re.sub("[^a-zA-Z ]+", '', content_json.content).strip()
  if len(summary) > 200 and content_json.revision_id not in duplicate_check:
      dict_main['title'].append(content_json.title)
      dict_main['revision_id'].append(str(content_json.revision_id))
      dict_main['summary'].append(summary)
      dict_main['description'].append(content)
      dict_main['url'].append(content_json.url)
      dict_main['topic'].append(topic)
      duplicate_check.add(content_json.revision_id)
      return 1
  return 0

q = queue.Queue()

for topic in topics:
  doc_count = 0
  search_results = wikipedia.search(topic, results=10000)
  for search_result in search_results:
    q.put(search_result)

  while(q.empty() != True):
    try:
      page = q.get()
      content_json = wikipedia.page(page, auto_suggest=False)
      for link in content_json.links:
        q.put(link)
      count = create_document(content_json,topic)
      doc_count = doc_count + count
      if(doc_count%100 == 0):
        print("completed: ", doc_count, topic,flush = True)
      if(doc_count > 5000):
        break
    except Exception as e:
      a = e
  print(doc_count, topic,flush = True)

with open("ir_data.json", "w") as f:
  json.dump(dict_main, f, indent=4)

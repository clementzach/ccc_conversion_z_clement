import pandas as pd
from ics import Calendar, Event
import os
import datetime
import arrow

def get_name(input_string):
  str_vector = input_string.split()
  if len(str_vector) > 1:
    return(str_vector[0] + " " + str_vector[1])
  else:
    return(input_string)



def is_valid_account(input_string):
  is_valid = True
  if len(input_string) > 3:
  	is_valid = False
  elif len(input_string) == 1:
  	is_valid = False
  else:
  	for i in range(len(input_string)):
  		if not input_string[i].isupper():
  			is_valid = False
  return(is_valid)

def get_account_num(input_string):
  words_vector = input_string.split()
  if is_valid_account(words_vector[-1]):
  	return(words_vector[-1])
  else:
    possibles_list = []
    for word in words_vector:
      if is_valid_account(word):
        possibles_list.append(word)
    if len(possibles_list) == 1:
      return(possibles_list[0])
    elif len(possibles_list) == 0:
      return('')
    else:
      print_string = "could not decide between "
      for word in possibles_list:
        print_string = print_string + word + " "
      print(print_string)
      print("choosing " + possibles_list[1])
      return(possibles_list[1])

def change_time_zone(input_date):
  end_daylight = arrow.get('2021-11-07T02:00:58.970460-06:00')
  start_daylight = arrow.get('2022-03-13T02:00:58.970460-06:00')
  start_daylight_2 = arrow.get('2021-11-06T02:00:58.970460-06:00')
  end_daylight_2 = arrow.get('2022-03-12T02:00:58.970460-06:00')
  if input_date == None:
    return(None)
  elif input_date.is_between(end_daylight, start_daylight) or input_date.is_between(end_daylight_2, start_daylight_2):
    return(input_date.to('UTC-07').replace(tzinfo = 'UTC').datetime)
  else:
    return(input_date.to('UTC-06').replace(tzinfo = 'UTC').datetime)





















##find file in current directory with an ics 
files_in_folder = os.listdir('.')

in_file_list = []

for file in files_in_folder:
        if file[-3:] == 'ics' and file[0] != '.':
                in_file_list.append(file)




out_df_list = []
sheet_names = []
for in_file in in_file_list:

  with open(in_file, 'r') as file:
    ics_text = file.read()
  
  ## import calendar file
  
  c = Calendar(ics_text)
  
  
  #make a bunch of empty lists
  event_name = []
  begin = []
  end = []
  dur = []
  uid = []
  desc = []
  created = []
  last_mod = []
  loc = []
  url = []
  transp = []
  alarms = []
  attend = []
  cat = []
  stat = []
  org = []
  classify = []	
  
  #iterate through events and add to file

  
  for e in c.events:
    event_name.append(e.name)
    begin.append(e.begin)
    end.append(e.end)
    dur.append(e.duration)
    uid.append(e.uid)
    desc.append(e.description)
    created.append(e.created)
    last_mod.append(e.last_modified)
    loc.append(e.location)
    url.append(e.url)
    transp.append(e.transparent)
    alarms.append(e.alarms)
    attend.append(e.attendees)
    cat.append(e.categories)
    stat.append(e.status)
    org.append(e.organizer)
    classify.append(e.classification)
    
  
  
  
  out_df = pd.DataFrame({"event_name":event_name,
  "begin":begin,
  "end":end,
  "duration":dur,
  "uid":uid,
  "description":desc,
  "created at":created,
  "last modified": last_mod,
  "location": loc,
  "url":url,
  "transparent":transp,
  "alarms":alarms,
  "attendees":attend,
  "categories":cat,
  "status":stat,
  "organizer":org,
  "classification":classify})
  
  
  out_df.begin = out_df.begin.apply(change_time_zone)
  out_df.end = out_df.end.apply(change_time_zone)
  
  
  
  out_df.begin = pd.to_datetime(out_df.begin).dt.tz_localize(None)
  
  out_df.end = pd.to_datetime(out_df.end).dt.tz_localize(None)
  
  
  out_df = out_df.drop(["created at", "last modified"], axis = 1)
  

  
  out_df['client_name'] = out_df.event_name.apply(get_name)

  out_df['account_num'] = out_df.event_name.apply(get_account_num)
  out_df_list.append(out_df)
  sheet_names.append(in_file[:-5])
  
  

writer = pd.ExcelWriter('calendar_created_' + str(datetime.datetime.now().date()) + '.xlsx')  

for i in range(len(out_df_list)):
  df = out_df_list[i]
  df.to_excel(writer, sheet_name = sheet_names[i][0:15], index = False)

writer.save()




## TODO: does this work if appointments are scheduled in daylight savings time?
  
  

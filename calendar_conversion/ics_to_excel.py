import pandas as pd
from ics import Calendar, Event
import os
import datetime
import arrow

##find file in current directory with an ics 
files_in_folder = os.listdir('.')

for file in files_in_folder:
        if file[-3:] == 'ics' and file[0] != '.':
                in_file = file



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
i = 0

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
	



out_df = pd.DataFrame({"name":event_name,
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



out_df.begin = out_df.begin.apply(lambda x: x.tz_localize(None))
out_df.end = out_df.end.apply(lambda x: x.tz_localize(None))

#out_df.begin = pd.to_datetime(out_df.begin, errors = 'coerce', utc = True)

#out_df.end = pd.to_datetime(out_df.end, errors = 'coerce', utc = True)

#out_df.begin = out_df.begin.apply(lambda x: x.date())
#out_df.end = out_df.end.apply(lambda x: x.date())


#out_df['created at'] = out_df['created at'].apply(lambda x: x.time())
#out_df['last modified'] = out_df['last_modified'].apply(lambda x: x.time())
out_df = out_df.drop(["created at", "last modified"], axis = 1)
out_df.to_csv('finished.csv')
out_df.to_excel("finished.xlsx")



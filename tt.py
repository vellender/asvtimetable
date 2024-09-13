#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:59:33 2024

@author: adam
"""
import csv
import re
from datetime import datetime

def hours_between(start_time, end_time):
    # Define the format in which time is input
    time_format = "%H:%M"
    
    # Convert the start and end time to datetime objects
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    
    # Calculate the time difference in hours
    time_difference = end - start
    hours = time_difference.total_seconds() / 3600
    
    return int(hours)

def extract_before_slash(input_str):
    # Find the index of the first occurrence of "/"
    slash_index = input_str.find('/')
    
    # If "/" is found, return the part before it, otherwise return the whole string
    if slash_index != -1:
        return input_str[:slash_index]
    else:
        return input_str
    
def extract_time(date_time_str):
    # Regular expression to match time in HH:MM format (ignoring seconds)
    match = re.search(r'\b(\d{2}:\d{2})\b', date_time_str)
    
    # Return the matched time if found, otherwise None
    if match:
        return match.group(1)
    else:
        return None
    
def summarize_ranges(lst):
    # Convert string list to integers
    numbers = sorted([int(i) for i in lst])

    # Initialize the result list and tracking variables
    ranges = []
    start = numbers[0]
    end = numbers[0]

    # Iterate through the sorted list of numbers
    for i in range(1, len(numbers)):
        if numbers[i] == end + 1:  # If current number is consecutive
            end = numbers[i]
        else:
            if start == end:
                ranges.append(f"{start}")
            else:
                ranges.append(f"{start}-{end}")
            start = end = numbers[i]

    # Append the last range or number
    if start == end:
        ranges.append(f"{start}")
    else:
        ranges.append(f"{start}-{end}")

    # Join the ranges with commas and return the result
    return ', '.join(ranges)    

def allZeros(lst):
    return all(x == 0 for x in lst)
    
# Define the Activity class
class Activity:
    def __init__(self, week, activityWeekLabel, activityDesc, activityName, activityType, activityTypeName, locationName, startDateTime, endDateTime, day, staff):
        self.week = week
        self.activityWeekLabel = activityWeekLabel
        self.activityDesc = activityDesc
        self.activityName = activityName
        self.moduleCode=extract_before_slash(activityName)
        self.activityType = activityType
        self.activityTypeName = activityTypeName
        self.locationName = locationName
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.startTime = extract_time(startDateTime),
        self.endTime = extract_time(endDateTime),
        self.hours = hours_between(self.startTime[0],self.endTime[0])
        self.day = day
        self.staff = staff

    def __repr__(self):
        return (f"Activity(week={self.week}, activityWeekLabel={self.activityWeekLabel}, activityDesc={self.activityDesc}, "
                f"activityName={self.activityName}, activityType={self.activityType}, activityTypeName={self.activityTypeName}, "
                f"locationName={self.locationName}, startDateTime={self.startDateTime}, endDateTime={self.endDateTime}, "
                f"day={self.day}, staff={self.staff})")
   

# Function to read the CSV and create a list of Activity objects
def load_activities_from_csv(file_path):
    activities = []
    
    # Open the CSV file and read it
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Loop through each row in the CSV and create Activity objects
        for row in reader:
            activity = Activity(
                week=row['Week'],
                activityWeekLabel=row['Activity Week Label'],
                activityDesc=row['Activity Desc'],
                activityName=row['Activity Name'],
                activityType=row['Activity Type'],
                activityTypeName=row['Activity Type Name'],
                locationName=row['Location Name'],
                startDateTime=row['Start Date Time'],
                endDateTime=row['End Date Time'],
                day=row['Day'],
                staff=row['Staff']
            )
            activities.append(activity)
    
    return activities

def weeks(module,startTime,day,locationName):
    return [a.week for a in activities_list if module in a.activityName and day in a.day and startTime in a.startTime and locationName in a.locationName]
    
# CSV loading
csv_file = 'activities.csv'  # Replace this with your CSV file path
activities_list = load_activities_from_csv(csv_file)

# generate a list of unique module, time, day, room combinations:
allActivtiesKeyDetails=[]
for a in activities_list:
    allActivtiesKeyDetails.append((a.moduleCode,a.startTime[0],a.day,a.locationName,a.activityType,a.staff,a.hours))
allActivtiesKeyDetails=tuple(set(allActivtiesKeyDetails))

# for each of these append the week numbers
asv=[]
b=1
for a in allActivtiesKeyDetails:
    b+=1
    asv.append((a[0].replace("FG","MP"),a[1],a[2],a[3],a[4],a[5],a[6],summarize_ranges(weeks(a[0],a[1],a[2],a[3])),b))
asv=sorted(asv,key=lambda c:-c[6])

monday=[a for a in asv if 'Monday' in a if a[0][0]!="X"]
tuesday=[a for a in asv if 'Tuesday' in a if a[0][0]!="X"]
wednesday=[a for a in asv if 'Wednesday' in a if a[0][0]!="X"]
thursday=[a for a in asv if 'Thursday' in a if a[0][0]!="X"]
friday=[a for a in asv if 'Friday' in a if a[0][0]!="X"]

# matrix layout
lookup = {'09:00': 0,'10:00': 1,'11:00': 2,'12:00': 3,'13:00': 4,'14:00': 5,'15:00': 6,'16:00': 7,'17:00': 8}

def renderCell(ID):
    a=getActivity(ID)
    start=""
    if a[6]>1:
        start="colspan='"+str(a[6])+"'"
    return """
    <td """+start+"""class='"""+a[4]+""" year"""+a[0][2]+"""'>
        <p class="modCode" title='"""+a[0]+' '+a[4]+"""'>"""+a[0]+"""</p>
        <p class="room">"""+a[3]+"""</p>
        <p class="staff">"""+a[5].replace("<br>"," ")+"""</p>
        <p class="weeks">"""+a[7]+"""</p>
    </td>"""

def dayMatrix(d):
    M=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    for a in d:
        row=0
        hours=a[6]
        startTime=a[1]
        activityID=a[-1]
        while allZeros(M[row][lookup[startTime]:lookup[startTime]+hours])==False:
            row+=1
        p=0
        while p<hours:
            if p==0:
                M[row][lookup[startTime]+p]=activityID
            else:
                M[row][lookup[startTime]+p]=-1
            p+=1
    return [a for a in M if not allZeros(a)]

def getActivity(ID):
    return [a for a in asv if a[-1]==ID][0]

def renderDay(d):
    out="<tr><th>09:00</th><th>10:00</th><th>11:00</th><th>12:00</th><th>13:00</th><th>14:00</th><th>15:00</th><th>16:00</th><th>17:00</th></tr>"
    for row in dayMatrix(d):
        out+="<tr>\n"
        for a in row:
            if a>0:
                out+=renderCell(a)
            if a==0:
                out+="""<td>&nbsp;</td>"""
        out+="</tr>"
    return out
    
def writeFile(s, f):
    with open(f, 'w') as file:
        file.write(s)

def index():
    out="""<html><head><title>Timetable</title><link rel="stylesheet" type="text/css" href="asvtt.css" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script></head><body><div id="controls"><h2>Controls</h2><p>Isolate yeargroups: <button id="year0">Year 0</button>
<button id="year1">Year 1</button>
<button id="year2">Year 2</button>
<button id="year3">Year 3</button>
<button id="yearM">Year M</button>
<button id="viewAll">View all</button></p>
<p><button id="hideControls">Hide controls (e.g. for printing)</button> (NB: after hiding, clicking on "Monday" will get the controls back).</p>
</div><h2 class="monday">Monday</h2><table>"""
    out+=renderDay(monday)
    out+="</table><h2>Tuesday</h2><table>"
    out+=renderDay(tuesday)
    out+="</table><h2>Wednesday</h2><table>"
    out+=renderDay(wednesday)
    out+="</table><h2>Thursday</h2><table>"
    out+=renderDay(thursday)
    out+="</table><h2>Friday</h2><table>"
    out+=renderDay(friday)
    out+="""</table/</body>
<script>
$('document').ready(()=>{
    $('#year0').click(()=>{
        $('.year0').css('visibility', 'visible');
        $('.year1').css('visibility', 'hidden');
        $('.year2').css('visibility', 'hidden');
        $('.year3').css('visibility', 'hidden');
        $('.yearM').css('visibility', 'hidden');
    });
    
    $('#year1').click(()=>{
        $('.year0').css('visibility', 'hidden');
        $('.year1').css('visibility', 'visible');
        $('.year2').css('visibility', 'hidden');
        $('.year3').css('visibility', 'hidden');
        $('.yearM').css('visibility', 'hidden');
    });    

    $('#year2').click(()=>{
        $('.year0').css('visibility', 'hidden');
        $('.year1').css('visibility', 'hidden');
        $('.year2').css('visibility', 'visible');
        $('.year3').css('visibility', 'hidden');
        $('.yearM').css('visibility', 'hidden');
    });

    $('#year3').click(()=>{
        $('.year0').css('visibility', 'hidden');
        $('.year1').css('visibility', 'hidden');
        $('.year2').css('visibility', 'hidden');
        $('.year3').css('visibility', 'visible');
        $('.yearM').css('visibility', 'hidden');
    });    

    $('#yearM').click(()=>{
        $('.year1').css('visibility', 'hidden');
        $('.year2').css('visibility', 'hidden');
        $('.year3').css('visibility', 'hidden');
        $('.year0').css('visibility', 'hidden');
        $('.yearM').css('visibility', 'visible');
    });
    
    $('#viewAll').click(()=>{
        $('.year1').css('visibility', 'visible');
        $('.year2').css('visibility', 'visible');
        $('.year3').css('visibility', 'visible');
        $('.year0').css('visibility', 'visible');
        $('.yearM').css('visibility', 'visible');
    });
    
    $('#hideControls').click(()=>{
        $('#controls').hide();
    });    
    
    $('.monday').click(()=>{
        $('#controls').show();
    });    
    
});
    
    
    </script>
    </html>"""
    writeFile(out,"index.htm")
index()
import csv


concept_uid = "recgcHII88NuXoipZ"
user_id = "172337"

all_activities = []
activity_mastery = []
activity_history = []

activities_obj  = []
history_obj  = []
mastery_obj  = []



with open('data/Activity.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for ptr,row in enumerate(spamreader):
        if ptr != 0:
            if row[7] == concept_uid:
                all_activities.append(row[0])
                activity_mastery += row[10].split(",")
                activities_obj.append({
                    "Id":row[0],
                    "Timestamp":row[2],
                    "Question":row[4],
                })
                activity_history += row[9].split(",")


print(activities_obj)
print("############################################")

with open('data/Activity_Mastery.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for ptr,row in enumerate(spamreader):
        if row[0] in activity_mastery:
            mastery_obj.append({
                "Id":row[0],
                "Activity Id":row[3],
                "Mastery Level":row[5],
                "Assigned At":row[6],
            })

print(mastery_obj)
print("############################################")

with open('data/Activity_Mastery_History.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for ptr,row in enumerate(spamreader):
        if row[0] in activity_history:
            activity_history.append(row[0])
            history_obj.append({
                "Id":row[0],
                "Created At":row[5],
                "Mastery Level":row[7],
                "Exercise Duration":row[8],
                "Total Duration":row[10]
            })


print(activity_history)
print("############################################")
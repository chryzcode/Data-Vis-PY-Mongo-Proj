import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from decouple import config

pd.set_option('future.no_silent_downcasting', True)

# Read JSON file
print('************ solution 1 - records about an individual sailor*****************')
with open('abership.json') as f:
    data = json.load(f)


# Connect to MongoDB

connection_string= config("MONGO_URI") #database credentials
client = MongoClient(connection_string)
print("************** Connected to MongoDB ***********************")
db = client['CSM6720-Assignment']  # Database name
collection = db['sailor']  # Database collection





print('************* Cleaning data ************************')
#cleaning the data
# Iterate over documents in the collection
for doc in collection.find():
    # Remove the $oid prefix from the _id field
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string

    # Remove any keys with $ prefix
    keys_to_remove = [key for key in doc.keys() if key.startswith('$')]
    for key in keys_to_remove:
        doc.pop(key)  



a_marine_person = [
    {
        '$unwind': '$mariners'
    },
    {
        '$match': {
            'mariners.name': 'John Williams'
        }
    }
]


# Get the aggregation of the marin person data
print('************ Gathering and fetching the user data ***********************')
all_person_details = collection.aggregate(a_marine_person)

# Print all the details
for detail in all_person_details:
    print(detail)





print('************ solution 2 - promotion history of two individual sailors born in Aberystwyth  *****************')


# Convert data to DataFrame
collection_data = collection.find()
data_frame = pd.json_normalize(collection_data, record_path='mariners', meta=['_id', 'vessel name', 'official number', 'port of registry'])

# Filter sailors by name
selected_sailors = data_frame[data_frame['name'].isin(['John Williams', 'Henry Evans'])]

# Filter out rows where joining date is not in the format 'YYYY-MM-DD' or 'YYYY-MM'
selected_sailors = selected_sailors[selected_sailors['this_ship_joining_date']
                                    .str.match(r'^\d{4}-\d{2}(-\d{2})?$')
                                    .infer_objects(copy=False)
                                    .fillna(False)]

# Add default day for incomplete dates
selected_sailors['this_ship_joining_date'] = selected_sailors['this_ship_joining_date'].apply(lambda x: x + '-01' if len(x) == 7 else x)

# Convert joining dates to datetime objects
selected_sailors['this_ship_joining_date'] = pd.to_datetime(selected_sailors['this_ship_joining_date'])

# Sort entries by joining date
selected_sailors = selected_sailors.sort_values(by='this_ship_joining_date')

# Plot promotion timeline for each sailor
print('************ Plotting visualization for specified sailors *****************')
plt.figure(figsize=(10, 6))

for name, group in selected_sailors.groupby('name'):
    plt.plot(group['this_ship_joining_date'], group['this_ship_capacity'], marker='o', label=name)

plt.xlabel('Joining Date')
plt.ylabel('Capacity')
plt.title('Promotion History of Selected Sailors')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
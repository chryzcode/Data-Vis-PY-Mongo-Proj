import json
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
from decouple import config

# Read JSON file
print('************ solution 1 - Visualise individual records of sailors born in Aberystwythr *****************')
with open('abership.json') as f: 
    data = json.load(f)


# Connect to MongoDB

connection_string=config("MONGO_URI") #database credentials
client = MongoClient(connection_string)
print("**************Connected to MongoDB***********************")
db = client['CSM6720-Assignment']  # Database name
collection = db['sailor']  # Database collection


# Convert data to DataFrame
data_frame = pd.json_normalize(data, record_path='mariners', meta=['_id', 'vessel name', 'official number', 'port of registry'])




# Clean the capacity column
data_frame['this_ship_capacity'] = data_frame['this_ship_capacity'].str.replace('[^a-zA-Z\s]', '', regex=True)

# Filter sailors born in Aberystwyth
aberys_sailors = data_frame[data_frame['place_of_birth'] == 'Aberystwyth']

# Group by capacity and count the number of Aberystwyth-born sailors for each capacity
aberys_sailors_by_capacity = aberys_sailors.groupby('this_ship_capacity').size()

# Group by capacity and count the total number of sailors for each capacity
total_sailors_by_capacity = data_frame.groupby('this_ship_capacity').size()

# Calculate the proportion of Aberystwyth-born sailors for each capacity
proportion_by_capacity = (aberys_sailors_by_capacity / total_sailors_by_capacity) * 100

# Visualize the proportion of Aberystwyth-born sailors at each capacity
plt.figure(figsize=(10, 6))
proportion_by_capacity.plot(kind='bar', color='skyblue')
plt.xlabel('Capacity')
plt.ylabel('Proportion (%)')
plt.title('Proportion of Aberystwyth-born Sailors at Each Capacity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



print('************ solution 2 - Visualise the number of sailors sailing from each port *****************')

# Clean the joining port column
data_frame['joining_port'] = data_frame['this_ship_joining_port'].str.replace('[^a-zA-Z\s]', '', regex=True)

# Group by joining port and count the number of sailors joining from each port
sailors_by_joining_port = data_frame.groupby('joining_port').size().sort_values(ascending=False)

# Visualize the number of sailors joining from each port
plt.figure(figsize=(10, 6))
sailors_by_joining_port.plot(kind='bar', color='skyblue')
plt.xlabel('Joining Port')
plt.ylabel('Number of Sailors')
plt.title('Number of Sailors Joining from Each Port')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
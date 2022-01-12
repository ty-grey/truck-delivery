import csv
import json
from hash_table import HashTable
from package import Package

config = json.load(open('config.json'))
max_packages = config['max_packages']
package_hash_map = HashTable()
package_together = ['13', '14', '15', '16', '19', '20']
priority_times = ['9:00 AM']
location_names, location_distances = [], []
first_truck_unsorted, second_truck_unsorted, third_truck_unsorted = [], [], []
no_truck = []

# Open with the right encoding to avoid encoding signatures at file start
with open('data/package_data.csv', encoding='utf-8-sig') as csv_file:
    csv_split = csv.reader(csv_file, delimiter=',')

    # Create a package off the split line and add some data to manipulate later
    for line in csv_split:
        p_id = line[0]
        address = line[1]
        city = line[2]
        state = line[3]
        p_zip = line[4]
        deadline = line[5]
        mass = line[6]
        note = line[7]
        delivered_time = None
        priority = False
        launch_time = None

        # Only sort special packages for now
        if ('EOD' not in deadline and 'Delayed' not in note) \
                or 'Must be' in note or p_id in package_together:
            first_truck_unsorted.append(p_id)
            if deadline in priority_times:
                priority = True
        elif 'truck 2' in note:
            second_truck_unsorted.append(p_id)
        elif 'EOD' not in deadline and 'Delayed' in note:
            second_truck_unsorted.append(p_id)
            priority = True
        elif 'Delayed' in note or 'Wrong' in note:
            third_truck_unsorted.append(p_id)
        else:
            no_truck.append(p_id)

        package = Package(p_id, address, city, state, p_zip, deadline, mass, note, delivered_time, priority,
                          launch_time)
        package_hash_map.insert(p_id, package)

    # Sort all regular packages after special ones have been sorted
    # This is so packages with special notes get on the trucks they need to be on and not hindered by
    # packages that can be delivered at any time
    for p_id in no_truck:
        if len(first_truck_unsorted) < max_packages:
            first_truck_unsorted.append(p_id)
        elif len(second_truck_unsorted) < max_packages:
            second_truck_unsorted.append(p_id)
        elif len(third_truck_unsorted) < max_packages:
            third_truck_unsorted.append(p_id)

with open('data/location_names.csv', encoding='utf-8-sig') as csv_file:
    location_names = list(csv.reader(csv_file, delimiter=','))

with open('data/location_distances.csv', encoding='utf-8-sig') as csv_file:
    location_distances = list(csv.reader(csv_file, delimiter=','))


# Return location_names and location_distances in one list to reduce amount of code
def get_location_info():
    return [location_names, location_distances]


# Return package_hash_map for easy retrieval in other files
def get_package_map():
    return package_hash_map


# Return all unsorted trucks in one list to reduce amount of code
def get_unsorted_trucks():
    return [first_truck_unsorted, second_truck_unsorted, third_truck_unsorted]


# Return truck launch times
def get_launch_times():
    return config['truck_launch_times']

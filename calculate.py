import info_sorting
from util import time_conversion

# Global Vars
hub_location = '4001 South 700 East'
truck_speed = 18.0
package_hash_map = info_sorting.get_package_map()
location_info = info_sorting.get_location_info()
location_names = location_info[0]
location_distances = location_info[1]

# Trucks are nested lists (Truck number - 1 = Truck index)
all_unsorted_trucks = info_sorting.get_unsorted_trucks()
# Nested lists to accommodate both distance and package id
all_sorted_trucks, all_truck_distances = [[], [], []], [[], [], []]
all_truck_launch_times = info_sorting.get_launch_times()


# Take an address name and return what ID it is from location_names
def id_from_address(address):
    for index, location in enumerate(location_names):
        if address in location[1]:
            return index


# Input 2 address IDs and retrieve the distance between them
# Since sometimes the response could be '' we need to flip them in order to get a value
def distance_between_addresses(address1, address2):
    distance = location_distances[address1][address2]
    # If looking up data retrieves nothing, switch order to obtain a value
    if distance == '':
        distance = location_distances[address2][address1]

    return distance


# After sorting make sure packages with a particular delivery time are placed first
# This is to ensure that the packages with a specific delivery time are delivered first
def move_priority_to_front(current_list):
    for j in current_list:
        current_package = package_hash_map.search(j)
        if current_package.priority:
            current_list.pop(current_list.index(j))
            current_list.insert(0, j)

    return current_list


# This adds a float distance in conjunction with the package id to a list
def calculate_final_distances(current_list):
    new_list = []

    for j in range(0, len(current_list)):
        package_initial = id_from_address(package_hash_map.search(current_list[j]).address)
        if j < len(current_list) - 1:
            package_travel = id_from_address(package_hash_map.search(current_list[j + 1]).address)
            distance_between = distance_between_addresses(package_initial, package_travel)
        else:
            # If at the final package in the list, then get the distance from package location to hub
            final_location_id = id_from_address(hub_location)
            distance_between = distance_between_addresses(package_initial, final_location_id)

        new_list.append([current_list[j], distance_between])

    # Add going from hub to the beginning of the list with a fake package id
    filler_package_id = -1
    start_location_id = id_from_address(hub_location)
    first_location_id = id_from_address(package_hash_map.search(current_list[0]).address)
    new_list.insert(0, [filler_package_id, distance_between_addresses(start_location_id, first_location_id)])

    return new_list


# This takes a truck launch time and sets every package's delivered, and launch time respectively
def calculate_package_deliveries(current_list, start):
    # Get time delta of truck launch time to work off of initially
    beg_time = time_conversion(start)

    for k in current_list:
        if k[0] != -1:
            current_package = package_hash_map.search(k[0])
            float_time = float(k[1])/truck_speed

            # Get time into the right format
            result = '{0:02.0f}:{1:02.0f}:{0:02.0f}'.format(*divmod(float_time * 60, 60))
            cur_time = time_conversion(result)

            # Add it on to the beginning time, use this to keep track of time of everything
            beg_time += cur_time

            # Update the package in the hashmap
            current_package.delivered_time = str(beg_time)
            current_package.launch_time = start
            package_hash_map.update(current_package.p_id, current_package)


# This adds up all float distances between locations made earlier
def get_total_distance_travelled():
    total_distance = 0
    for k in range(0, 2):
        for j in all_truck_distances[k]:
            total_distance += float(j[1])

    # Round it to remove floating point imprecision (Only to tenths place)
    return round(total_distance, 1)


# Greedy algorithm using recursive techniques
# The unsorted list is passed through and then is sorted and placed into
# all_sorted_trucks of the corresponding truck_index
def greedy_algo(current_list, current_package_id, truck_index):
    # Stop the whole algo if the list becomes empty
    if len(current_list) == 0:
        return

    # These will be used for comparison sake
    # Make sure no distance can be above lowest_distance initially
    lowest_distance = 10000.0
    lowest_distance_id = 0

    # This is for the initialization of the algorithm
    # This also finds the most optimal first package from the hub
    if current_package_id != 0:
        current_package = package_hash_map.search(current_package_id)
        current_location_id = id_from_address(current_package.address)
    else:
        current_location_id = 0

    for j in current_list:
        # This is an ID from the unsorted trucks
        new_package_id = j
        new_package = package_hash_map.search(new_package_id)
        new_location_id = id_from_address(new_package.address)
        distance_between = float(distance_between_addresses(int(current_location_id), int(new_location_id)))

        if distance_between < lowest_distance:
            lowest_distance = distance_between
            lowest_distance_id = new_package_id

    all_sorted_trucks[truck_index].append(lowest_distance_id)
    current_list.pop(current_list.index(lowest_distance_id))
    greedy_algo(current_list, lowest_distance_id, truck_index)


# This is so main.py can access the hash map
def get_package_hash_map():
    return package_hash_map


# Go through all unsorted trucks and sort them
# Then put priority packages at the front of each truck
# After that get distances between each package and add going to hub and returning to hub
# One of the final steps is to enumerate through each list and to set pack_delivered_time in package_hash_map
for i in range(0, len(all_unsorted_trucks)):
    greedy_algo(all_unsorted_trucks[i], 0, i)
    all_sorted_trucks[i] = move_priority_to_front(all_sorted_trucks[i])
    all_truck_distances[i] = calculate_final_distances(all_sorted_trucks[i])
    calculate_package_deliveries(all_truck_distances[i], all_truck_launch_times[i])

import calculate
from util import time_conversion


def start():
    print('[1] --- Print total mileage travelled by all trucks.')
    print('[2] --- Print package delivery information in a certain timeframe.')
    print('[3] --- Print package information based off package ID.')
    print('[4] --- Print package status based off package ID and a timeframe.')
    print('[5] --- Exit.')
    response_beginning = input('\nSelect an option. [INSERT NUMBER]   ')

    if response_beginning == '1':
        print(f'\nThe total distance travelled is {calculate.get_total_distance_travelled()} miles.\n')
    elif response_beginning == '2':
        timeframe_response()
    elif response_beginning == '3':
        information_response()
    elif response_beginning == '4':
        info_time_response()
    elif response_beginning == '5' or response_beginning == 'exit':
        exit()
    else:
        print('\nInput not recognized\n')
    print('----------------------------------------------\n')
    start()


# Receives an input from the user and searches the hash table for that id
def information_response():
    package_hash_map = calculate.get_package_hash_map()
    response_package_id = input('Input an ID to search. [INSERT NUMBER]   ')
    current_package = package_hash_map.search(response_package_id)

    if current_package is None:
        print('You have searched an invalid ID.')
    else:
        print_package_med(current_package)


# Receives a time from the user.  After it cycles through all the packages in the hash table and prints info about them
def timeframe_response():
    response_timeframe = input('\nInput a time to print delivery information of packages.\n'
                               'EXAMPLES [08:00:00] [13:00:00]\n'
                               'Please insert a time in 24h format. [INSERT TIME]   ')
    try:
        timeframe = time_conversion(response_timeframe)
        package_hash_map = calculate.get_package_hash_map()

        for i in range(1, 41):
            current_package = package_hash_map.search(str(i))
            package_launch = time_conversion(current_package.launch_time)
            package_delivered = time_conversion(current_package.delivered_time)

            status = package_status_string(timeframe, package_launch, package_delivered, current_package)
            print_package_sml(current_package, status)
        print('\n')
    except (IndexError, TypeError, ValueError):
        print('\nError, please ensure the values entered are correctly formatted.\n')


# Receives a time/id from the user.
# After it cycles through all the packages in the hash table and prints info about the package with the given id
def info_time_response():
    package_hash_map = calculate.get_package_hash_map()
    response_package_id = input('Input an ID to search. [INSERT NUMBER]   ')
    current_package = package_hash_map.search(response_package_id)

    if current_package is None:
        print('You have searched an invalid ID.')
    else:
        response_timeframe = input('\nInput a time to print delivery information of this package.\n'
                                   'EXAMPLES [08:00:00] [13:00:00]\n'
                                   'Please insert a time in 24h format. [INSERT TIME]   ')

        try:
            timeframe = time_conversion(response_timeframe)
            package_launch = time_conversion(current_package.launch_time)
            package_delivered = time_conversion(current_package.delivered_time)

            status = package_status_string(timeframe, package_launch, package_delivered, current_package)
            print_package_big(current_package, status)

        except(IndexError, TypeError, ValueError):
            print('\nError, please ensure the time entered is correctly formatted.\n')


# Creates a nicely formatted string based on time comparisons
def package_status_string(timeframe, package_delivered, package_launch, package):
    if timeframe < package_delivered:
        if timeframe > package_launch:
            return f'En route     (Left Hub at - {package.launch_time})'
        else:
            return f'Hub          (Leaving Hub at - {package.launch_time})'
    else:
        return f'Delivered    (Delivered at - {package.delivered_time})'


# Prints all information of a package
def print_package_big(package, status):
    print(f'\nID: {package.p_id}\n'
          f'Time Delivered: {package.delivered_time}\n'
          f'Address: {package.address, package.city, package.state, package.p_zip}\n'
          f'Mass: {package.mass}kg\n'
          f'Special Notes: {package.note}\n'
          f'Truck leave time: {package.launch_time}\n'
          f'Status: {status}\n')


# Prints most information of a package
def print_package_med(package):
    print(f'\nID: {package.p_id}\n'
          f'Time Delivered: {package.delivered_time}\n'
          f'Address: {package.address, package.city, package.state, package.p_zip}\n'
          f'Mass: {package.mass}kg\n'
          f'Special Notes: {package.note}\n')


# Prints very little information of a package
def print_package_sml(package, status):
    print(f'ID: {package.p_id}  Status: {status}')


if __name__ == '__main__':
    start()

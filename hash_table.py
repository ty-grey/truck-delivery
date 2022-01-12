class HashTable:

    # Initialize the hash table with an inputted capacity.
    def __init__(self, capacity=10):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Return a hash of the key given, this is abstracted to remove redundancy
    def __get_hashed_key(self, key):
        return hash(key) % len(self.table)

    # Insert a value into the hash table when given both a key and item
    def insert(self, key, value):
        bucket_list = self.table[self.__get_hashed_key(key)]

        key_value = [key, value]
        bucket_list.append(key_value)
        return

    # Update a value in the hash table when given a valid id and a new item
    def update(self, key, value):
        bucket_list = self.table[self.__get_hashed_key(key)]

        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = value
                return

    # Returns an item when a valid is given, if not nothing is returned
    def search(self, key):
        bucket_list = self.table[self.__get_hashed_key(key)]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]

        return None

    # Removes an item in the hash table when a valid id given
    def remove(self, key):
        bucket_list = self.table[self.__get_hashed_key(key)]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove(key_value[0])
                return

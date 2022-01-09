import os
import sys
import glob
import datetime

input_path = ''
output_path = ''
current_path = ''

MAX_STRING_LENGTH = 20
TYPESIZE = 220
PAGE_AMOUNT = 100
RECORD_AMOUNT = 32
FEATURE_AMOUNT = 10
FULL_PAGE_SIZE = 1672
FULL_RECORD_SIZE = 52
FILE_HEADER_SIZE = 8
PAGE_HEADER_SIZE = 8
RECORD_HEADER_SIZE = 12
FIRST_PART_PAGE_HEADER = 4
SECOND_PART_PAGE_HEADER = 4

def connect():
    '''
    - Returns the input and output file paths 
    from the command line interface arguments.
    '''
    args = sys.argv
    return (args[1], args[2])

def pathify():
    '''
    - Sets the input and output 
    file paths to the global variables.
    '''
    global input_path, output_path, current_path
    (input_path, output_path) = connect()
    pwd = os.getcwd()
    current_path = "."

def eventize():
    '''
    - Iterates over the input file and extracts
    discrete events that are running consecutively 
    and if any event returns a response, 
    it streams out the response to output file. 
    - Used guideline can be found in 
    project description, section 2: DDL & DML Tables
    '''
    global input_path
    input_file = open(input_path, "r")
    output_file = open(output_path, "w")
    for line in input_file:
        event_tokens = line.split(' ')
        event_tokens = strip(event_tokens)
        if event_tokens[0] == 'create':
            if event_tokens[1] == 'type':
                create_type(event_tokens[2:])
            if event_tokens[1] == 'record':
                create_record(event_tokens[2:])
        if event_tokens[0] == 'delete':
            if event_tokens[1] == 'type':
                delete_type(event_tokens[2:])
            if event_tokens[1] == 'record':
                delete_record(event_tokens[2:])
        if event_tokens[0] == 'list':
            if event_tokens[1] == 'type':
                type_list = list_type()
                for db_type in type_list:
                    output_file.write(db_type.rstrip()+'\n')
            if event_tokens[1] == 'record':
                record_list = list_record(event_tokens[2:])
                for record in record_list:
                    record_output = ''
                    for feature in record:
                        record_output += '{} '.format(feature)
                    output_file.write(record_output+'\n')
        if event_tokens[0] == 'update':
            if event_tokens[1] == 'record':
                update_record(event_tokens[2:])
        if event_tokens[0] == 'search':
            if event_tokens[1] == 'record':
                record = search_record(event_tokens[2:])
                if record:
                    record_output = ''
                    for feature in record:
                        record_output += '{} '.format(feature)
                    record_output.rstrip()
                    output_file.write(record_output+'\n')
        output_file.flush()
    output_file.close()

def strip(input_list):
    '''
    - Removes any trailing whitespaces from each token if any exists.
    Also removes any misclassified tokens. 
    '''
    stripped_tokens = []
    for token in input_list:
        if token == '':
            continue
        stripped_tokens.append(token.rstrip())
    return stripped_tokens

def construct_time():
    '''
    - Create a datetime format specialized for records in this project.
    Datetime format: YYYYMMDDHHmm
    YYYY: Year
    MM: Month
    DD: Day
    HH: Hour
    mm: Minute
    '''
    now = datetime.datetime.now()
    date_raw = datetime.datetime.date(now)
    time_raw = datetime.datetime.time(now)
    date = str(date_raw).split("-")
    time = str(time_raw).split(":")
    return '{}{}{}{}{}'.format(date[0], date[1], date[2], time[0], time[1])

def init_file(db_type, file_num):
    '''
    - Initialize a file for a type 
    that includes blank records.
    - Any update and create operation results 
    in changes in any of these files.
    - First code block is related to file header.
    - Second code block is related to page header.
    - Third code block is related to record header.
    '''
    # First Code Block
    record_file = open('./{}-{}.bin'.format(db_type, file_num), 'w+b')
    record_file.write('001'.encode("utf-8"))
    record_file.write('001'.encode("utf-8"))
    record_file.write('0'.encode("utf-8"))
    record_file.write('0'.encode("utf-8"))
    record_file.flush()
    # END OF First Code Block
    moment = construct_time()

    for page in range(0, PAGE_AMOUNT):
        # Second Code Block
        record_file.write('0'.encode("utf-8"))
        record_file.write('1'.encode("utf-8"))
        record_file.write('C'.encode("utf-8"))
        record_file.write('0'.encode("utf-8"))
        record_file.write('0000'.encode("utf-8"))
        # END OF Second Code Block

        for record in range(0, RECORD_AMOUNT):
            # Third Code Block
            record_file.write(moment.encode("utf-8"))
            # END OF Third Code Block

            for i in range(0, 10):
                record_file.write('----'.encode("utf-8"))

        record_file.flush()

    record_file.flush()
    record_file.close()

def format_file_num(file_num):
    '''
    - Formats the desired file number by addind leading zeros.
    If file number exceeds 10000, returns ValueError
    '''
    file_num = int(file_num)
    if file_num < 10:
        return '000{}'.format(int(file_num))
    elif file_num < 100:
        return '00{}'.format(int(file_num))
    elif file_num < 1000:
        return '0{}'.format(int(file_num))
    elif file_num < 10000:
        return '{}'.format(int(file_num))
    else:
        raise ValueError

def format_int(value):
    '''
    - Formats the desired value by addind leading zeros.
    - If file number exceeds 10000, returns ValueError.
    - It is exactly same with the previous one, but it is
    left if any patch is requested.
    '''
    value = int(value)
    if value < 10:
        return '000{}'.format(value)
    elif value < 100:
        return '00{}'.format(value)
    elif value < 1000:
        return '0{}'.format(value)
    elif value < 10000:
        return '{}'.format(value)
    else:
        raise ValueError

def find_page_head(primary_key):
    '''
    - Returns the position of page head in the current file,
    regarding the parameter 'primary_key'.
    - I have 100 pages per file, and 32 records per page.
    '''
    page_number = ((primary_key-1)/32)%100
    return FILE_HEADER_SIZE + int(page_number) * FULL_PAGE_SIZE

def find_record_head(primary_key):
    '''
    - Returns the position of record head in the current file,
    regarding the parameter 'primary_key'
    '''
    record_number = primary_key % 32
    if record_number == 0:
        record_number = record_number + 32
    return (record_number - 1) * FULL_RECORD_SIZE

def find_primary_key(primary_key):
    '''
    - Returns the position of an entry, regarding the parameter
    'primary_key'
    '''
    return primary_key % 32

def change_bit_value(pre_value, primary_key, setEmpty):
    '''
    - Sets the bit value in page header related 
    to the given 'primary_key'.
    - For the i^th position of a bit, it represents
    the i^th record space in the page.
    - Returns changed version of the previous value.
    - If illogical operations are requested,
    ValueError will be raised.
    '''
    byte_array = pre_value.decode("utf-8")
    char_order = int((int(primary_key) - 1) / 8)
    bit_order = int(primary_key % 8)
    changed_byte = byte_array[char_order]
    changed_byte_value = ord(changed_byte)
    bit_representation = "{0:b}".format(changed_byte_value)
    bit_representation = (8 - len(bit_representation)) * '0' + bit_representation
    if bit_representation[bit_order] == 1:
        raise ValueError
    if bit_representation[bit_order] == 0 and setEmpty:
        raise ValueError
    change_value = 2 ** bit_order
    if setEmpty:
        changed_byte_value = changed_byte_value - change_value
    changed_byte_value = changed_byte_value + change_value
    changed_byte = chr(changed_byte_value)
    byte_array = byte_array[0:char_order] + changed_byte + byte_array[char_order+1:]
    return byte_array.encode("utf-8")

def zero_check(input):
    '''
    - Returns the formatted value
    that is stripped from leading zeros.
    - If number is zero, returns just '0'.
    '''
    if input == '0000':
        return 0
    else:
        return input.lstrip('0')

def create_type(input):
    '''
    - Creates a type by adding typename and
    features into systemCatalog file.
    - Checks for any duplicate typenames.
    '''
    global current_path
    if not os.path.exists(current_path + '/systemCatalog'):
        catalog = open(current_path + '/systemCatalog', 'w+b')
        type_info = []

        type_name = input[0] + ((20 - len(input[0])) * ' ')
        if not type_name[0:len(input[0])].isalnum():
            raise ValueError

        type_info.append(type_name.encode("utf-8"))

        for type_feature in input[2:]:
            type_feature = type_feature + ((20 - len(type_feature)) * ' ')
            type_info.append(type_feature.encode("utf-8"))

        for dummy_feature in range(10 - len(input[2:])):
            type_info.append((20 * ' ').encode("utf-8"))

        for byte_token in type_info:
            catalog.write(byte_token)

        catalog.flush()
        catalog.close()
    else:
        catalog = open(current_path + '/systemCatalog', 'rb')
        current_types = []

        while True:
            db_type_b = catalog.read(TYPESIZE)
            if not db_type_b:
                break

            current_type_name = db_type_b[0:20].decode("utf-8")
            current_type_features = []

            for i in range(1, int(TYPESIZE/MAX_STRING_LENGTH)):
                current_type_features.append(db_type_b[(i*20):((i+1)*20)].decode("utf-8"))

            current_type = (current_type_name, current_type_features)
            current_types.append(current_type)

        catalog.close()

        new_type_name = input[0]
        if not new_type_name.isalnum():
            raise ValueError

        new_type_features = []
        for (type_name, type_features) in current_types:
            stripped = type_name.rstrip()
            if stripped == new_type_name:
                raise ValueError

        new_type_name = new_type_name + ((20 - len(new_type_name)) * ' ')
        for feature in input[2:]:
            new_type_feature = feature + ((20 - len(feature)) * ' ')
            new_type_features.append(new_type_feature)

        for dummy_feature in range(10 - len(input[2:])):
            new_type_features.append((20 * ' '))

        new_type = (new_type_name, new_type_features)
        current_types.append(new_type)

        current_types.sort(key=lambda tup: tup[0]) # Sorted ascending order

        final_type_list = []
        for i, (type_name, type_features) in enumerate(current_types):
            pre_byte_type = []
            pre_byte_type.append(type_name.encode("utf-8"))
            for feature in type_features:
                pre_byte_type.append(feature.encode("utf-8"))
            final_type_list.append(pre_byte_type)

        os.remove(current_path + '/systemCatalog') # removes the old version
        catalog = open(current_path + '/systemCatalog', 'wb') # creates the new version

        for byte_type in final_type_list:
            for byte_token in byte_type:
                catalog.write(byte_token)

        catalog.flush()
        catalog.close()

def delete_type(input):
    '''
    - Deletes a type by 'type_name' given
    as 'input'.
    - Removes any record files regarding
    the deleted_type.
    '''
    deleted_type_name = input[0].rstrip()
    type_list = []

    catalog = open(current_path + '/systemCatalog', 'rb')
    while True:
        db_type_b = catalog.read(TYPESIZE)
        if not db_type_b:
            break

        current_type_name = db_type_b[0:20].decode("utf-8")
        current_type_features = []

        for i in range(1, int(TYPESIZE/MAX_STRING_LENGTH)):
            current_type_feature = db_type_b[(i*20):(20+(i*20))].decode("utf-8")
            current_type_features.append(current_type_feature)

        current_type = (current_type_name, current_type_features)
        type_list.append(current_type)
    catalog.close()

    for (type_name, type_features) in type_list:
        if type_name.rstrip() == deleted_type_name:
            type_list.remove((type_name, type_features))
            break

    os.remove(current_path + '/systemCatalog')
    catalog = open(current_path + '/systemCatalog', 'wb')
    for (type_name, type_features) in type_list:
        catalog.write(type_name.encode("utf-8"))
        for feature in type_features:
            catalog.write(feature.encode("utf-8"))
        catalog.flush()
    catalog.close()

    type_occurences = glob.glob('./{}-[0-9][0-9][0-9][0-9].bin'.format(deleted_type_name))
    for occurence in type_occurences:
        os.remove(occurence)

def list_type():
    '''
    - Lists any type name resides in
    systemCatalog file.
    '''
    global current_path
    catalog = open(current_path + '/systemCatalog', 'rb')
    type_list = []

    while True:
        db_type_b = catalog.read(TYPESIZE)

        if not db_type_b:
            break

        db_type_name = db_type_b[0:20].decode("utf-8")
        db_type_name.rstrip()

        type_list.append(db_type_name)
    catalog.close()
    return type_list

def create_record(input):
    '''
    - Creates a record with the given type_name.
    - Moves the cursor in the file,
    via file.seek() method.
    - All positions are precalculated,
    since it is not built as a dynamic
    database.
    '''
    db_type = input[0]
    primary_key = int(input[1])
    file_num = format_file_num(int((primary_key-1)/3200) + 1)

    occurences = glob.glob('./{}-{}.bin'.format(db_type, file_num))
    if not occurences:
        init_file(db_type, file_num)

    type_file = open('./{}-{}.bin'.format(db_type, file_num), 'r+b')
    offset = find_page_head(primary_key)
    type_file.seek(offset + FIRST_PART_PAGE_HEADER)
    record_list = type_file.read(SECOND_PART_PAGE_HEADER)
    type_file.seek(-SECOND_PART_PAGE_HEADER, 1)
    type_file.write(change_bit_value(record_list, find_primary_key(primary_key), False))
    type_file.seek(find_record_head(primary_key), 1)
    type_file.write(construct_time().encode("utf-8"))
    for feature in input[1:]:
        type_file.write(format_int(feature).encode("utf-8"))
    type_file.flush()
    type_file.close()

def delete_record(input):
    '''
    - Deletes a record with the given 'primary_key'.
    - Moves the cursor as explained above.
    - Replaces the data with 'dash' ('-') to represent the null.
    - Keeps the volume size constant
    - No dynamic data manipulation., 
    '''
    db_type = input[0]
    primary_key = int(input[1])

    file_num = format_file_num(int((primary_key-1)/3200) + 1)    
    type_file = open('./{}-{}.bin'.format(db_type, file_num), 'r+b')
    offset = find_page_head(primary_key)
    type_file.seek(offset + FIRST_PART_PAGE_HEADER)
    record_list = type_file.read(SECOND_PART_PAGE_HEADER)
    type_file.seek(-SECOND_PART_PAGE_HEADER, 1)
    type_file.write(change_bit_value(record_list, find_primary_key(primary_key), True))
    type_file.seek(find_record_head(primary_key), 1)
    type_file.write(construct_time().encode("utf-8"))
    for i in range(0, 10):
        type_file.write('----'.encode("utf-8"))
    type_file.flush()
    type_file.close()

def update_record(input):
    '''
    - Updates a record with the given 'primary_key'.
    - Moves the cursor as explained above.
    - Replaces the data with the given values in parameter 'input'.
    '''
    db_type = input[0]
    primary_key = int(input[1])

    file_num = format_file_num(int((primary_key-1)/3200) + 1)    
    type_file = open('./{}-{}.bin'.format(db_type, file_num), 'r+b')
    offset = find_page_head(primary_key)
    type_file.seek(offset + FIRST_PART_PAGE_HEADER)
    record_list = type_file.read(SECOND_PART_PAGE_HEADER)
    type_file.seek(-SECOND_PART_PAGE_HEADER, 1)
    type_file.write(change_bit_value(record_list, find_primary_key(primary_key), False))
    type_file.seek(find_record_head(primary_key), 1)
    type_file.write(construct_time().encode("utf-8"))
    type_file.write(format_int(primary_key).encode("utf-8"))
    for feature in input[2:]:
        type_file.write(format_int(feature).encode("utf-8"))
    type_file.flush()
    type_file.close()

def search_record(input):
    '''
    - Searchs a record with the given 'primary_key'.
    - Moves the cursor as explained above.
    - Prints out the data of the requested record.
    '''
    db_type = input[0]
    primary_key = int(input[1])

    file_num = format_file_num(int((primary_key-1)/3200) + 1)
    if not os.path.exists('./{}-{}.bin'.format(db_type, file_num)):
        return

    type_file = open('./{}-{}.bin'.format(db_type, file_num), 'r+b')
    offset = find_page_head(primary_key) + PAGE_HEADER_SIZE + find_record_head(primary_key)
    type_file.seek(offset)
    moment = construct_time()
    type_file.write(moment.encode("utf-8"))
    record_features = []
    
    for i in range(0, 10):
        feature = type_file.read(4)
        feature_decoded = feature.decode("utf-8")
        if feature_decoded != '----':
            record_features.append(feature_decoded.lstrip('0'))
    type_file.close()

    return record_features

def list_record(input):
    '''
    - Lists all records for a given 
    type_name, as parameter 'input'.
    - Checks every file related to the given type_name.
    - Reads page by page in files.
    - 'r_index' is record index from 0 to 31.
    - 'f_index' is feature index from 0 t0 9.
    '''
    db_type = input[0]
    occurences = glob.glob('./{}-[0-9][0-9][0-9][0-9].bin'.format(db_type))

    record_list = []
    for file_name in occurences:
        type_file = open(file_name, 'r+b')
        type_file.seek(FILE_HEADER_SIZE)
        for page in range(0, PAGE_AMOUNT):
            page_data = type_file.read(FULL_PAGE_SIZE)
            index = PAGE_HEADER_SIZE
            for r_index in range(0, RECORD_AMOUNT):
                record_byte = page_data[index+r_index*FULL_RECORD_SIZE:index+(r_index+1)*FULL_RECORD_SIZE]
                record = record_byte.decode("utf-8")
                record_obj = []
                if record[12:16] != '----':
                    for f_index in range(0, 10):
                        feature = record[12+(4*f_index):12+(4*(f_index+1))]
                        if feature != '----':
                            record_obj.append(zero_check(feature))
                if record_obj:
                    record_list.append(record_obj)
        type_file.close()

    return record_list

if __name__ == '__main__':
    '''
    - Initializes the project,
    kind of a form of
    'main' in C and Java.
    '''
    pathify()
    eventize()

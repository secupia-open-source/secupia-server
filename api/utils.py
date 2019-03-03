def validate_vehicle_log_data(data):
    try:
        license_plate = data['license_plate']
        is_entry = data['is_entry']
    except KeyError:
        raise ValueError("Field missing")
    if not isinstance(is_entry, bool):
        raise ValueError
    return license_plate, is_entry

def validate_guest_visit_data(data):
    '''Return validated Guest visit data'''
    try:
        name = data['name']
        contact = int(data['contact'])
        # expected_date_time = datetime(data['expected_date_time'])
        purpose = data['purpose']
    except KeyError:
        raise ValueError('Fields missing')
    return data

def validate_update_vehicle_data(data):
    '''Return validated data to update guest's vehicle'''
    try:
        name = data['license_plate']
        contact = int(data['guest_id'])
    except KeyError:
        raise ValueError('Fields missing')
    return data

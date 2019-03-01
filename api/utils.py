def validate_vehicle_log_data(data):
	license_plate = data['license_plate']
	is_entry = data['is_entry']
	if not isinstance(is_entry, bool):
		raise ValueError
	return license_plate, is_entry

def validate_guest_visit_data(data):
	'''Return validated Guest visit data'''
	name = data['name']
	# email = data['email']
	# gender = data['gender']
	contact = int(data['contact'])
	# dob = ['dob']
	# occupation = ['occupation']
	# license_num = data['license_num']

	purpose = data['purpose']

	guest_data = {
		"name": name,
		"contact": contact
	}

	visit_data = {
		"purpose": purpose
	}

	return guest_data, visit_data
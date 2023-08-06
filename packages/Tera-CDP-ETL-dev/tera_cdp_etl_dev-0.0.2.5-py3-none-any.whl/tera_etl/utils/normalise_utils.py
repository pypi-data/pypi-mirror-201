import string
import pandas
import re


def assign_to_event(event_object, key, value) -> any:
	if pandas.isna(value) or not value:
		return None
	
	if isinstance(value, str):
		event_object[key] = value[:127]
	else:
		event_object[key] = value
	return value


def clean_email_field(email: str) -> string:
	if pandas.isna(email):
		return None
	if not email or 'vtvcab@vtvcab.vn' == email:
		return None
	# Regex is not efficiency
	email_pattern = r'(\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+)'
	searched_result = re.search(email_pattern, email)
	return searched_result.group() if searched_result else None


def clean_phone_field(phone_str: str) -> str:
	"""
		Output phone format: 84xxxx
	"""
	if pandas.isna(phone_str) or not phone_str:
		return None

	# Regex is not efficiency
	# Sometimes we even find note in the phone number field.
	phone_regex = r'(\d+)'
	phone = ''.join(re.findall(phone_regex, phone_str))
	
	p_length = len(phone)

	if p_length == 9:
		phone = '0' + phone
		p_length += 1
	
	# Too short to be a phone
	if p_length < 10:
		return None
	# Too long, possibly a text
	if p_length > 16:
		return None
	
	country_code = '84'
	
	if phone.startswith('00840'):
		phone = f'{phone[4:]}'
	elif phone.startswith('0840'):
		phone = f'{phone[3:]}'
	elif phone.startswith('840'):
		phone = f'{phone[2:]}'
	elif phone.startswith('84') and p_length >= 11:
		phone = f'0{phone[2:]}'
	elif not phone.startswith('0') and p_length == 10:
		phone = f'0{phone}'
	
	p_length = len(phone)
	processed_phone = ''
	if p_length == 10:
		processed_phone = f'{phone[1:]}'
	elif p_length == 11:
		processed_phone = f'{__convert_old_phone(phone)}'
	
	if processed_phone.startswith('0'):
		processed_phone = processed_phone[1:]
	
	return f'{country_code}{processed_phone}' if len(processed_phone) >= 9 else ''


def __convert_old_phone(phone_number) -> string:
	phone_prefix_map = {
		'0162': '32',
		'0163': '33',
		'0164': '34',
		'0165': '35',
		'0166': '36',
		'0167': '37',
		'0168': '38',
		'0169': '39',
		'0120': '70',
		'0121': '79',
		'0122': '77',
		'0126': '76',
		'0128': '78',
		'0123': '83',
		'0124': '84',
		'0125': '85',
		'0127': '81',
		'0129': '82',
		'0186': '56',
		'0188': '58',
		'0199': '59'
	}
	for k, v in phone_prefix_map.items():
		if phone_number.startswith(k):
			return phone_number.replace(k, v, 1)
	return phone_number

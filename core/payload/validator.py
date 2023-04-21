import re


class Patterns(object):
	def __init__(self):
		self._ids = [
			re.compile(r'(?=.*[^\w\s]).*'),
			re.compile(r'(?=.*[ㄱ-힣]).*')
		]
		self._password = None
		self._car_identifiers = [
			re.compile(r'^\d{2,3}[가-힣]{1}\d{4}$'),
			re.compile(r'^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$'),
		]
		self._mobile = re.compile('\d{11}$')

	@property
	def mobile(self):
		return self._mobile

	@property
	def usernames(self):
		return self._ids

	@property
	def password(self):
		return self._password

	@property
	def cars(self):
		return self._car_identifiers


patterns = Patterns()


def IDRules(value):
	if value:
		if value == 'dev':
			return True
		if len(value) > 20 or len(value) < 4:
			return False
		for username in patterns.usernames:
			if username.match(value):
				return False
		if value.__contains__(' '):
			return False

	else:
		return False

	return True


def PasswordRules(value, repeat):
	if value and repeat:
		if value != repeat:
			return False
		elif len(value) > 20 or len(value) < 4:
			return False
		elif value.__contains__(' '):
			return False
	else:
		return False

	return True


def CarIdentifierRules(value):
	for regex in patterns.cars:
		if regex.match(value):
			return True
	return False


def MobileNumberRules(value:str):
	length = len(value)
	if length == 11:
		if not patterns.mobile.match(value):
			return False
		else:
			# top = value[:4]
			# mid = value[4:8]
			# btm = value[8:]
			# nums = "{}-{}-{}".format(top, mid, btm)
			return True
	else:
		return False

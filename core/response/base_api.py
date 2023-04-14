from datetime import datetime

from django.http import JsonResponse


def now():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class APIResponseSpecification(object):
	init = False
	_data = dict()

	def __init__(self):
		self.init = False
		self._data = {
			"result_code": None,
			"result_msg": None,
			"result_date": None
		}

	def __str__(self):
		return self._data

	@property
	def _message_properties(self):
		return {
			-7: "Apple auth failed",
			-6: "NICE Auth Server error",
			-5: "SMTP Server error",
			-4: "Device authentication failed",
			-3: "Expired authorize token",
			-2: "Access denied",
			-1: "CSRF token is not vaild",

			1: "Success",
			2: "Success(duplicated)",
			3: "The result does not exists",

			11: "Invalid parameters",
			12: "Already exists",
			13: "Violates the ID rules",
			14: "Violates the Password rules",
			15: "Violates the QR Code rules",
			16: "Invalid car-number",
			17: "Identity verification failed",
			18: "Repeat password is not valid",
			19: "Point Insufficient",
			20: "Point limit exceeded",
			21: "FCM messaging failed",
			22: "No available for 3 consecutive days",
			23: "Already exists car number",

		}

	def json_response(self):
		return JsonResponse(self.to_dict())

	def to_dict(self):
		if self.init == False:
			self._data.update({"result_code": -9999})
			self._data.update({"result_msg": "Unknown response message, Response need to setup"})
			self._data.update({"result_date": now()})
			return self._data
		else:
			return self._data

	def update(self, options:dict):
		for k, v in options.items():
			self._data.update({k: v})
		return self

	def setup(self, code, msg=None, rdate=now()):
		if self.init == False:
			try:
				if not msg:
					self._data.update({"result_msg": self._message_properties.get(int(code))})
				else:
					self._data.update({"result_msg": msg})

			except:
				self._data.update({"result_msg": msg})

			self._data.update({"result_code": code})
			self._data.update({"result_date": rdate})
			self.init = True

		return self

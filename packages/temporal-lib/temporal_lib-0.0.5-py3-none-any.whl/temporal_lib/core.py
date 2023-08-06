""" __init__.py for module 'core' """

# Module Typing: https://docs.python.org/3.8/library/typing.html#module-typing


# Third Party
# import dateutil.parser  # https://stackoverflow.com/questions/48632176/python-dateutil-attributeerror-module-dateutil-has-no-attribute-parse
# from dateutil.relativedelta import relativedelta
# from dateutil.rrule import SU, MO, TU, WE, TH, FR, SA  # noqa F401


from datetime import (
	date as DateType,
	datetime as DateTimeType,
	timedelta
)
from typing import Generator


# Third Party
import tzlocal
import pytz_deprecation_shim as pds
from pytz_deprecation_shim._impl import _PytzShimTimezone

# Temporal - Only import specific functions and constants; avoid circular references.
from temporal_lib.tlib_types import (
	any_to_date,
	datestr_to_date,
	validate_datatype,
	UTC, EPOCH_START_DATE, EPOCH_END_DATE
)

# --------
# Time Zones
# --------
class TimeZone(_PytzShimTimezone):
	"""
	Wrapper for the _PytzShimTimezone, which itself is a wrapper around tzinfo
	"""

	@staticmethod
	def get_local():
		return TimeZone(tzlocal.get_localzone())

	def __init__(self, timezone: object):
		if isinstance(timezone, str):
			timezone_obj = pds.timezone(timezone)  # Could be pytz, could be ZoneInfo
		else:
			timezone_obj = timezone
		super().__init__(timezone_obj, timezone_obj)  # no idea what to do about this "key"

		self._timezone = timezone_obj
		if not self._timezone:
			raise ValueError("Unable to initialize TimeZone class.")

	def ambiguous_name(self, as_of_datetime=None):
		"""
		WARNING: This particular "name" of a Time Zone is fluid.
		For example, "America/New_York" is EST in the winter and EDT in the summer.
		"""
		if not as_of_datetime:
			# as_of_datetime = DateTimeType.now(UTC)
			as_of_datetime = DateTimeType.now()
		return self._timezone.tzname(as_of_datetime)  # _PytzShimTimezone.tzname(dt)

	def iana_name(self):
		# For IANA time zones, calling str() on the shim zones (and indeed on pytz and zoneinfo zones as well) returns the IANA 'key'
		return str(self._timezone)


# --------
# Current System Time
# --------

def get_system_datetime_now(time_zone=None):
	"""
	Return the current DateTime in the system's local Time Zone.
	"""
	time_zone = time_zone or TimeZone.get_local()
	utc_datetime = DateTimeType.now(UTC)
	return utc_datetime.astimezone(time_zone)  # convert UTC to local zone


def get_system_date(time_zone=None):
	return get_system_datetime_now(time_zone).date()

# --------
# UTC
# --------

def get_utc_datetime_now():
	return DateTimeType.now(UTC)

def is_datetime_naive(any_datetime):
	"""
	Returns True if the datetime is missing a Time Zone component.
	"""
	if not isinstance(any_datetime, DateTimeType):
		raise TypeError("Argument 'any_datetime' must be a Python datetime object.")

	if any_datetime.tzinfo is None:
		return True
	return False


def make_datetime_naive(any_datetime):
	"""
	Takes a timezone-aware datetime, and makes it naive.
	"""
	return any_datetime.replace(tzinfo=None)

def localize_datetime(any_datetime, any_timezone):
	"""
	Given a naive datetime and time zone, return the localized datetime.

	Necessary because Python is -extremely- confusing when it comes to datetime + timezone.
	"""
	if not isinstance(any_datetime, DateTimeType):
		raise TypeError("Argument 'any_datetime' must be a Python datetime object.")

	if any_datetime.tzinfo:
		raise TypeError(f"Datetime value {any_datetime} is already localized and time zone aware (tzinfo={any_datetime.tzinfo})")

	# What kind of time zone object was passed?
	type_name = type(any_timezone).__name__

	# WARNING: DO NOT USE:  naive_datetime.astimezone(timezone).  This implicitly shifts you the UTC offset.
	if type_name == 'ZoneInfo':
		# Only available in Python 3.9+
		return any_datetime.replace(tzinfo=any_timezone)
	# Python 3.8 or earlier
	return any_timezone.localize(any_datetime)


def date_is_between(any_date, start_date, end_date, use_epochs=True):
	"""
	Returns a boolean if a date is between 2 other dates.
	The interesting part is the epoch date substitution.
	"""
	if (not use_epochs) and (not start_date):
		raise ValueError("Function 'date_is_between' cannot resolve Start Date = None, without 'use_epochs' argument.")
	if (not use_epochs) and (not end_date):
		raise ValueError("Function 'date_is_between' cannot resolve End Date = None, without 'use_epochs' argument.")

	if not start_date:
		start_date = EPOCH_START_DATE
	if not end_date:
		end_date = EPOCH_END_DATE

	any_date = any_to_date(any_date)
	start_date = any_to_date(start_date)
	end_date = any_to_date(end_date)

	return bool(start_date <= any_date <= end_date)

def date_range(start_date, end_date) -> Generator:
	"""
	Generator for an inclusive range of dates.
	It's very weird this isn't part of Python Standard Library or datetime  :/
	"""

	# Convert from Strings to Dates, if necessary.
	start_date = any_to_date(start_date)
	end_date = any_to_date(end_date)
	# Important to add +1, otherwise the range is -not- inclusive.
	for number_of_days in range(int((end_date - start_date).days) + 1):
		yield start_date + timedelta(number_of_days)

def date_range_from_strdates(start_date_str, end_date_str):
	""" Generator for an inclusive range of date-strings. """
	if not isinstance(start_date_str, str):
		raise TypeError("Argument 'start_date_str' must be a Python string.")
	if not isinstance(end_date_str, str):
		raise TypeError("Argument 'end_date_str' must be a Python string.")
	start_date = datestr_to_date(start_date_str)
	end_date = datestr_to_date(end_date_str)
	return date_range(start_date, end_date)

def date_generator_type_1(start_date, increments_of, earliest_result_date):
	"""
	Given a start date, increment N number of days.
	First result can be no earlier than 'earliest_result_date'
	"""
	iterations = 0
	next_date = start_date
	while True:
		iterations += 1
		if (iterations == 1) and (start_date == earliest_result_date):  # On First Iteration, if dates match, yield Start Date.
			yield start_date
		else:
			next_date = next_date + timedelta(days=increments_of)
			if next_date >= earliest_result_date:
				yield next_date

def calc_future_dates(epoch_date, multiple_of_days, earliest_result_date, qty_of_result_dates):
	"""
		Purpose: Predict future dates, based on an epoch date and multiple.
		Returns: A List of Dates

		Arguments
		epoch_date:           The date from which the calculation begins.
		multiple_of_days:     In every iteration, how many days do we move forward?
		no_earlier_than:      What is earliest result date we want to see?
		qty_of_result_dates:  How many qualifying dates should this function return?
	"""
	validate_datatype('epoch_date', epoch_date, DateType, True)
	validate_datatype('earliest_result_date', earliest_result_date, DateType, True)

	# Convert to dates, always.
	epoch_date = any_to_date(epoch_date)
	earliest_result_date = any_to_date(earliest_result_date)
	# Validate the remaining data types.
	validate_datatype("multiple_of_days", multiple_of_days, int)
	validate_datatype("qty_of_result_dates", qty_of_result_dates, int)

	if earliest_result_date < epoch_date:
		raise ValueError(f"Earliest_result_date '{earliest_result_date}' cannot precede the epoch date ({epoch_date})")

	this_generator = date_generator_type_1(epoch_date, multiple_of_days, earliest_result_date)
	ret = []
	for _ in range(qty_of_result_dates):  # underscore because we don't actually need the index.
		ret.append(next(this_generator))
	return ret


def get_earliest_date(list_of_dates):
	if not all(isinstance(x, DateType) for x in list_of_dates):
		raise ValueError("All values in argument must be datetime dates.")
	return min(list_of_dates)

def get_latest_date(list_of_dates):
	if not all(isinstance(x, DateType) for x in list_of_dates):
		raise ValueError("All values in argument must be datetime dates.")
	return max(list_of_dates)

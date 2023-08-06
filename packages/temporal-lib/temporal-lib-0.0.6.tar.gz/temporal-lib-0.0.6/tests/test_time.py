#!/bin/python

from datetime import time
from temporal_lib.tlib_types import timestr_to_time

def test_string_to_time():

	time_string = "1AM"
	expected_time = time(1, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "2PM"
	expected_time = time(14, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "13"
	expected_time = time(13, 0, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "1:30AM"
	expected_time = time(1, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "1:30PM"
	expected_time = time(13, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "12:30PM"
	expected_time = time(12, 30, 0)
	assert timestr_to_time(time_string) == expected_time

	time_string = "12:30PM"
	expected_time = time(12, 30, 0)
	assert timestr_to_time(time_string) == expected_time

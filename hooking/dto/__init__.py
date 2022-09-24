"""Data Transfer Object module"""
from collections import namedtuple


Context = namedtuple("Context", ["h", "hid", "event", "spec", "accept_input"])

HookInfo = namedtuple("HookInfo", ["hid", "event", "spec", "accept_input"])

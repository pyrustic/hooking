"""Data Transfer Object"""
from collections import namedtuple

# these namedtuples are used by the hooking.H class to store information
# in its class variables
HookInfo = namedtuple("HookInfo", ["cls", "hid", "hook", "tag", "spec"])
TargetInfo = namedtuple("TargetInfo", ["cls", "tag", "target", "config"])

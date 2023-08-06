"""

    This is the net tracer package main file.

    When import from `net-tracer` package usually you need to specify the module but we skip that by importing all functions from the modules here.

"""

# from module import functions
from .scan import * # tracer 
from .dns import *  # resolve_domain, query_record, reverse_lookup, zone_transfer, cache_lookup, spoofing_detection, dnssec_validation

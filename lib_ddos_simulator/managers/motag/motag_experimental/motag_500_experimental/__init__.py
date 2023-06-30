#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This folder contains all the motag managers for DDOS simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .motag_manager_500_bucket_combine_diff_start import Motag_Manager_500_Bucket_Combine_Diff_Start
from .motag_manager_500_bucket_no_combine_diff_start import Motag_Manager_500_Bucket_No_Combine_Diff_Start
from .motag_manager_500_bucket_no_combine_normal_start import Motag_Manager_500_Bucket_No_Combine_Normal_Start
from .motag_manager_500_invalid import Motag_Manager_500_Bucket_Invalid

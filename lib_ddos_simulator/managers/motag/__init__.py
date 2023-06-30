#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This folder contains all the motag managers for DDOS simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .motag_manager_3_bucket import Motag_Manager_3_Bucket
from .motag_manager_20_bucket import Motag_Manager_20_Bucket
from .motag_manager_40_bucket import Motag_Manager_40_Bucket
from .motag_manager_200_bucket import Motag_Manager_200_Bucket
from .motag_manager_500_bucket import Motag_Manager_500_Bucket


# Experiments
from .motag_experimental import Motag_Manager_40_Bucket_Combine_Diff_Start
from .motag_experimental import Motag_Manager_40_Bucket_No_Combine_Diff_Start
from .motag_experimental import Motag_Manager_40_Bucket_No_Combine_Normal_Start
from .motag_experimental import Motag_Manager_40_Bucket_No_Combine_Normal_Start_Unlimited
from .motag_experimental import Motag_Manager_40_Bucket_Invalid
#500
from .motag_experimental import Motag_Manager_500_Bucket_Combine_Diff_Start
from .motag_experimental import Motag_Manager_500_Bucket_No_Combine_Diff_Start
from .motag_experimental import Motag_Manager_500_Bucket_No_Combine_Normal_Start
from .motag_experimental import Motag_Manager_500_Bucket_No_Combine_Normal_Start_Unlimited
from .motag_experimental import Motag_Manager_500_Bucket_Invalid

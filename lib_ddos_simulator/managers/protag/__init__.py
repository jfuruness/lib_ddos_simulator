#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This folder contains all the protag managers for DDOS simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .protag_manager_base import Protag_Manager_Base
from .protag_manager_merge import Protag_Manager_Merge
from .protag_manager_no_merge import Protag_Manager_No_Merge
from .protag_manager_smart_merge import Protag_Manager_Smart_Merge
from .protag_manager_smart_merge_conservative import Protag_Manager_Smart_Merge_Conservative
from .protag_manager_smart_merge_3 import Protag_Manager_Smart_Merge_3
from .protag_manager_smart_merge_conservative_3 import Protag_Manager_Smart_Merge_Conservative_3

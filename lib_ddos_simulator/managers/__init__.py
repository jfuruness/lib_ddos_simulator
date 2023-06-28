#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This folder contains all the managers for DDOS simulation"""

__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com, agorbenko97@gmail.com"
__status__ = "Development"

from .bounded_manager import Bounded_Manager
from .dose import DOSE_Manager, DOSE_Attack_Event
from .motag import Motag_Manager_3_Bucket
from .motag import Motag_Manager_20_Bucket
from .motag import Motag_Manager_40_Bucket
from .motag import Motag_Manager_40_Bucket_Invalid
from .motag import Motag_Manager_200_Bucket
from .motag import Motag_Manager_500_Bucket
from .opt_s import Opt_S
from .protag import Protag_Manager_Base
from .protag import Protag_Manager_Merge
from .protag import Protag_Manager_No_Merge
from .protag import Isolator_2i_1f
from .protag import Isolator_3i_1f
from .protag import Isolator_2i_kf
from .protag import Isolator_3i_kf
from .protag import Isolator_2i_SQRT_kf
from .protag import Isolator_3i_SQRT_kf
from .protag import Opt_H


from .sieve import Sieve_Manager_V0_S0, Sieve_Manager_V0_S1, Sieve_Manager_V0_S2
from .sieve import Sieve_Manager_V0_W_Stop_S0
from .sieve import Sieve_Manager_V0_W_Stop_S1
from .sieve import Sieve_Manager_V0_W_Stop_S2
from .sieve import Sieve_Manager_V1_S0, Sieve_Manager_V1_S1, Sieve_Manager_V1_S2
from .sieve import Sieve_Manager_KPO_S0, Sieve_Manager_KPO_S1, Sieve_Manager_KPO_S2
from .sieve import Sieve_Manager_Base

# Done here to force init
from .manager import Manager

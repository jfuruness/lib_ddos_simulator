from pathlib import Path

from lib_ddos_simulator import DDOS_Simulator, Basic_Attacker
from lib_ddos_simulator import Motag_Manager_40_Bucket
from lib_ddos_simulator import Protag_Manager_Merge

# Parameters to change for the animations
############################################################
num_users = 100
num_attackers = int(num_users * .1)
num_buckets = 1
num_rounds = 10
# All the managers to run. See manager section for a list
manager_child_classes = [
    # Protag_Manager_Merge,
    Motag_Manager_40_Bucket
]
# The type of attacker. See attacker section for a list
attacker_cls = Basic_Attacker
############################################################

# Not necessary to change below this line for typical use

sim = DDOS_Simulator(
    # Options to change above
    num_users=num_users,
    num_attackers=num_attackers,
    num_buckets=num_buckets,
    Manager_Child_Classes=manager_child_classes,
    attacker_cls=attacker_cls,
    # Not necessary to change for animations
    graph_dir=str(Path("~/Desktop/ddos_anim").expanduser()),
    save=True,
    high_res=False
)
sim.run(num_rounds, animate=True, graph_trials=False)

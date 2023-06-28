import cProfile, pstats, io
from pathlib import Path

from lib_ddos_simulator import DDOS_Simulator, Protag_Manager_Merge, Basic_Attacker

# Parameters to change for the animations
############################################################
num_users = 10
num_attackers = 1
num_buckets = 1
num_rounds = 5
# All the managers to run. See manager section for a list
manager_child_classes = [Protag_Manager_Merge]
# The type of attacker. See attacker section for a list
attacker_cls = Basic_Attacker
############################################################

# Not necessary to change below this line for typical use

def main():
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

# Profiling starts here
pr = cProfile.Profile()
pr.enable()
main()  # run the main function
pr.disable()

# Save profiling stats into a text file
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()

with Path('~/Desktop/profiling_output.txt').expanduser().open('w') as f:
    f.write(s.getvalue())

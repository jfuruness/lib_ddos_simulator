from lib_ddos_simulator import DDOS_Simulator, Protag_Manager_Merge, Basic_Attacker
num_users = 10
num_attackers = 1
num_buckets = 5
# All the managers to run. See manager section for a list
manager_child_classes = [Protag_Manager_Merge]
# The following options are the defaults, you can omit
# these or change them if you wish
graph_dir = "/tmp/lib_ddos_simulator"
# The type of attacker. See attacker section for a list
attacker_cls = Basic_Attacker
sim = DDOS_Simulator(num_users,
                     num_attackers,
                     num_buckets,
                     manager_child_classes,
                     graph_dir=graph_dir,
                     attacker_cls=attacker_cls,
                     save=True,
                     high_res=False)
# Num rounds can be changed as needed
num_rounds = 3
sim.run(num_rounds, animate=True, graph_trials=False)

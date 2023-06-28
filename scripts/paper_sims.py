from lib_ddos_simulator import (
    Combination_Grapher,
    Protag_Manager_Merge,
    Protag_Manager_No_Merge,Motag_Manager_40_Bucket,
    Motag_Manager_500_Bucket,
    Isolator_2i_1f,
    Isolator_2i_kf,
    Isolator_3i_1f,
    Isolator_3i_kf,
    Isolator_2i_SQRT_kf,
    Isolator_3i_SQRT_kf,
    Opt_H,
    Opt_S,
    Attacker
)
from lib_ddos_simulator.attackers import (
    Basic_Attacker,
    Even_Turn_Attacker,
    Herzberg_Motag_Attacker,  # All but one attacker
    Never_Alone_Attacker,
    Never_Last_Attacker,
    Log2n_Turns_Straight_Attacker
)

managers=[
    Protag_Manager_Merge,
    # Protag_Manager_No_Merge,
    Motag_Manager_40_Bucket,
    Motag_Manager_500_Bucket,
    Isolator_2i_1f,
    # Isolator_2i_kf,
    # Isolator_3i_1f,
    Isolator_3i_kf,
    # Isolator_2i_SQRT_kf,
    # Isolator_3i_SQRT_kf,
    Opt_S,
    Opt_H,
]

attackers = [
    Basic_Attacker,
    Even_Turn_Attacker,
    Herzberg_Motag_Attacker,  # All but one attacker
    # Never_Alone_Attacker,  # Anna said we don't need this
    Never_Last_Attacker,
    Log2n_Turns_Straight_Attacker
]
attackers = attackers[::-1]

users_per_bucket = 10_000
trials = 10
num_rounds = 501
percent_attackers_list = (0, .001, .005, .01, .02, .03, .04)


grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs/paper_graphs",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=managers,
    attackers=attackers,
    percent_attackers_list=percent_attackers_list,
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)

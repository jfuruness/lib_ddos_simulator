from lib_ddos_simulator import (
    Combination_Grapher,
    Motag_Manager_40_Bucket,
    Motag_Manager_40_Bucket_Invalid,
    Motag_Manager_40_Bucket_Combine_Diff_Start,
    Motag_Manager_40_Bucket_No_Combine_Diff_Start,
    Motag_Manager_40_Bucket_No_Combine_Normal_Start,
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
    Motag_Manager_40_Bucket,
    Motag_Manager_40_Bucket_Invalid,
    Motag_Manager_40_Bucket_Combine_Diff_Start,
    Motag_Manager_40_Bucket_No_Combine_Diff_Start,
    Motag_Manager_40_Bucket_No_Combine_Normal_Start,
]

attackers = [
    Basic_Attacker,
    Even_Turn_Attacker,
    Herzberg_Motag_Attacker,  # All but one attacker
    Never_Last_Attacker,
    Log2n_Turns_Straight_Attacker
]

users_per_bucket = 10_000
trials = 8
num_rounds = 501
percent_attackers_list = (0, .001, .005, .01, .02, .03, .04)


############################

grapher = Combination_Grapher(debug=True,
                              graph_dir="/tmp/ddos_graphs/motag_experiment",
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

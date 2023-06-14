from lib_ddos_simulator import (
    Combination_Grapher,
    Protag_Manager_Merge,
    Protag_Manager_No_Merge,Motag_Manager_20_Bucket,
    Motag_Manager_200_Bucket,
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
    Protag_Manager_No_Merge,
    Motag_Manager_20_Bucket,
    Motag_Manager_200_Bucket,
    Isolator_2i_1f,
    # Isolator_2i_kf,
    # Isolator_3i_1f,
    Isolator_3i_kf,
    Isolator_2i_SQRT_kf,
    # Isolator_3i_SQRT_kf,
    Opt_S,
    Opt_H,
]

attackers = [
    Basic_Attacker,
    Even_Turn_Attacker,
    Herzberg_Motag_Attacker,  # All but one attacker
    Never_Alone_Attacker,
    Never_Last_Attacker,
    Log2n_Turns_Straight_Attacker
]
attackers = attackers[::-1]

users_per_bucket = 10_000
trials = 2
num_rounds = 501



############### Attackers from 1 to 6% with Opt H #############

grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs/1",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=managers,
    attackers=attackers,
    percent_attackers_list=[x / 100 for x in range(1, 7)],
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)


############### Attackers from 1 to 625 insiders with Opt H #############

grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs/2",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=managers,
    attackers=attackers,
    percent_attackers_list=[
        1/users_per_bucket,
        5/users_per_bucket,
        25/users_per_bucket,
        125/users_per_bucket,
        625/users_per_bucket,
    ],
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)


############### Attackers from 1 to 6% without Opt H #############

grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs/3",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=[x for x in managers if x != Opt_H],
    attackers=attackers,
    percent_attackers_list=[x / 100 for x in range(1, 7)],
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)


############### Attackers from 1 to 625 insiders without Opt H #############

grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs/4",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=[x for x in managers if x != Opt_H],
    attackers=attackers,
    percent_attackers_list=[
        1/users_per_bucket,
        5/users_per_bucket,
        25/users_per_bucket,
        125/users_per_bucket,
        625/users_per_bucket,
    ],
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)

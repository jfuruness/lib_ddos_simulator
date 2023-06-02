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

managers=[
    Protag_Manager_Merge,
    Protag_Manager_No_Merge,
    Motag_Manager_20_Bucket,
    Motag_Manager_200_Bucket,
    Isolator_2i_1f,
    Isolator_2i_kf,
    Isolator_3i_1f,
    Isolator_3i_kf,
    Isolator_2i_SQRT_kf,
    Isolator_3i_SQRT_kf,
    Opt_S,
    Opt_H,
],


users_per_bucket = 1000
# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs",
                              tikz=False,
                              save=True,
                              high_res=False)
print(len(Attacker.runnable_attackers))
# For the full list of managers that is run by default,
# see Managers section
grapher.run(
    managers=[
        Protag_Manager_Merge,
        Protag_Manager_No_Merge,
        Motag_Manager_20_Bucket,
        Motag_Manager_200_Bucket,
        Isolator_2i_1f,
        Isolator_2i_kf,
        Isolator_3i_1f,
        Isolator_3i_kf,
        Opt_S,
        Opt_H,
    ],
    attackers=[
        x for x in Attacker.runnable_attackers
        if "Never_Alone" not in x.__name__
    ],
    percent_attackers_list=[x / 100 for x in range(1, 7)],
    # percent_attackers_list = [1,10,100,1000],
    num_buckets=1,
    # Takes 1m 57s for 1k 2 trials 101 rounds
    users_per_bucket=users_per_bucket,
    num_rounds=101,
    #num_rounds=101,
    trials=2
)

# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs_2",
                              tikz=False,
                              save=True,
                              high_res=False)
print(len(Attacker.runnable_attackers))
# For the full list of managers that is run by default,
# see Managers section
users_per_bucket = 10_000
grapher.run(
    managers=[
        Protag_Manager_Merge,
        Protag_Manager_No_Merge,
        Motag_Manager_20_Bucket,
        Motag_Manager_200_Bucket,
        Isolator_2i_1f,
        Isolator_2i_kf,
        Isolator_3i_1f,
        Isolator_3i_kf,
        Opt_S,
        Opt_H
    ],
    attackers=[
        x for x in Attacker.runnable_attackers
        if "Never_Alone" not in x.__name__
    ],
    percent_attackers_list=[
        1/users_per_bucket,
        10/users_per_bucket,
        100/users_per_bucket,
        1000/users_per_bucket,
    ],
    # percent_attackers_list = [1,10,100,1000],
    num_buckets=1,
    # Takes 1m 57s for 1k 2 trials 101 rounds
    users_per_bucket=users_per_bucket,
    num_rounds=101,
    #num_rounds=101,
    trials=2
)

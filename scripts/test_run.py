# https://buildbot.pypy.org/nightly/release-pypy3.10-v7.x/pypy-c-jit-latest-linux64.tar.bz2

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

users_per_bucket = 100
# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs_test",
                              tikz=False,
                              save=True,
                              high_res=False)
# For the full list of managers that is run by default,
# see Managers section
grapher.run(
    managers=[
        Protag_Manager_Merge,
    ],
    attackers=[
        x for x in Attacker.runnable_attackers
        if "Never_Alone" not in x.__name__
    ][:2],
    percent_attackers_list=[x / 100 for x in range(1, 7)][:2],
    # percent_attackers_list = [1,10,100,1000],
    num_buckets=1,
    # Takes 1m 57s for 1k 2 trials 101 rounds
    users_per_bucket=users_per_bucket,
    num_rounds=10,
    #num_rounds=101,
    trials=2
)

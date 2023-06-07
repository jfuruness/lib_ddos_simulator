from lib_ddos_simulator import (
    Combination_Grapher,
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
    Opt_H,
    Opt_S,
    Attacker
)

managers = [
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
]


users_per_bucket = 10_000
# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs",
                              tikz=False,
                              save=True,
                              high_res=False)
print(len(Attacker.paper_attackers))

import time
start = time.perf_counter()
if True:
    # For the full list of managers that is run by default,
    # see Managers section
    grapher.run(
        managers=managers,
        attackers=[
            x for x in Attacker.paper_attackers
            if "Never_Alone" not in x.__name__
        ],
        percent_attackers_list=[x / 100 for x in range(1, 7)],
        # percent_attackers_list = [1,10,100,1000],
        num_buckets=1,
        # Takes 1m 57s for 1k 2 trials 101 rounds
        users_per_bucket=users_per_bucket,
        num_rounds=501,
        # num_rounds=101,
        trials=2
    )
else:
    # For the full list of managers that is run by default,
    # see Managers section
    grapher.run(
        managers=managers[:1],
        attackers=[
            x for x in Attacker.paper_attackers
            if "Never_Alone" not in x.__name__
        ][:2],
        percent_attackers_list=[x / 100 for x in range(1, 7)][:2],
        # percent_attackers_list = [1,10,100,1000],
        num_buckets=1,
        # Takes 1m 57s for 1k 2 trials 101 rounds
        users_per_bucket=users_per_bucket,
        num_rounds=10,
        # num_rounds=101,
        trials=2
    )

end = time.perf_counter()
print(f"Ran in {round((end-start) / 2, 2)}s per trial")

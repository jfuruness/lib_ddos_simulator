import time
import cProfile
import pstats
import io


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
    # Motag_Manager_20_Bucket,
    # Motag_Manager_200_Bucket,
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

users_per_bucket = 10_000
trials = 2
num_rounds = 501



############### Attackers from 1 to 6% with Opt H #############

start = time.perf_counter()
pr = cProfile.Profile()
pr.enable()

grapher = Combination_Grapher(debug=True,
                              graph_dir="/tmp/ddos_graphs/benchmark",
                              tikz=False,
                              save=True,
                              high_res=False)
grapher.run(
    managers=managers,
    attackers=attackers,
    percent_attackers_list=[5 / 100],
    num_buckets=1,
    users_per_bucket=users_per_bucket,
    num_rounds=num_rounds,
    trials=trials
)
end = time.perf_counter()
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('/tmp/test.txt', 'w') as f:
    f.write(s.getvalue())

print(f"Ran in {round((end-start) / 2, 2)}s per trial")

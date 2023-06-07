import cProfile
import pstats
import io


from lib_ddos_simulator import Combination_Grapher, Sieve_Manager_Base, Attacker, Protag_Manager_Merge, Basic_Attacker

# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=True,
                              graph_dir="/tmp/lib_ddos_simulator",
                              tikz=False,
                              save=True,
                              high_res=False)


pr = cProfile.Profile()
pr.enable()
# For the full list of managers that is run by default, see Managers section
grapher.run(managers=[Protag_Manager_Merge],  # List of runnable managers
            # List of runnable attackers
            attackers=[Basic_Attacker],
            # List of percentages to run
            percent_attackers_list=[.5],#[x / 100 for x in range(1, 92, 5)],
            # Number of buckets to start the simulations off
            num_buckets=10,
            # Number of users in each bucket to start
            users_per_bucket=100,
            # Number of rounds per trial
            num_rounds=5,
            # Number of trials. NEVER LESS THAN 2 - you need two to calculate stddev
            trials=20000)
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
ps.print_stats()

with open('test.txt', 'w') as f:
    f.write(s.getvalue())

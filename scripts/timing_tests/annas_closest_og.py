import cProfile
import pstats
import io

from lib_ddos_simulator import Combination_Grapher, Protag_Manager_Merge, Protag_Manager_No_Merge,Motag_Manager_20_Bucket, Motag_Manager_200_Bucket, Isolator_2i_1f, Isolator_3i_kf, Attacker
# NOTE: Removed 2 Opt managers

# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=True,
                              graph_dir="/tmp/lib_ddos_simulator",
                              tikz=True,
                              save=True,
                              high_res=False)
print(len(Attacker.runnable_attackers))

#pr = cProfile.Profile()
#pr.enable()


# For the full list of managers that is run by default, see Managers section
# NOTE: removed 1 Opt manager, all motag managers
grapher.run(managers=[Protag_Manager_Merge, Protag_Manager_No_Merge, Isolator_2i_1f, Isolator_3i_kf],
#grapher.run(managers=[Protag_Manager_Merge, Protag_Manager_No_Merge,Isolator_2i_1f, Isolator_3i_kf,Opt_H, Opt_S],
# NOTE: Removed Never_Alone_Attacker because it's not necessary
            attackers=[x for x in Attacker.runnable_attackers if "Never_Alone_Attacker"  != x.__name__],
            percent_attackers_list=[x / 100 for x in range(1, 7)],
            num_buckets=1,
            users_per_bucket=10000,
            num_rounds=500,
            trials=2)

#pr.disable()
#
#s = io.StringIO()
#ps = pstats.Stats(pr, stream=s).sort_stats('cumtime')
#ps.print_stats()
#
#with open('test.txt', 'w') as f:
#    f.write(s.getvalue())

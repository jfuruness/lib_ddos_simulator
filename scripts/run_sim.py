from lib_ddos_simulator import Combination_Grapher, Protag_Manager_Merge, Protag_Manager_No_Merge,Motag_Manager_20_Bucket, Motag_Manager_200_Bucket, Isolator_2i_1f, Isolator_3i_kf, Opt_H, Opt_S, Attacker

# stream_level and graph_path defaults, can be omitted
grapher = Combination_Grapher(debug=False,
                              graph_dir="/tmp/ddos_graphs",
                              tikz=True,
                              save=True,
                              high_res=False)
print(len(Attacker.runnable_attackers))
# For the full list of managers that is run by default, see Managers section
grapher.run(managers=[Protag_Manager_Merge, Protag_Manager_No_Merge,Motag_Manager_20_Bucket, Motag_Manager_200_Bucket, Isolator_2i_1f, Isolator_3i_kf, Opt_S],
#grapher.run(managers=[Protag_Manager_Merge, Protag_Manager_No_Merge,Isolator_2i_1f, Isolator_3i_kf,Opt_H, Opt_S],
            attackers=[x for x in Attacker.runnable_attackers if "Never_Alone" not in x.__name__],
            percent_attackers_list=[x / 100 for x in range(1, 7)],
            num_buckets=1,
            users_per_bucket=10000,
            num_rounds=101,
            trials=10)

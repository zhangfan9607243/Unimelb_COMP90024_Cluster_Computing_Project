import time
import json
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print("Method: Not read files in parallel, but process in parallel.")
    print()

file_name = "data/bigTwitter.json"

# Process 0 & 7: Set start time
if rank in [0,7]:
    begin_time = time.time()

# Process 0: Read data files
if rank == 0:
    # (1) Read suburb data file
    sub_dict = {}
    with open("data/sal.json", "r", encoding="utf-8") as sal_file:
        sal_data = json.load(sal_file)
    for suburb in sal_data:
        sub_dict[suburb] = sal_data[suburb]["gcc"]
    gcc_valid = ["1gsyd", "2gmel", "3gbri", "4gade", "5gper", "6ghob", "7gdar", "8acte", "9oter", "0none"]
    # Send suburb dictionary and valid gcc list to process 1, 2, 3
    comm.send((sub_dict, gcc_valid), dest=1, tag=11)
    comm.send((sub_dict, gcc_valid), dest=2, tag=22)
    comm.send((sub_dict, gcc_valid), dest=3, tag=33)
    
    # (2) Read twitter data file
    with open(file_name, "r", encoding="utf-8") as twitter_file:
        new_line = twitter_file.readline()
        while new_line:
            new_line = twitter_file.readline()
            if new_line.strip()[0:11] == '"author_id"':
                aid = new_line.split(":")[1].strip().split(",")[0].strip('"')
                while not new_line.strip()[0:11] == '"full_name"':
                    new_line = twitter_file.readline()
                sub = new_line.split(":")[1].strip().split(",")[0].strip('"').lower()
                gcc = sub_dict.get(sub)
                if gcc not in gcc_valid:
                    gcc = "0none"  
                # Send gcc to process 1; aid to process 2; pair of gcc and aid to process 3
                comm.send(gcc, dest=1, tag=1)
                comm.send(aid, dest=2, tag=2)
                comm.send((gcc,aid), dest=3, tag=3)
        # Send a over signal to process 1, 2, 3
        comm.send("OVER", dest=1, tag=1)
        comm.send("OVER", dest=2, tag=2)
        comm.send("OVER", dest=3, tag=3)

# Process 0: Mid time check
if rank == 0:
    print("Mid Time Check (After Read): Time used: " + str(round(time.time()-begin_time,2)) + " seconds.")

# Process 1: Count in great capital city dictionary
if rank == 1:
    sub_dict, gcc_valid = comm.recv(source=0, tag=11)
    gcc_dict = {"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}
    while True:
        gcc = comm.recv(source=0, tag=1)
        if gcc != "OVER":
            if gcc in gcc_dict:
                gcc_dict[gcc] += 1
            else:
                gcc_dict[gcc] = 1 
        else:
            break
    # Send processed greater capital city dictionary to process 4
    comm.send(gcc_dict, dest=4, tag=4)

# Process 2: Count in author id dictionary
elif rank == 2:
    sub_dict, gcc_valid = comm.recv(source=0, tag=22)
    aid_dict = {"test":0}
    while True:
        aid = comm.recv(source=0, tag=2)
        if aid != "OVER":
            if aid in aid_dict:
                aid_dict[aid] += 1
            else:
                aid_dict[aid] = 1
        else:
            break
    # Send processed author id dictionary to process 5
    comm.send(aid_dict, dest=5, tag=5)

# Process 3: Count in author in greater capital city dictionary
elif rank == 3:
    sub_dict, gcc_valid = comm.recv(source=0, tag=33)
    agc_dict = {"test":{"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}}
    while True:
        rcv = comm.recv(source=0, tag=3)
        if rcv != "OVER":
            gcc, aid = rcv
            if aid in agc_dict:
                agc_dict[aid][gcc] += 1
            else:
                agc_dict[aid] = {"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}
                agc_dict[aid][gcc] += 1
        else:
            break
    # Send processed author in greater capital city dictionary dictionary to process 6
    comm.send(agc_dict, dest=6, tag=6)

# Process 4: Summarise greater capital city
if rank == 4:
    gcc_dict = comm.recv(source=1, tag=4)
    gcc_dict.pop("0none")
    gcc_dict.pop("7gdar")
    gcc_dict.pop("8acte")
    gcc_dict.pop("9oter")
    gcc_name_list = list(gcc_dict.keys())
    gcc_cont_list = list(int(i) for i in gcc_dict.values())
    gcc_name_list_sort = []
    gcc_cont_list_sort = []
    for i in np.array(gcc_cont_list).argsort()[::-1]:
        if gcc_name_list[i] == "1gsyd":
            add_name = " (Greater Sydney)"
        elif gcc_name_list[i] == "2gmel":
            add_name = " (Greater Melbourne)"
        elif gcc_name_list[i] == "3gbri":
            add_name = " (Greater Brisbane)"
        elif gcc_name_list[i] == "4gade":
            add_name = " (Greater Adelaide)"
        elif gcc_name_list[i] == "5gper":
            add_name = " (Greater Perth)"
        else:
            add_name = " (Greater Hobart)"
        gcc_name_list_sort.append(gcc_name_list[i]+add_name)
        gcc_cont_list_sort.append(gcc_cont_list[i])
    gcc_sumy_string = "%-30s\t\t%-30s\n"%("Greater Capital City","Number of Tweets Made")
    for i in range(6):
        gcc_sumy_string += "%-30s\t\t%-30s\n"%(gcc_name_list_sort[i],gcc_cont_list_sort[i])
    # Send summarised string to process 7 
    comm.send(gcc_sumy_string, dest=7, tag=7)

# Process 5: Summarise author id
elif rank == 5:
    aid_dict = comm.recv(source=2, tag=5)
    aid_name_list = list(aid_dict.keys())
    aid_cont_list = list(aid_dict.values())
    aid_rank_list = []
    aid_name_list_sort = []
    aid_cont_list_sort = []
    rank_i = 1
    for i in np.array(aid_cont_list).argsort()[::-1]:
        aid_rank_list.append("#" + str(rank_i))
        aid_name_list_sort.append(aid_name_list[i])
        aid_cont_list_sort.append(aid_cont_list[i])
        rank_i += 1
    aid_sumy_string = "%-20s\t\t%-20s\t\t%-20s\n"%("Rank","Author Id","Number of Tweets Made")
    for i in range(10):
        aid_sumy_string += "%-20s\t\t%-20s\t\t%-20s\n"%(aid_rank_list[i],aid_name_list_sort[i],aid_cont_list_sort[i])
    # Send summarised string to process 7 
    comm.send(aid_sumy_string, dest=7, tag=8)

# Process 6: Summarise author in greater capital city
elif rank == 6:
    agc_dict = comm.recv(source=3, tag=6)
    agc_aid_list = list(agc_dict.keys())
    ags_gcc_list = list(agc_dict.values())
    agc_name_list = []
    agc_cont_byucity_list = []
    agc_cont_byntwet_list = []
    agc_strg_list = []
    agc_sumy_table = []
    for i in range(len(agc_aid_list)):
        aid_i = agc_aid_list[i]
        gcc_i = ags_gcc_list[i]
        gcc_i_name_list = list(gcc_i.keys())
        gcc_i_cont_list = list(gcc_i.values())
        gcc_i_name_list_sort = []
        gcc_i_cont_list_sort = []
        for j in np.array(gcc_i_cont_list).argsort()[::-1]:
            if gcc_i_cont_list[j] != 0 and gcc_i_name_list[j] not in ["0none", "7gdar", "8acte", "9oter"]:
                gcc_i_name_list_sort.append(gcc_i_name_list[j][1::])
                gcc_i_cont_list_sort.append(gcc_i_cont_list[j])
        str_i = str(len(gcc_i_cont_list_sort)) + " (#" + str(sum(gcc_i_cont_list_sort)) + " tweets - "
        for k in range(len(gcc_i_name_list_sort)):
            str_i += str(gcc_i_cont_list_sort[k]) + gcc_i_name_list_sort[k] + ", "
        str_i = str_i[:-2] + ")"
        agc_name_list.append(aid_i)
        agc_cont_byucity_list.append(len(gcc_i_cont_list_sort))
        agc_cont_byntwet_list.append(sum(gcc_i_cont_list_sort))
        agc_strg_list.append(str_i)
        agc_sumy_table.append([aid_i, str_i, len(gcc_i_cont_list_sort), sum(gcc_i_cont_list_sort)])
    agc_sumy_table = sorted(agc_sumy_table, key=(lambda x:[x[2],x[3]]),reverse=True)
    agc_sumy_string = "%-20s\t\t%-20s\t\t%-20s\n"%("Rank", "Author Id", "Number of Unique City Locations and #Tweets")
    for i in range(10):
        agc_sumy_string += "%-20s\t\t%-20s\t\t%-20s\n"%(str("#")+str(i+1), agc_sumy_table[i][0],agc_sumy_table[i][1])
    # Send summarised string to process 7 
    comm.send(agc_sumy_string, dest=7, tag=9)

# Process 7: Print output
if rank == 7:
    gcc_sumy_string = comm.recv(source=4, tag=7)
    aid_sumy_string = comm.recv(source=5, tag=8)
    agc_sumy_string = comm.recv(source=6, tag=9)
    print("End Time Check (After Summary): Time used: " + str(round(time.time()-begin_time,2)) + " seconds.")
    print()
    print("## Final Result:")
    print()
    print("1. Count number of tweets made in greater capital cities: ")
    print(gcc_sumy_string)
    print("2. Count number of tweets made by different authors: ")
    print(aid_sumy_string)
    print("3. Authors that made tweeted in the most Greater Capital cities: ")
    print(agc_sumy_string)
    
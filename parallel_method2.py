import time
import json
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print("Method: Read files in parallel, but not process in parallel.")
    print()

file_name = "data/bigTwitter.json"

# Process 0: Set start time
if rank == 0:
    begin_time = time.time()

# All processes: Read data files
# (1) Suburb data file
sub_dict = {}
with open("data/sal.json", "r", encoding="utf-8") as sal_file:
    sal_data = json.load(sal_file)
for suburb in sal_data:
    sub_dict[suburb] = sal_data[suburb]["gcc"]

# (2) Twitter data file
gcc_valid = ["1gsyd", "2gmel", "3gbri", "4gade", "5gper", "6ghob", "7gdar", "8acte", "9oter", "0none"]
aid_gcc_pair_list = []

with open(file_name, "r", encoding="utf-8") as twitter_file:
    new_line = twitter_file.readline()
    count = 0
    while new_line:
        new_line = twitter_file.readline()
        if new_line.strip()[0:11] == '"author_id"':
            count += 1
            # Only process that it is its turn read the object
            if count % size == rank:
                aid = new_line.split(":")[1].strip().split(",")[0].strip('"')
                while not new_line.strip()[0:11] == '"full_name"':
                    new_line = twitter_file.readline()
                sub = new_line.split(":")[1].strip().split(",")[0].strip('"').lower()
                gcc = sub_dict.get(sub)
                if gcc not in gcc_valid:
                    gcc = "0none"
                aid_gcc_pair_list.append((aid,gcc))

# All process: Send list of pair of aid and gcc to process 0
aid_gcc_pair_list_gather = comm.gather(aid_gcc_pair_list, root = 0)

# Process 0: Mid time check
if rank == 0:
    print("Mid Time Check (After Read): Time used: " + str(round(time.time()-begin_time,2)) + " seconds.")

# Process 0: Do all the summarise tasks
if rank == 0:
    # Count in three dictionaries
    aid_gcc_pair_list_rearrange = []
    for lists in aid_gcc_pair_list_gather:
        for pair in lists:
            aid_gcc_pair_list_rearrange.append(pair)
    gcc_dict = {"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}
    aid_dict = {"test":0}
    agc_dict = {"test":{"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}}
    for aid, gcc in aid_gcc_pair_list_rearrange:
        if gcc in gcc_dict:
            gcc_dict[gcc] += 1
        else:
            gcc_dict[gcc] = 1 
        if aid in aid_dict:
            aid_dict[aid] += 1
        else:
            aid_dict[aid] = 1
        if aid in agc_dict:
            agc_dict[aid][gcc] += 1
        else:
            agc_dict[aid] = {"1gsyd":0, "2gmel":0, "3gbri":0, "4gade":0, "5gper":0, "6ghob":0, "7gdar":0, "8acte":0, "9oter":0, "0none":0}
            agc_dict[aid][gcc] += 1

    # Summarise greater capital city
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

    # Summarise author id
    aid_dict.pop("test")
    aid_name_list = list(aid_dict.keys())
    aid_cont_list = list(aid_dict.values())
    aid_rank_list = []
    aid_name_list_sort = []
    aid_cont_list_sort = []
    rank = 1
    for i in np.array(aid_cont_list).argsort()[::-1]:
        aid_rank_list.append("#" + str(rank))
        aid_name_list_sort.append(aid_name_list[i])
        aid_cont_list_sort.append(aid_cont_list[i])
        rank += 1
    aid_sumy_string = "%-20s\t\t%-20s\t\t%-20s\n"%("Rank","Author Id","Number of Tweets Made")
    for i in range(10):
        aid_sumy_string += "%-20s\t\t%-20s\t\t%-20s\n"%(aid_rank_list[i],aid_name_list_sort[i],aid_cont_list_sort[i])

    # Summarise author in cities
    agc_dict.pop("test")
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

    # Print the result and check the time
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


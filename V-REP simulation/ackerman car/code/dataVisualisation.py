import csv

import matplotlib.pyplot as plt
import os

source_dir = "results"


def import_gen_data(gen_no):
    data = []
    with open(os.path.join(source_dir, ('statistics/gen-' + str(gen_no) + ".csv"))) as f_obj:
        reader = csv.reader(f_obj, delimiter=',')
        for line in reader:
            try:
                data.append([float(line[0]), float(line[1]), float(line[2])])
            except ValueError:
                pass
    return data


def init(dir):
    global source_dir
    source_dir = dir


def add_to_scatter(gen_no):
    gen_data = import_gen_data(gen_no)
    plt.subplot(111)
    plt.grid(True)
    plt.title("Generation " + str(gen_no))
    plt.xlabel('Genome #')
    plt.ylabel('Sim. Time')
    plt.xlim(-1, len(gen_data))
    plt.ylim(0, 800)
    plt.scatter([i for i in range(0, len(gen_data))], [time[1] for time in gen_data])
    plt.show()


def all_in_range(start_gen_no, end_gen_no, step=1):
    all_from([i for i in range(start_gen_no, end_gen_no + 1, step)],
             "from {0} till {1} with step {2}".format(start_gen_no, end_gen_no, step))


def all_from(gens, gens_description=""):
    plt.subplot(111)
    plt.grid(True)
    if len(gens_description) == 0:
        d = str(gens)
    else:
        d= gens_description
    plt.title("Generations " + d)
    plt.xlabel('Genome #')
    plt.ylabel('Sim. Time')
    plt.ylim(0, 800)
    for gen in gens:
        data = import_gen_data(gen)
        plt.scatter([i for i in range(0, len(data))], [time[1] for time in data], label="gen " + str(gen))
    plt.legend()
    plt.show()

def speed_time_dependency(gen_no):
    plt.subplot(111)
    plt.grid(True)
    plt.title("Generation " + str(gen_no))
    plt.xlabel('Avg. Speed')
    plt.ylabel('Sim. Time')
    plt.ylim(0, 800)
    data = import_gen_data(gen_no)
    plt.scatter([time[0] for time in data], [time[1] for time in data])
    plt.show()
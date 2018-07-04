import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import graphviz
import os

source_dir = 'results'
statistics_prefix = 'statistics/gen-'
checkpoints_prefix = 'checkpoints/neat-checkpoint-'


def init(dir, stat_prefix='statistics/gen-', checkp_prefix='checkpoints/neat-checkpoint-'):
    global source_dir, statistics_prefix, checkpoints_prefix
    source_dir = dir
    statistics_prefix = stat_prefix
    checkpoints_prefix = checkp_prefix


def import_gen_stat_data(gen_no):
    data = []
    with open(os.path.join(source_dir, (statistics_prefix + str(gen_no) + ".csv"))) as f_obj:
        reader = csv.reader(f_obj, delimiter=',')
        for line in reader:
            try:
                data.append([float(line[0]), float(line[1]), float(line[2])])
            except ValueError:
                pass
    return data


def add_to_scatter(gen_no):
    gen_data = import_gen_stat_data(gen_no)
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
        data = import_gen_stat_data(gen)
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
    data = import_gen_stat_data(gen_no)
    plt.scatter([time[0] for time in data], [time[1] for time in data])
    plt.show()


def draw_best_genome_net(gen_no):
    from NeatEngine.utils import import_best_genome
    best_gen, config = import_best_genome(os.path.join(source_dir, checkpoints_prefix + str(gen_no)),
                                          os.path.join(source_dir, 'config-neat'))
    draw_net(config, best_gen, 'net-gen-' + str(gen_no))


def draw_net(config, genome, filename='net'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    file_path = os.path.join(source_dir, 'net-images', filename)
    format = 'png'

    node_names = {}
    node_colors = {}

    node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'
    }

    dot = graphviz.Digraph(format=format, node_attr=node_attrs)
    dot.attr(rankdir='LR')

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled'}
        input_attrs['fillcolor'] = node_colors.get(k, 'lightgray')
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled'}
        node_attrs['fillcolor'] = node_colors.get(k, 'lightblue')

        dot.node(name, _attributes=node_attrs)

    used_nodes = set(genome.nodes.keys())

    for n in used_nodes:
        if n in inputs or n in outputs:
            continue

        attrs = {'style': 'filled',
                 'fillcolor': node_colors.get(n, 'white')}
        dot.node(str(n), _attributes=attrs)

    for cg in genome.connections.values():
        if cg.enabled:
            # if cg.input not in used_nodes or cg.output not in used_nodes:
            #    continue
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            color = 'green' if cg.enabled else 'red'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(a, b, label=str('%.3f' % cg.weight), _attributes={'color': color, 'penwidth': width})

    dot.render(file_path)
    img = mpimg.imread(file_path + "." + format)
    plt.imshow(img)
    plt.title(file_path)
    labels = [
        'input', 'output', 'hidden', 'enabled', 'disabled'
    ]
    markers = ['o', 'o', 'o', r'$\rightarrow$', r'$\rightarrow$']
    colors = ['lightgray', 'lightblue', 'w', 'green', 'red']
    plt.legend(handles=[
        plt.plot([], [], marker=markers[i], ms=10, ls="", mec=None, color=colors[i],
                 label="{:s}".format(labels[i]))[0] for i in range(len(labels))
    ])
    plt.show()
    return dot
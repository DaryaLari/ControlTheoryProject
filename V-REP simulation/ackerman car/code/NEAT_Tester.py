import neat
import os
import csv
import simulation

client_id = -1
generation = 0

params_borders = [
    [50, 250],
    [0, 50],
    [0, 5],
    [0, 50]
]


def export_population_info(params):
    with open("generations_stat/gen" + str(generation) + ".csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows([params])


def normalize_params(params):
    for i in range(0, len(params)):
        params[i] = (params[i] - params_borders[i][0]) / (params_borders[i][1] - params_borders[i][0])
    return params


def denormalize_params(params):
    for i in range(0, len(params)):
        params[i] = params_borders[i][0] + params[i] * (params_borders[i][1] - params_borders[i][0])
    return params


def eval_genomes(genomes, config):
    export_population_info(["Speed", "Kp", "Ki", "Kd", "Time", "Fitness"])
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        [speed, kp, ki, kd] = denormalize_params(net.activate(normalize_params([100, 5, 0.1, 1])))
        time = simulation.run_test(client_id, speed, kp, ki, kd, log_errors=False, time_limit=1500)
        genome.fitness = speed * time
        export_population_info([speed, kp, ki, kd, time, genome.fitness])

    global generation
    generation += 1


def run():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-neat')
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # last_g = neat.Checkpointer.last_generation_checkpoint
    # if last_g != -1:
    #     p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-' + str(last_g))

    # Run for up to 100 generations.
    winner = p.run(eval_genomes, 100)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')

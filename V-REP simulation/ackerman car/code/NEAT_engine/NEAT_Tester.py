import neat
import os
import csv

import simulation
from NEAT_engine import CarController

client_id = -1
generation = 0
sim_time_limit = -1
max_generations = 100


def init_tester(c_id, time_limit=-1, gen_amount=100):
    global client_id, sim_time_limit, max_generations
    client_id = c_id
    sim_time_limit = time_limit
    max_generations = gen_amount


def export_population_info(params):
    print("\n-------------------------"
     + "\n| avg. speed: " + str(params[0])
     + "\n| sim. time:  " + str(params[1])
     + "\n| fitness:    " + str(params[2])
     + "\n-------------------------")
    with open("results/statistics/gen-" + str(generation) + ".csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows([params])


def eval_genomes(genomes, config):
    export_population_info(["Average Speed", "Simulation Time", "Fitness"])
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        controller = CarController.CarController(net)
        time = simulation.run_controlled_test(client_id, controller, log_errors=False, time_limit=sim_time_limit)

        avg_speed = controller.avg_speed
        genome.fitness = avg_speed * time
        export_population_info([avg_speed, time, genome.fitness])

    global generation
    generation += 1


def init_NEAT():
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
    p.add_reporter(neat.Checkpointer(1, filename_prefix='results/checkpoints/neat-checkpoint-'))

    # last_g = neat.Checkpointer.last_generation_checkpoint
    # if last_g != -1:
    # p = neat.Checkpointer.restore_checkpoint('18')
    return p


def run():
    population = init_NEAT()

    # Run several generations.
    winner = population.run(eval_genomes, max_generations)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')

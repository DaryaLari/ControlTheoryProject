import neat
import os


def import_best_genome(restore_file_name, config_file_name):

    p = neat.Checkpointer.restore_checkpoint(restore_file_name)
    if p.best_genome is not None:
        best_gen = p.best_genome
    else:
        best_gen = max(filter(lambda g: g.fitness is not None, p.population.values()), key=lambda g: g.fitness)

    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file_name)

    return best_gen, config


def get_net_of_best_genome(restore_file_name, config_file_name):
    best_gen, config = import_best_genome(restore_file_name, config_file_name)
    return get_net_of_genome(best_gen, config)


def get_net_of_genome(genome, config):
    return neat.nn.FeedForwardNetwork.create(genome, config)
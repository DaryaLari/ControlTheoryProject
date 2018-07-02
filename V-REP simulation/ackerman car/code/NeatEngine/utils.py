import neat
import os


def import_best_genome(base_dir, restore_gen):

    restore_file_name = "{0}/checkpoints/neat-checkpoint-{1}".format(base_dir, restore_gen)
    p = neat.Checkpointer.restore_checkpoint(restore_file_name)
    if p.best_genome is not None:
        best_gen = p.best_genome
    else:
        best_gen = max(filter(lambda g: g.fitness is not None, p.population.values()), key=lambda g: g.fitness)

    config_file = os.path.join(base_dir, 'config-neat')
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    return best_gen, config


def get_net_of_best_genome(base_dir, restore_gen):
    return get_net_of_best_genome(import_best_genome(base_dir, restore_gen))


def get_net_of_genome(genome, config):
    return neat.nn.FeedForwardNetwork.create(genome, config)
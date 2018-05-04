import neat
import os
import scene_loading

client_id = -1

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        params = net.activate([100, 3, 0.1, 1])
        speed = params[0] * 200
        kp = params[1] * 10
        ki = params[2] * 1
        kd = params[3] * 10
        if speed < 5:
            genome.fitness = 0
        else:
            genome.fitness = speed * scene_loading.run_test(client_id, speed, kp, ki, kd)


class NEAT_Tester:

    def run(self):
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

        # Run for up to 100 generations.
        winner = p.run(eval_genomes, 100)

        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))

        # Show output of the most fit genome against training data.
        print('\nOutput:')

        last_g = neat.Checkpointer.last_generation_checkpoint
        if last_g != -1:
            p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-' + str(last_g))
        p.run(eval_genomes, 10)

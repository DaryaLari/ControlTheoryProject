import neat
import os
import csv
from simulationEnvironment import simulation


class NeatTester:
    client_id = -1
    sim_time_limit = -1
    max_generations = 100

    def __init__(self, c_id, fitness_function, controller_type, controller_init_function, gen_amount=100, resdir="results", restore_gen=-1):
        self.client_id = c_id
        self.controller_type = controller_type
        self.controller_init_function = controller_init_function
        self.calc_fitness = fitness_function
        self.max_generations = gen_amount
        self.baseDir = resdir
        self.population = None

        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, 'config-neat')
        # Load configuration.
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        if not os.path.exists(self.baseDir):
            os.makedirs(self.baseDir + "/checkpoints")
            os.makedirs(self.baseDir + "/statistics")

        if restore_gen != -1:
            restore_file_name = self.baseDir + "/checkpoints/neat-checkpoint-" + str(restore_gen)
            if not os.path.exists(restore_file_name):
                print("File '" + restore_file_name + "' doesn't exists")
                return
            p = neat.Checkpointer.restore_checkpoint(restore_file_name)
        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        p.add_reporter(neat.Checkpointer(1, filename_prefix=self.baseDir + "/checkpoints/neat-checkpoint-"))

        self.population = p

    def export_population_info(self, params):
        print("\n-------------------------"
         + "\n| avg. speed: " + str(params[0])
         + "\n| sim. time:  " + str(params[1])
         + "\n| fitness:    " + str(params[2])
         + "\n-------------------------")

        with open(self.baseDir + "/statistics/gen-" + str(self.population.generation) + ".csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([params])

    def eval_genomes(self, genomes, config):
        self.export_population_info(["Average Speed", "Simulation Time", "Fitness"])
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            # Create & init controller
            controller = self.controller_type(net)
            if self.controller_init_function is not None:
                self.controller_init_function(controller)

            time = simulation.run_test(controller, log_errors=False)

            avg_speed = controller.avg_speed
            genome.fitness = self.calc_fitness(controller.states) # avg_speed * time
            self.export_population_info([avg_speed, time, genome.fitness])

    def run(self):
        # Run several generations.
        winner = self.population.run(self.eval_genomes, self.max_generations)
        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))

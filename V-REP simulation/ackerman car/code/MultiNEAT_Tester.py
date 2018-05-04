import MultiNEAT as NEAT
import scene_loading

params = NEAT.Parameters()

params.PopulationSize = 100

genome = NEAT.Genome(0,
                     5, # inputs# (1 extra input)
                     0,
                     1, # outputs#
                     False,
                     NEAT.ActivationFunction.UNSIGNED_SIGMOID,
                     NEAT.ActivationFunction.UNSIGNED_SIGMOID,
                     0,
                     params,
                     0)

# create population
population = NEAT.Population(genome, params, True, 1.0, 0) # the 0 is the RNG seed

def evaluate(genome):

    # this creates a neural network (phenotype) from the genome
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)

    # let's input just one pattern to the net, activate it once and get the output
    net.Input( [ 100, 5.0, 0.1, 3.0, 1.0 ] )
    net.Activate()
    output = net.Output()

    fitness = scene_loading.run_test(client_id, speed=100, kp=5, ki=0.2, kd=1)

    # fitness = 1.0 - output[0]
    return fitness

def run():
    for generation in range(100): # run for 100 generations

        # retrieve a list of all genomes in the population
        genome_list = NEAT.GetGenomeList(population)

        # apply the evaluation function to all genomes
        for genome in genome_list:
            fitness = evaluate(genome)
            genome.SetFitness(fitness)

        # at this point we may output some information regarding the progress of evolution, best fitness, etc.
        # it's also the place to put any code that tracks the progress and saves the best genome or the entire
        # population. We skip all of this in the tutorial.
        print(fitness)
        # advance to the next generation
        population.Epoch()


### Starting point ###
client_id = scene_loading.init_connection_scene(path="..\\ackerman_car.ttt") # path to scene
run()
scene_loading.close_connection_scene(client_id)

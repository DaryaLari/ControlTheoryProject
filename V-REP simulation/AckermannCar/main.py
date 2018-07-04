import csv

from simulationEnvironment import connections
import TestDataGenerator
from NeatEngine import NeatTester
from car_controllers import PidController, NeatController, sensor_type_vision, sensor_type_proximity

path_to_scene = '.\\V-REP_scenes\\ackerman_car_complicated.ttt'


def export_data(params):
    with open("results/results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(params)


def run_test_engine():
    test_gen = TestDataGenerator.TestDataGenerator(
        [ # [start_value, end_value, step_size]
            [50, 150, 5],   # speed
            [0, 10, 1],     # kp
            [0.1, 1, 0.1],  # ki
            [0, 5, 1]       # kd
        ])
    while test_gen.has_next():
        [t_speed, t_kp, t_ki, t_kd] = test_gen.get_test_case()
        print("\n-------------------------"
              + "\n| Speed: " + str(t_speed)
              + "\n| Kp: " + str(t_kp)
              + "\n| Ki: " + str(t_ki)
              + "\n| Kd: " + str(t_kd)
              + "\n---")
        t_time = connections.run_test(
            PidController.PidController(
                t_kp, t_ki, t_kd, t_speed,
                sensor_type_vision,
                time_limit=750
            ),
            log_errors=False
        )
        print("---"
              + "\n| Sim. time: " + str(t_time)
              + "\n-------------------------")
        export_data([[t_speed, t_kp, t_ki, t_kd, t_time]])


def run_neat_tests():
    from NeatEngine.fitness_functions import distance

    def controller_init_function(controller):
        controller.sensor_type = sensor_type_vision
        controller.time_limit = 750
    nt = NeatTester.NeatTester(
        fitness_function=distance,
        controller_type=NeatController.NeatController,
        controller_init_function=controller_init_function,
        gen_amount=100,
        resdir="results/vision-1",
        restore_gen=20
    )
    if nt.population is not None:
        nt.run()


def run_single_test():
    kp = 10
    ki = 0.1
    kd = 3
    base_speed = 50
    print("\n-------------------------"
          + "\n| Speed: " + str(base_speed)
          + "\n| Kp: " + str(kp)
          + "\n| Ki: " + str(ki)
          + "\n| Kd: " + str(kd)
          + "\n---")
    from car_controllers import UniversalController
    sim_time = connections.run_test(
        PidController.PidController(
            kp, ki, kd,
            base_speed,
            sensor_type=sensor_type_vision,
            time_limit=-1
        ),
        log_errors=True
    )
    print("---"
          + "\n| Sim. time: " + str(sim_time)
          + "\n-------------------------")


def run_best_genome():
    from NeatEngine.utils import get_net_of_best_genome
    net = get_net_of_best_genome('results/vision-1/checkpoints/neat-checkpoint-20', 'results/vision-1/config-neat')
    sim_time = connections.run_test(
        NeatController.NeatController(
            net=net,
            sensor_type=sensor_type_vision,
            time_limit=-1
        ),
        log_errors=False
    )
    print("Sim. time: " + str(sim_time))


def run_program():
    client_id = connections.init_connection_scene(path=path_to_scene)
    if client_id == -1:
        print("Error occured. Terminate program")
        exit(-1)

    run_single_test()
    # run_test_engine()
    # run_neat_tests()
    # run_best_genome()

    connections.close_connection_scene()


### Starting  point ###
run_program()
#######################

import csv

import simulation
import TestDataGenerator
from NEAT_engine import NEAT_Tester


def export_data(params):
    with open("tests_results/results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(params)


def run_test_engine(client_id):
    test_gen = TestDataGenerator.TestDataGenerator(
        [ # [start_value, end_value, step_size]
            [50, 150, 5],   # speed
            [0, 10, 1],     # kp
            [0.1, 1, 0.1],  # ki
            [0, 5, 1]       # kd
        ])
    while test_gen.has_next():
        [t_speed, t_kp, t_ki, t_kd] = test_gen.get_test_case()
        t_time = simulation.run_test(client_id, t_speed, t_kp, t_ki, t_kd, log_errors=False, time_limit=1500)
        export_data([[t_speed, t_kp, t_ki, t_kd, t_time]])


def run_NEAT_tests(client_id):
    NEAT_Tester.init_tester(
        c_id=client_id,
        time_limit=750,
        gen_amount=100
    )
    NEAT_Tester.run()


def run_simple_test(client_id):
    simulation.run_test(client_id, speed=50, kp=25, ki=0.1, kd=3, log_errors=True, time_limit=-1)


def run_program():
    client_id = simulation.init_connection_scene(path="..\\ackerman_car_with_walls (1).ttt") # path to scene
    # export_data([["speed", "kp", "ki", "kd", "time"]])

    # run_simple_test(client_id)
    # run_test_engine(client_id)
    run_NEAT_tests(client_id)

    simulation.close_connection_scene(client_id)


### Starting  point ###
run_program()
#######################

import csv
import simulation
import TestDataGenerator
import NEAT_Tester


def export_data(params):
    with open("tests_results/results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(params)


def run_test_engine(client_id):
    test_gen = TestDataGenerator.TestDataGenerator(
        [ # [start_value, end_value, step_size]
            [80, 150, 5], # speed
            [3, 10, 1], # kp
            [0.1, 0.1, 0.1], # ki
            [1, 5, 1] # kd
        ])
    while test_gen.has_next():
        [t_speed, t_kp, t_ki, t_kd] = test_gen.get_test_case()
        t_time = simulation.run_test(client_id, t_speed, t_kp, t_ki, t_kd, log_errors=False, time_limit=1500)
        export_data([[t_speed, t_kp, t_ki, t_kd, t_time]])


def run_NEAT_tests(client_id):
    NEAT_Tester.init_tester(
        c_id=client_id,
        borders=[
            [75, 250],
            [0, 25],
            [0, 2.5],
            [0, 20]
        ],
        default_p=[100, 5, 0.1, 1],
        time_limit=750,
        gen_amount=100
    )
    NEAT_Tester.run()


def run_simple_test(client_id):
    simulation.run_test(client_id, speed=100, kp=5, ki=0.1, kd=1, log_errors=True, time_limit=-1)


def run_program():
    client_id = simulation.init_connection_scene(path="..\\ackerman_car.ttt") # path to scene

    # export_data([["speed", "kp", "ki", "kd", "time"]])
    # run_simple_test(client_id)
    # run_test_engine(client_id)
    run_NEAT_tests(client_id)

    simulation.close_connection_scene(client_id)


### Starting  point ###
run_program()
#######################

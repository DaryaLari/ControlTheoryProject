import csv
import scene_loading
import TestDataGenerator
import NEAT_Tester


def export_data(params):
    with open("tests_results/results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(params)


def run_test_engine(client_id):
    # params = [] # [0] - speed, [1] - kp, [2] - ki, [3] - kd, [4] - sim_time
    test_gen = TestDataGenerator.TestDataGenerator(#
        [ # [start_value, end_value, step_size]
            [80, 150, 5], # speed
            [3, 10, 1], # kp
            [0.1, 0.1, 0.1], # ki
            [1, 5, 1] # kd
        ])
    while test_gen.has_next():
        [t_speed, t_kp, t_ki, t_kd] = test_gen.get_test_case()
        t_time = scene_loading.run_test(client_id, t_speed, t_kp, t_ki, t_kd, log_errors=False)
        export_data([[t_speed, t_kp, t_ki, t_kd, t_time]])
        # params.append([t_speed, t_kp, t_ki, t_kd, t_time])


def run_NEAT_tests(client_id):
    neatTester = NEAT_Tester.NEAT_Tester()
    NEAT_Tester.client_id = client_id
    neatTester.run()

def run_simple_test(client_id):
    scene_loading.run_test(client_id, speed=100, kp=5, ki=0.1, kd=1, log_errors=True)


def run_program():
    client_id = scene_loading.init_connection_scene(path="..\\ackerman_car_with_additional_paths_1.ttt") # path to scene

    # export_data([["speed", "kp", "ki", "kd", "time"]])
    # run_test_engine(client_id)
    # run_simple_test(client_id)
    run_NEAT_tests(client_id)

    scene_loading.close_connection_scene(client_id)


### Starting  point ###
run_program()
#######################

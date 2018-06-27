import csv

from simulationEnvironment import simulation
import TestDataGenerator
from NeatEngine import NeatTester
from car_controllers import PidController, sensor_type_vision, sensor_type_proximity

path_to_scene = "..\\ackerman_car.ttt"


def export_data(params):
    with open("results/results.csv", "a", newline="") as file:
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
        print("\n-------------------------"
              + "\n| Speed: " + str(t_speed)
              + "\n| Kp: " + str(t_kp)
              + "\n| Ki: " + str(t_ki)
              + "\n| Kd: " + str(t_kd)
              + "\n---")
        t_time = simulation.run_test(
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


def run_NEAT_tests(client_id):
    nt = NeatTester.NeatTester(
        c_id=client_id,
        gen_amount=100,
        resdir="results-vision-2",
        restore_gen=-1,
        sensor_type=sensor_type_vision,
        time_limit=750
    )
    if nt.population is not None:
        nt.run()


def run_simple_test():
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
    sim_time = simulation.run_test(
        PidController.PidController(
            kp, ki, kd,
            base_speed, sensor_type=sensor_type_vision,
            time_limit=-1
        ),
        log_errors=True
    )
    print("---"
          + "\n| Sim. time: " + str(sim_time)
          + "\n-------------------------")

def run_program():
    client_id = simulation.init_connection_scene(path=path_to_scene)
    if client_id == -1:
        print("Error occured. Terminate program")
        exit(-1)

    # run_simple_test()
    # run_test_engine(client_id)
    run_NEAT_tests(client_id)

    simulation.close_connection_scene()


### Starting  point ###
run_program()
#######################

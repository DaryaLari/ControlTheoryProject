Contains V-REP simulation scene file with line-following Ackerman car. 
The algorithm is implemented on Python using V-REP remote API. 

Report can be found in `ControlTheoryProject/documentation/Report.pdf` file.

The script can be found in 
`ControlTheoryProject/V-REP simulation/AckermannCar` folder.

# Line-following Ackermann car

To run the project, clone `ControlTheoryProject/V-REP simulation/AckermannCar` folder to your computer.

Check V-REP remote api settings (i.e. the port number in configuration file is the same, as specified in `simulationEnvironment/connections.py`).
Additional information can be found here: 
http://www.coppeliarobotics.com/helpFiles/en/remoteApiServerSide.htm

Also check settings from following page:
http://www.coppeliarobotics.com/helpFiles/en/remoteApiClientSide.htm

Launch V-REP application.
Then run `main.py` file.

## Handling car movement

An interface for moving the car and reading sensors data is provided in `simulationEnvironment/AckermannCar.py`.

You can use following methods of `AckermannCar` instance:
- `read_vision_sensors_intensity()` which returns intensity values read from left, middle and right vision sensor respectively
- `read_proximity_sensors()` which returns destination read from right, middle and left proximity sensor respectively
- `set_rotation_angle(base_angle)` for setting steering angle value (in radians)
- `set_speed(speed)` sets speed to front motors

For running a car you can use one of controllers, provided in `car_controllers` package 
or create the own one that would have implementation of following methods:
- `set_driven_car(car)`
- `drive_car()`

## How to run different algorithms

In `main.py` file `run_program()` function uncomment one of the following lines:
- `run_single_test()` for running single test
- `run_test_engine()` for running bunch of tests with predefined range of tested parameters 
(PID controller's coefficients and car speed)
- `run_neat_tests()` for running tests with NEAT algorithm
- `run_best_genome()` for running simulation with neural network of the fittest genome from certain generation

## Algorithms running options examples

### `run_single_test()`

This function runs one test with `PidController`.

### `run_test_engine()`

It runs several tests with `PidController` using all possible combinations of parameters from specified ranges.

### `run_neat_tests()`

It runs NEAT algorithm, which selects suitable neural network for driving Ackermann car

### `run_best_genome()`

It restores specified generation from checkpoint (created by NEAT algorithm), 
gets a neural network of the best genome and runs simulation with `NeatController` using this network

## Controllers description

### `UniversalController`
It is a simple controller for line-following car.
Implementation of function `drive_car()` from this class is used by `PidController` and `NeatController`
For using `UniversalController` you can specify:
- type of sensors used by controller for checking relative car position:
    - `sensor_type_vision`
    - `sensor_type_proximity`
- limit of simulation time (in sec) or not restrict it by setting `time_limit = -1`

### `PidController`
For this type of controller you should provide:
- PID coefficients (`kp`, `ki`, `kd`)
- speed of the car (`base_speed`)
- sensor type(as in `UniversalController`)

### `NeatController`
For this type of controller you should provide:
- neural network (`net`)
- sensor type(as in `UniversalController`)

Also you can set your own range of parameters resulted by net.
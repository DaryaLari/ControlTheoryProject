"ControlTheoryProject" 

Contains V-REP simulation scene file with line-following Ackerman car. 
The algorithm (based on PID controller) is implemented on Python using V-REP remote API. 

Report can be found in "ControlTheoryProject/documentation/Report.pdf" file.

The script can be found in 
"ControlTheoryProject/V-REP simulation/ackerman car/code" folder.

To start the program run "main.py" script.

It has 3 options. To choose one of them uncomment following lines in "main.py" -> "run_program()":
- run_simple_test(client_id) // for running single test
- run_test_engine(client_id) // for running banch of tests with predefined range
- run_NEAT_tests(client_id) // for running tests with genetic algorithm
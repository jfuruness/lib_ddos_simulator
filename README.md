# lib\_ddos\_simulator
This package contains functionality to simulate, graph, and animate various attack/defense scenarios for DDOS attacks. It is also easily extendable to allow for easy testing of defense techniques. The purpose of this library is to determine which DDOS defense techniques from published literature work the best in practice.

* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Description](#package-description)
* [Simulation Setup](#simulation-setup)
* [Usage](#usage)
    * [Running One Scenario](#running-one-scenario)
    * [Running Manager Comparisons](#running-manager-comparisons)
    * [API (currently in development)](#api)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
    * [Adding a Manager (to be written)](#adding-a-manager)
    * [Adding an Attacker (to be written)](#adding-a-attacker)
* [History](#history)
* [Credits](#credits)
* [Licence](#licence)
* [Todo and Possible Future Improvements](#todopossible-future-improvements)
* [FAQ](#faq)
* Developer Notes (to be written)
    * Simulation Script
    * Managers
        * Manager (Base class)
        * Bounded Manager
        * KPO Manager
        * Miad Manager
        * Protag Manager
        * Sieve Manager
    * Graphers
        * Animater
        * Grapher
        * Combination_Grapher
    * Attackers
        * Attacker (Base)
        * Basic Attacker
        * Lone Attacker
        * Even Turn Attacker
        * Fifty Percent Attacker
        * Ten Percent Attacker
        * Wait for x addition Attacker
        * Mixed Attacker
    * Simulation Objects
        * User
        * Bucket
    * Utils
        * Logging
## Package Description
* [lib\_ddos\_simulator](#lib_ddos_simulator)

There are 5 main sections to this python package. Managers, Graphers, Attackers, Users, and Utils. Manager is the term used to describe a defense technique - essentially, the manager of the system. Graphers collect data from the simulation and turn it into a readable format. Attackers contain the different types of attackers. Users contain the different types of users. Utils contains auxiliary functions that may be useful across all categories.

The simulator is the main script in the package, called ddos_simulator. You can pass several arguments into the simulator that will allow you to run any attack or defense scenario. You can also use the graphers, which call the simulator several times to compare statistics for many scenarios. Usage details below.

## Simulation Setup
* [lib\_ddos\_simulator](#lib_ddos_simulator)

The simulation works like the following:
1. Simulation is initialized with arguments to specify attack/defense scenario (see [Usage](#usage))
2. Users and attackers are shuffled together
3. Managers are initialized with the same starting configuration of users
4. Each turn, buckets are attacked
5. Each turn, the grapher captures the data
6. Each turn, the manager detects attackers and shuffles (according to that manager's algorithm
7. Each turn, all buckets are reset
8. The grapher represents the data after all turns are complete

Assumptions:
* Static set of users
* No maximum capacity to a bucket
* Managers have unlimited number of potential buckets

## Usage
* [lib\_ddos\_simulator](#lib_ddos_simulator)

There are three ways to run this package. 

1. Gather statistics per round (cost, percent serviced, utility, percent detected), for each manager specified
2. At the end of all the rounds, gather the utility of the manager and compare it with all other managers
3. Use the API to manage live users (and protect from DDOS attacks)

### Running One Scenario
* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Usage](#usage)

This way of running the simulator will chart (for each manager) cost, percent serviced, utility, percent detected, etc. for every round.

#### From the command line:
```bash
lib_ddos_simulator
```
with some additional parameters:
```bash
lib_ddos_simulator --num_users 9 --num_attackers 1 --num_buckets 3 --debug
```

#### Optional command line parameters:
| Parameter  | Default                    | Description                                                                                        |
|------------|----------------------------|----------------------------------------------------------------------------------------------------|
| num_users      | 1000     | Number of good users |
| num_attackers  | 10       | Number of attackers  |
| num_buckets    | 100      | Number of buckets    |
| threshold      | 10       | Threshold for suspicion removal. Legacy code.                                          |
| rounds         | 20       | Number of rounds to run |
| debug          | False    | Display debug info   |
| animate        | False    | Save animations (not used here)|
| graph_combos   | False    | Compares manager's utilities (not used here)|


#### From a script:

> Note the optional parameters included below
> These are all the possible parameters to supply

```python
import logging
from lib_ddos_simulator import DDOS_Simulator, Protag_Manager, Basic_Attacker
num_users = 10
num_attackers = 1
num_buckets = 5
# Threshold is legacy code
threshold = .1
# All the managers to run. See manager section for a list
manager_child_classes = [Protag_Manager]
# The following options are the defaults, you can omit
# these or change them if you wish
stream_level = logging.INFO
graph_path = "/tmp/lib_ddos"
# The type of attacker. See attacker section for a list
attacker_cls = Basic_Attacker
sim = DDOS_Simulator(num_users,
                     num_attackers,
                     num_buckets,
                     threshold,
                     manager_child_classes,
                     stream_level=stream_level,
                     graph_path=graph_path,
                     attacker_cls=attacker_cls)
# Num rounds can be changed as needed
num_rounds = 10
sim.run(num_rounds)
```



### Running Manager Comparisons
* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Usage](#usage)

This way of running the simulator will chart (for each scenario) the utility over all the rounds, and will chart all managers on one plot. The X axis will be percentage of users that are attackers.

#### From the command line:
```bash
lib_ddos_simulator --graph_combos
```
To display debug info:
```bash
lib_ddos_simulator --debug
```
There are no optional parameters other than debugging for command line, they seemed unnecessary

#### From a script:

> Note the optional parameters included below
> These are all the possible parameters to supply

```python
import logging
from lib_ddos_simulator import Combination_Grapher, Sieve_Manager, Attacker

# stream_level and graph_path defaults, can be omitted
grapher = Comination_Grapher(stream_level=logging.INFO,
                             graph_path="/tmp/lib_ddos")

# For the full list of managers that is run by default, see Managers section
grapher.run(managers=Sieve_Manager.runnable_managers,
            attackers=Attacker.runnable_attackers,
            num_bucket_list=[10],
            users_per_bucket_list=[10 ** i for i in range(1,3)],
            num_rounds_list=[10 ** i for i in range(1,3)],
            trials=100)

# NOTE: If you are confused by these lists, what gets graphed is essentially:
# for num_buckets in num_buckets_list:
#     for users_per_bucket in users_per_bucket_list:
#         for num_rounds in num_rounds_list:
#             for attacker in attackers:
#                  generate_graph(managers, trials)
```



### API
* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Usage](#usage)

Currently in development



## Installation
* [lib\_ddos\_simulator](#lib_ddos_simulator)

As far as system requirements goes, I run this off my laptop. The more cores, the faster the combination_grapher will run, although it only parallelizes by scenario. I use Linux, it's possible it will work on other OSes, although the graph paths would probably have to be changed.

Install python and pip if you have not already. Then run:

```bash
pip3 install wheel
pip3 install lib_ddos_simulator
```
This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/lib_ddos_simulator.git
cd lib_ddos_simulator
pip3 install wheel
pip3 install -r requirements.txt --upgrade
python3 setup.py develop
```

To test the development package, cd into the root directory and run pytest.


## Testing
* [lib\_ddos\_simulator](#lib_ddos_simulator)

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
```sudo python3 setup.py test```

To test a specific submodule, run pytest --markers. Then you can run pytest -m <submodule_name> and only tests from that submodule will be run.

Also note that slow tests are marked as slow. So you can not run slow tests by doing pytest -m "not slow".

All the skipped tests are for the interns to fill in. I have completed these tests manually and am confident they will succeed, and I have been told by my bosses to move on to other tasks.

## Development/Contributing
* [lib\_ddos\_simulator](#lib_ddos_simulator)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because idk how to even check those messages

### Adding a Manager
* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Development/Contributing](#developmentcontributing)

To be written

### Adding an Attacker
* [lib\_ddos\_simulator](#lib_ddos_simulator)
* [Development/Contributing](#developmentcontributing)

To be written


## History
* [lib\_ddos\_simulator](#lib_ddos_simulator)
   * 0.0.0 - Basic simulation capabilities, no API

## Credits
* [lib\_ddos\_simulator](#lib_ddos_simulator)

Many thanks to Anna Gorbenko for helping code the managers with me as well as other parts of this library, as well as lots of DDOS theory

Many thanks to Amir Herzberg for direction in research and help with DDOS theory as well as coming up with many improvements

Thanks to the Nikhil for working with us to test out the API portion of this library for deployment

Many thanks to all the stack overflow questions and sites that have helped in development of this package:
* https://stackoverflow.com/a/16910957/8903959
* https://stackoverflow.com/a/4701285/8903959
* https://stackoverflow.com/a/48958260/8903959
* https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/gradient_bar.html
* https://stackoverflow.com/a/43057166/8903959
* http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
* https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/custom_legends.html
* https://riptutorial.com/matplotlib/example/32429/multiple-legends-on-the-same-axes
* https://stackoverflow.com/a/26305286/8903959
* https://stackoverflow.com/a/1987484/8903959

Also thanks to the pathos library. Amazing way to multiprocess.

## License
* [lib\_ddos\_simulator](#lib_ddos_simulator)

Four Clause BSD License (see license file)

## TODO/Possible Future Improvements
* [lib\_ddos\_simulator](#lib_ddos_simulator)



See [Jira Board](https://wkkbgp.atlassian.net/jira/software/projects/PYTHON/boards/15?label=DDOS)

## FAQ
* [lib\_ddos\_simulator](#lib_ddos_simulator)

Q: More links to some research

A: Read these:


# Project Title: NEAT-Based AI for Flappy Bird

## Description

This project implements a NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve neural networks to play a flappy bird game. The project uses the `neat-python` library to train a population of neural networks.

## Usage

To run the project and start the NEAT algorithm with the bird game simulation, use the following command:

```sh
python main.py
```

To run the best genome, use the following command:

```sh
python main.py run_best
```

## Configuration

The behavior and performance of the NEAT algorithm can be adjusted using the `config-feedforward.txt` file. Below are some of the key parameters:

- **Population Size (`pop_size`)**: Number of neural networks in each generation. Default is 50.
- **Fitness Threshold (`fitness_threshold`)**: The fitness level required to stop the evolution. Default is 1000000.0.
- **Mutation Rates**: Various rates for mutating network weights, biases, and structure.
- **Network Structure**: Parameters defining the initial network structure and how it can change over time.

Here is a sample of the configuration file:

```ini
[NEAT]
fitness_criterion     = max
fitness_threshold     = 1000000.0
pop_size              = 50
reset_on_extinction   = False

[DefaultGenome]
activation_default      = tanh
activation_mutate_rate  = 0.1
aggregation_default     = sum
bias_init_mean          = 0.0
bias_init_stdev         = 1.0
conn_add_prob           = 0.5
conn_delete_prob        = 0.5
enabled_default         = True
enabled_mutate_rate     = 0.01
feed_forward            = True
initial_connection      = full_direct
node_add_prob           = 0.2
node_delete_prob        = 0.2
num_hidden              = 0
num_inputs              = 3
num_outputs             = 1
weight_init_mean        = 0.0
weight_init_stdev       = 1.0
weight_mutate_power     = 0.5
weight_mutate_rate      = 0.8
```

## Acknowledgements

This project is inspired by and uses techniques from [this article](https://medium.com/analytics-vidhya/how-i-built-an-ai-to-play-flappy-bird-81b672b66521).

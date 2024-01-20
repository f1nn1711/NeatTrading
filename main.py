import sys
from myneat import NEAT
import json
from Trading212 import Trading212
from DataProcessor import ProcessorV1
import os
from helpers.listHelpers import argMax
import neat
import multiprocessing
import pickle


runs_per_net = 2


def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = 0

    # replace with for each element in the test data
    for runs in range(runs_per_net):
        env = gym.make("BipedalWalker-v3")

        observation = None # get the next test data


        action = net.activate(observation)

        # check the result
        fitnesses.append(fitness)

    return fitnesses / 1 # Replace with number of datapoints


def autoTrain():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '/storage/configs/config')

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, 10)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)


def train():
    print('Generating population')
    with open('config.json', 'r') as file:
        config = json.loads(file.read())

    with open('storage/datasets/' + config['trainingData'], 'r') as file:
        dataset = json.loads(file.read())

    controller = NEAT(config)
    for generation in range(config['generations']):
        for agent in controller.getPopulation():
            correctCount = 0
            for datapoint, correctResponse in zip(dataset['XTrain'], dataset['yTrain']):
                response = agent.getNetworkResponse(datapoint)

                if argMax(response) == argMax(correctResponse):
                    correctCount += 1

            agent.setFitness(correctCount / len(dataset['XTrain']))

        controller.generateEvolvedPopulation()


    # for each gen
    #   for each agent
    #       agent.getNetworkResponse(obs)
    #       set the fitness of the agent
    #   call generateEvolvedPopulation to set new population

    return


def getData(ticker):
    connection = Trading212()
    responseData = connection.getTickerData(ticker, 'TEN_MINUTES')
    print(responseData)  # use 25 to 45 last periods

    return


def generateData(tickers):
    processor = ProcessorV1(Trading212())
    processor.generateData(tickers, output=os.path.abspath(os.getcwd()) + '/storage/datasets/datasetV1.json')

    return


def main():
    arguments = sys.argv

    if len(arguments) == 1:
        return

    match arguments[1]:
        case 'train':
            return train()
        case 'help':
            print('Enter an option to run that function, this was helpful.')
        case 'getData':
            return getData(arguments[2])
        case 'generateData':
            return generateData(arguments[2])
        case _:
            print('Option not found')


if __name__ == '__main__':
    main()

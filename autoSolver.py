
from __future__ import print_function
from numpy import *
from ortools.graph import pywrapgraph


infinite = 100
price = 1

def main():

    counter = 0 #how many were successful

    #Change these parameters
    days = 3
    segments = 2 #I've defined segment to be the number of time slots between cycles, so there are 2*segment intervals in a day
    nodes = 3
    initialBikes = 10 #at each node
    maxMovement = 8
    numberOfTrials = 1000

    for trial in range(0, numberOfTrials):
        startingBikes = full((nodes), initialBikes)
        totalBikes = sum(startingBikes)

        bikeData = random.random_integers(0, maxMovement, size=(2*segments*days, nodes, nodes))
        for i in range (0, 2*segments*days):
            for j in range (0, nodes):
                bikeData[i][j][j] = 0

        inBikes = sum(bikeData, axis=1)

        min_cost_flow = pywrapgraph.SimpleMinCostFlow()


        start(min_cost_flow, nodes, startingBikes)
        offset = nodes
        for i in range(0, 2*segments*days):
            if(i % segments == 0):
                costCycle(min_cost_flow, nodes, offset)
                offset = offset + nodes
            freeCycle(min_cost_flow, nodes, offset, i, bikeData, inBikes)
            offset = offset + 3 * nodes
        end(min_cost_flow, nodes, offset, totalBikes)


        if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
            counter = counter + 1

    print('Finished\n %1s / %2s successful' % (counter, numberOfTrials))


def start(graph, size, data):
    #print("\nStarting start")
    for i in range(0, size):
        #print('Node %1s with supply %2s' % (i, data[i]))
        graph.SetNodeSupply(i, data[i])

def freeCycle(graph, size, offset, time, data, sumData):
    #print("\nStarting freeCycle")
    for i in range(0, size):
        #print('Node %1s with supply %2s' % ( offset+i, -1*sumData[time][i]))
        graph.SetNodeSupply(offset+i, -1*sumData[time][i].item())
        #print('Node %1s with supply %2s' % ( offset+i+size, sumData[time][i]))
        graph.SetNodeSupply(offset+i+size, sumData[time][i].item())
        #print('Node %1s with supply %2s' % ( offset+i+2*size, 0))
        graph.SetNodeSupply(offset+i+2*size, 0)

        #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + i + 2*size, infinite, 0))
        graph.AddArcWithCapacityAndUnitCost(offset -size + i, offset + i + 2*size, infinite, 0)

        for j in range (0, size):
            if(j != i):
                #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset + i - size, offset + j, data[time][i][j], 0))
                graph.AddArcWithCapacityAndUnitCost(offset + i - size, offset + j, data[time][i][j].item(), 0)

        #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (i + offset + size, i + offset + 2*size, infinite, 0))
        graph.AddArcWithCapacityAndUnitCost(i + offset + size, i + offset + 2*size, infinite, 0)

def costCycle(graph, size, offset):
    #print("\nStarting cost cycle")
    for i in range(0, size):
        #print('Node %1s with supply %2s' % ( offset+i, 0))
        graph.SetNodeSupply(offset+i, 0)
        for j in range(0, size):
            if(i == j):
                #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + j, infinite, 0))
                graph.AddArcWithCapacityAndUnitCost(offset - size + i, offset + j, infinite, 0)
            else:
                #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + j, infinite, price))
                graph.AddArcWithCapacityAndUnitCost(offset - size + i, offset + j, infinite, price)

def end(graph, size, offset, totalBikes):
    #print("\nStarting end")
    graph.SetNodeSupply(offset, -1* totalBikes.item())
    for i in range(0, size):
        #print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset + i - size, offset, infinite, 0))
        graph.AddArcWithCapacityAndUnitCost(offset + i - size, offset, infinite, 0)

if __name__ == '__main__':
  main()

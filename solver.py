
from __future__ import print_function
from numpy import *
from ortools.graph import pywrapgraph


infinite = 100
price = 1

def main():
    setupData = loadtxt("input1.txt").astype(int)
    days = setupData[0].item()
    segments = setupData[1].item() #number of intervals between costCycles
    nodes = setupData[2].item()
    startingBikes = delete(setupData, [0,1,2])
    totalBikes = sum(startingBikes)

    bikeData = reshape(loadtxt("input2.txt").astype(int), (2*segments*days, nodes, nodes))
    inBikes = sum(bikeData, axis=1)

    min_cost_flow = pywrapgraph.SimpleMinCostFlow()


    start(min_cost_flow, nodes, startingBikes)
    offset = nodes
    for i in range(0, 2*segments*days):
        if(i % segments == 0):
            costCycle(min_cost_flow, nodes, offset)
            offset = offset + nodes
        freeCycle(min_cost_flow, nodes, offset, i, bikeData, inBikes)
        offset = offset + 2 * nodes
    end(min_cost_flow, nodes, offset, totalBikes)




    print(min_cost_flow.NumArcs())

    if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
        print('Minimum cost:', min_cost_flow.OptimalCost())
        print('')
        print('  Arc    Flow / Capacity  Cost')
        for i in range(min_cost_flow.NumArcs()):
            cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
            print('%1s -> %1s   %3s  / %3s       %3s' % (
                min_cost_flow.Tail(i),
                min_cost_flow.Head(i),
                min_cost_flow.Flow(i),
                min_cost_flow.Capacity(i),
                cost))
    else:
        print('There was an issue with the min cost flow input.')
        print('  Arc    Capacity  Cost')
        for i in range(min_cost_flow.NumArcs()):
            print('%1s -> %2s   %3s  %4s' % (
                min_cost_flow.Tail(i),
                min_cost_flow.Head(i),
                min_cost_flow.Capacity(i),
                min_cost_flow.UnitCost(i),
            ))
        print('\n')
        print('  Node   Supply')
        for i in range(min_cost_flow.NumNodes()):
            print('%1s : %2s' % (i, min_cost_flow.Supply(i)))


def start(graph, size, data):
    print("\nStarting start")
    for i in range(0, size):
        print('Node %1s with supply %2s' % (i, data[i].item()))
        graph.SetNodeSupply(i, data[i].item())

def freeCycle(graph, size, offset, time, data, sumData):
    print("\nStarting freeCycle")
    for i in range(0, size):
        print('Node %1s with supply %2s' % ( offset+i, -1*sumData[time][i]))
        graph.SetNodeSupply(offset+i, -1*sumData[time][i].item())
        print('Node %1s with supply %2s' % ( offset+i+size, sumData[time][i]))
        graph.SetNodeSupply(offset+i+size, sumData[time][i].item())
        # print('Node %1s with supply %2s' % ( offset+i+2*size, 0))
        # graph.SetNodeSupply(offset+i+2*size, 0)

        print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + i + size, infinite, 0))
        graph.AddArcWithCapacityAndUnitCost(offset - size + i, offset + i + size, infinite, 0)

        for j in range (0, size):
            if(j != i):
                print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset + i - size, offset + j, data[time][i][j], 0))
                graph.AddArcWithCapacityAndUnitCost(offset + i - size, offset + j, data[time][i][j].item(), 0)

        # print('Arc from %1s to %2s with capacity %3s and cost %4s' % (i + offset + size, i + offset + 2*size, infinite, 0))
        # graph.AddArcWithCapacityAndUnitCost(i + offset + size, i + offset + 2*size, infinite, 0)

def costCycle(graph, size, offset):
    print("\nStarting cost cycle")
    for i in range(0, size):
        print('Node %1s with supply %2s' % ( offset+i, 0))
        graph.SetNodeSupply(offset+i, 0)
        for j in range(0, size):
            if(i == j):
                print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + j, infinite, 0))
                graph.AddArcWithCapacityAndUnitCost(offset - size + i, offset + j, infinite, 0)
            else:
                print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset - size + i, offset + j, infinite, price))
                graph.AddArcWithCapacityAndUnitCost(offset - size + i, offset + j, infinite, price)

def end(graph, size, offset, totalBikes):
    print("\nStarting end")
    graph.SetNodeSupply(offset, -1* totalBikes.item())
    for i in range(0, size):
        print('Arc from %1s to %2s with capacity %3s and cost %4s' % (offset + i - size, offset, infinite, 0))
        graph.AddArcWithCapacityAndUnitCost(offset + i - size, offset, infinite, 0)

if __name__ == '__main__':
  main()


from __future__ import print_function
from numpy import *
from ortools.graph import pywrapgraph

setupData = loadtxt("input1.txt").astype(int)
days = setupData[0]
segments = setupData[1]
nodes = setupData[2]
startingBikes = delete(setupData, [0,1,2,3])
capacity = 10000
price = 1

bikeData = reshape(loadtxt("input2.txt").astype(int), (4, 3, 3))
outBikes = sum(bikeData, axis=2)
inBikes = sum(bikeData, axis=1)

min_cost_flow = pywrapgraph.SimpleMinCostFlow()

slots = days*(2*segments + 2)

# for i in range(0, slots):
#     min_cost_flow.AddArcWithCapacityAndUnitCost(3*i, 3*(i+1), capacity, 0)
#     min_cost_flow.AddArcWithCapacityAndUnitCost(3*i+1, 3*(i+1)+1, capacity, 0)
#     min_cost_flow.AddArcWithCapacityAndUnitCost(3*i+2, 3*(i+1)+2, capacity, 0)


# for i in range(0, nodes):
#     min_cost_flow.SetNodeSupply(i, startingBikes[i].item())


start_nodes = [ 0, 0,  0, 1, 1,  1, 2, 2,  2,  6,  7,  8,  9,  9,  9, 12, 12, 12, 13, 13, 13, 14, 14, 14, 18, 19, 20, 21, 22, 23 ]
end_nodes =   [ 4, 5,  9, 3, 5, 10, 3, 4, 11,  9, 10, 11, 12, 13, 14, 16, 17, 21, 15, 17, 22, 15, 16, 23, 21, 22, 23, 24, 24, 24 ]
capacities =  [ 0, 0, 90, 1, 4, 90, 2, 0, 90, 90, 90, 90, 90, 90, 90,  2,  0, 90,  3,  1, 90,  0,  0, 90, 90, 90, 90, 90, 90, 90 ]
unit_costs =  [ 0, 0,  0, 0, 0,  0, 0, 0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]

supplies = [
    5, 5, 5,
    -3, 0, -4,
    3, 0, 4,
    0, 0, 0,
    -3, -2, -1,
    3, 2, 1,
    0, 0, 0,
    0, 0, 0,
    -15,
]

# start_nodes = [ 0, 0, 1, 1, 2, 2, 3, 3, 6, 7,  8,  9 ]
# end_nodes   = [ 2, 3, 2, 3, 5, 8, 4, 9, 8, 9, 10, 10 ]
# capacities  = [ 9, 9, 9, 9, 3, 9, 2, 9, 9, 9,  9,  9 ]
# unit_costs  = [ 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,  0,  0 ]

# supplies = [ 1, 4, 0, 0, -2, -3, 2, 3, 0, 0, -5]


# Add each arc.
for i in range(0, len(start_nodes)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],
                                            capacities[i], unit_costs[i])

# Add node supplies.

for i in range(0, len(supplies)):
    min_cost_flow.SetNodeSupply(i, supplies[i])


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
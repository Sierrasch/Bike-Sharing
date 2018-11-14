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
print(startingBikes)

slots = days*(2*segments + 2)
print(slots)

for i in range(0, slots):
    min_cost_flow.AddArcWithCapacityAndUnitCost(3*i, 3*(i+1), capacity, 0)
    min_cost_flow.AddArcWithCapacityAndUnitCost(3*i+1, 3*(i+1)+1, capacity, 0)
    min_cost_flow.AddArcWithCapacityAndUnitCost(3*i+2, 3*(i+1)+2, capacity, 0)


for i in range(0, nodes):
    min_cost_flow.SetNodeSupply(i, startingBikes[i])

print(days*(2*segments + 2))
for i in range(nodes, x):
    min_cost_flow.SetNodeSupply(i, 0)



# def main():

# # Define four parallel arrays: start_nodes, end_nodes, capacities, and unit costs
# # between each pair. For instance, the arc from node 0 to node 1 has a
# # capacity of 15 and a unit cost of 4.

#     start_nodes = [ 0, 0,  1, 1,  1,  2, 2,  3, 4]
#     end_nodes   = [ 1, 2,  2, 3,  4,  3, 4,  4, 2]
#     capacities  = [15, 8, 20, 4, 10, 15, 4, 20, 5]
#     unit_costs  = [ 4, 4,  2, 2,  6,  1, 3,  2, 3]

#     # Define an array of supplies at each node.

#     supplies = [20, 0, 0, -5, -15]


#     # Instantiate a SimpleMinCostFlow solver.
#     min_cost_flow = pywrapgraph.SimpleMinCostFlow()

#     # Add each arc.
#     for i in range(0, len(start_nodes)):
#         min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i],
#                                                 capacities[i], unit_costs[i])

#     # Add node supplies.

#     for i in range(0, len(supplies)):
#         min_cost_flow.SetNodeSupply(i, supplies[i])


#     # Find the minimum cost flow between node 0 and node 4.
#     if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:
#         print('Minimum cost:', min_cost_flow.OptimalCost())
#         print('')
#         print('  Arc    Flow / Capacity  Cost')
#         for i in range(min_cost_flow.NumArcs()):
#             cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
#             print('%1s -> %1s   %3s  / %3s       %3s' % (
#                 min_cost_flow.Tail(i),
#                 min_cost_flow.Head(i),
#                 min_cost_flow.Flow(i),
#                 min_cost_flow.Capacity(i),
#                 cost))
#     else:
#         print('There was an issue with the min cost flow input.')

# if __name__ == '__main__':
#     main()
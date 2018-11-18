from ortools.graph import pywrapgraph
import pickle as pkl


def main():
    #for 2 node testing
    metadata = pkl.load(open('metadata', 'rb'))

    # for 3 node testing
    #metadata = pkl.load(open('3nodes_test_metadata', 'rb'))

    nodes = {}
    meta_nodes = []
    start_nodes = []
    end_nodes = []
    capacities = []
    unit_costs = []
    supplies = []
    num_nodes = len(metadata[0])
    tot_supplies = sum(metadata[0])
    time_slots = metadata[1]
    slots_per_day = metadata[2]
    price = metadata[3]
    count = 0

    def tot_transfer(node):
        tot = 0
        for key in receiving_transfer:
            if key == str(node):
                tot += receiving_transfer[key]
        return tot

    def add_edge(start, end, capacity, cost):
        start_nodes.append(start)
        end_nodes.append(end)
        capacities.append(capacity)
        unit_costs.append(cost)
        
    for t in range(time_slots):
        receiving_transfer = {} # Contains the sum of bikes received by each node
        
        #for 2 node testing
        data = pkl.load(open('test_data{}'.format(t), 'rb'))

        # for 3 node testing
        #data = pkl.load(open('3nodes_test{}'.format(t), 'rb'))

        # Read in all nodes to keep track of how many there are
        prior_node = None
        for transfer in data:
            if transfer[0] not in meta_nodes:
                    meta_nodes.append(transfer[0])
            if transfer[0] != prior_node:
                if transfer[0] not in nodes.keys():
                    nodes[transfer[0]+str(t)] = count
                    count += 1
                    nodes[transfer[0]+str(t)+'1'] = count
                    count += 1
                    nodes[transfer[0]+str(t)+'2'] = count
                    count += 1
                    nodes[transfer[0]+str(t)+'f'] = count
                    count += 1
            # Keep track of how many bikes each node receives
            if transfer[1] in receiving_transfer:
                receiving_transfer[transfer[1]] += transfer[2]
            else:
                receiving_transfer[transfer[1]] = transfer[2]
            prior_node = transfer[0]

        # Add supplies to graph
        supplies.extend([0]*4*num_nodes)
        if t == 0:
            for i in range(num_nodes):
                supplies[nodes[meta_nodes[i]+str(t)]] = metadata[0][i]
                
        for i in range(4):
            for node in meta_nodes:
                supplies[nodes[node+str(t)+'1']] = -receiving_transfer[node]
                supplies[nodes[node+str(t)+'2']] = receiving_transfer[node]

        # Add edges to graph
        if t > 0:
            for node in meta_nodes:
                # Add edge from node in previous time to same node in current time
                # Represents bikes which were not moved by users
                add_edge(nodes[node+str(t-1)+'f'],nodes[node+str(t)],10000,0)
                # Add all costly edges where we decide how many bikes to move
                if t%(int(slots_per_day/2)) == 0:
                    for other_node in meta_nodes:
                        if node != other_node:
                            add_edge(nodes[node+str(t-1)+'f'],nodes[other_node+str(t)],10000,price)

        for transfer in data:
            # Add edges where users move the bike
            add_edge(nodes[transfer[0]+str(t)],nodes[transfer[1]+str(t)+'1'],transfer[2],0)

        for node in meta_nodes:
            # Add edge from node to self within the same time
            # Represents bikes which were not moved
            add_edge(nodes[node+str(t)],nodes[node+str(t)+'f'],10000,0)
            # Add edge from receiving node to final node
            # Represents bikes which were 
            add_edge(nodes[node+str(t)+'2'],nodes[node+str(t)+'f'],tot_transfer(node),0)    

        for transfer in data:
            print("Transfer from,to,capacity: {}".format(transfer))

    # Create sink and its edges
    supplies.append(-tot_supplies)
    nodes['Sink'] = count
    for i in range(num_nodes):
        add_edge((count-(i*4)-1), count, 10000,0)

     
    for node in nodes:
        print("Node: {}\tID: {}".format(node,nodes[node]))

    print("Start Nodes: {}".format(start_nodes))
    print("End Nodes: {}".format(end_nodes))
    print("Capacities: {}".format(capacities))
    print("Costs: {}".format(unit_costs))
    print("Supplies: {}".format(supplies))

    # Instantiate a SimpleMinCostFlow solver.
    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

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
            print('%1s -> %1s   %3s  / %3s       %3s' % (min_cost_flow.Tail(i),min_cost_flow.Head(i),min_cost_flow.Flow(i),min_cost_flow.Capacity(i),cost))
    else:
        print('There was an issue with the min cost flow input.')

if __name__ == '__main__':
    main()

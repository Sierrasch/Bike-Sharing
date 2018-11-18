import pickle as pkl

first_three_node_rides = [('a','b',5),('a','c',0),('b','a',0),('b','c',5),('c','a',0),('c','b',0)]
second_three_node_rides = [('a','b',0),('a','c',0),('b','a',1),('b','c',3),('c','a',1),('c','b',0)]
third_three_node_rides = [('a','b',5),('a','c',0),('b','a',0),('b','c',5),('c','a',0),('c','b',0)]
fourth_three_node_rides = [('a','b',0),('a','c',0),('b','a',3),('b','c',2),('c','a',0),('c','b',0)]
three_node_supplies = [5,5,5]
three_node_time_slots = 4
slots_per_day = 4
price = 5
metadata = (three_node_supplies, three_node_time_slots, slots_per_day,price)
pkl.dump(metadata, open('3nodes_test_metadata', 'wb'))
pkl.dump(first_three_node_rides, open('3nodes_test0', 'wb'))
pkl.dump(second_three_node_rides, open('3nodes_test1', 'wb'))
pkl.dump(third_three_node_rides, open('3nodes_test2', 'wb'))
pkl.dump(fourth_three_node_rides, open('3nodes_test3', 'wb'))

first_rides = [('a','b',2),('b','a',1)]
second_rides = [('a','b',0),('b','a',1)]
third_rides = [('a','b',4),('b','a',0)]
fourth_rides = [('a','b',0),('b','a',1)]

supplies = [2,2]
time_slots = 4
slots_per_day = 4
price = 5
metadata = (supplies, time_slots, slots_per_day,price)

pkl.dump(metadata, open('metadata', 'wb'))
pkl.dump(first_rides, open('test_data0', 'wb'))
pkl.dump(second_rides, open('test_data1', 'wb'))
pkl.dump(third_rides, open('test_data2', 'wb'))
pkl.dump(fourth_rides, open('test_data3', 'wb'))

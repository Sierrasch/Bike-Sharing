# Bike-Sharing

Variables:

* days = d
* halfDays = 2d
* segments = k/2 
* nodes = n
* totalBikes = b 
* maxMovement = m


Graph Size:

* Start: adds n nodes 
* FreeCycle: adds 2n nodes, n^2 edges
* CostCycle: adds n nodes, n^2 edges
* End: adds 1 node, n edges

* Number of FreeCycles = halfDays * segments
* Number of CostCycles = halfDays

Total node size of graph = n + (k*2*d*n) + (2*d*n) + 1 = n + (k+1)(2*n*d) + 1 ~= (k+1)(2*n*d)

Scales linearly with all input parameters

Total edge size of graph = 0 + (k*2*d*n^2) + (2*d*n^2) + n = n + (k+1)(2*d*n^2) ~= (k+1)(2*d*n^2)

Edmund-Karp runs in VE^2, so time complexity should be = O( (k+1)^3 * (2*n*d) * (2*d*n^2)^2 )

=O(k^3 * d^3 * n^5)
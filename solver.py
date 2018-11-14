from numpy import *

setupData = loadtxt("input1.txt")
days = setupData[0]
segments = setupData[1]
nodes = setupData[2]
startingBikes = delete(setupData, [0,1,2,3])

bikeData = reshape(loadtxt("input2.txt"), (4, 3, 3))
outBikes = sum(bikeData, axis=2)
inBikes = sum(bikeData, axis=1)



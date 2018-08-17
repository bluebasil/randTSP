A variety of methods from simple to more complex, to tackle the Traveling Salesman Problem as a study.


Let
<img src="https://latex.codecogs.com/svg.latex?\Large&space;A=\{a_1,a_2,\dots,a_n\}" title="l1" /> be the set of all cities

Let
<img src="https://latex.codecogs.com/svg.latex?\Large&space;P=\{p_1,p_2,\dots,p_n\}" title="l2" /> be the set of cities in the path

Let 
<img src="https://latex.codecogs.com/svg.latex?\Large&space;distance(i,j)=√((i.x-j.x)^2+(i.y-j.y)^2)" title="l3" />

<img src="https://latex.codecogs.com/svg.latex?\Large&space;h(n)=max⁡(∀c∈\frac{A}{P}|distance(p_1,c)+distance(c,p_k))" title="l4" />


![viewEfficiency](/efficiencyGraph.png)

test

Number of Cities	|Custom Heuristic Number of Timeouts   |h(n) = 0 Number of Timeouts 
:----------------|:-------------------------------------|:---------------------------
|14	              |0	                                   |3                           |
|15	              |0	                                   |6                           |
|16               |2	                                   |10 (note that no ‘number of states’ could be determined because none of the test executed to completion)

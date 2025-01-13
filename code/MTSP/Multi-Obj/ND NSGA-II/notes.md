This is currently not working perfectly, the hypervolume occasionally drops between generations but
I'm pushing that down the road to focus on visualisation for now. I'm going to make a copy of this
directory in ``../visualisation``.

Eventually this will all need to be incorporated into a single class or something that takes the 
relevant functions (crossover, fitness, mutation, initiaisation) and sorts that all out but that's
a can I'm kicking down the road for now.

--------------------
RIGHT, hypervolume is fied with just a stupid error. Currently I'm converting the visualisation
interface to be "plotly" rather than matplotlib. This allows for much smoother visualisation that
can be interacted with $1000\times$ faster than matplotlib without slowing down.

It uses panda dataframes and allows each point to be highlightable showing characteristics. As such
I'm adding a clause to append the permutations for each solution in all generations because that
could be interesting.
Two solutions for Google Hashcode 2020 Problem

1. Heuristic Approach
2. Simulated Annealing

### Heuristic Approach
We tried scoring each library with a function of

`f(library) = (total_score / num_books) * (1 / time_to_scan )`

This gave us our best score in the tournament.


### Simulated Annealing 
For people who don't know what's SA is check this out [simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing)

Select an initial random library setup, randomly shuffle their positions, decrease the temperature and keep doing that until we find the approximate global maxima

### Credits
Rohith Uppala

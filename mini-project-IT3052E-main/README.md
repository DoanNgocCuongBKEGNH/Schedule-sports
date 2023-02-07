# Postman Problem
### Problem description.

Given a fixed depot at point 0, a number of N places needed to deliver at points 1,...,N, and a number of K postmans. Suppose there is a matrix $A_{(N+1) \times (N+1)}$, where $d[i,j]$ is a distance from point i to point j for all $i,j = 0,1,...,N$. 

The aim of this problem is determining a set of tours for K postmans in a way that each tour starts and ends at the depot and every places is visited by exactly one of these K postmans. 

Two objective functions are considered including:

- minimize the length of the longest tour
- minimize the total cost of all vehicles routes

### Math Modelling.

#### Variables.
* $x_{i,j}^{k} \in \{0,1\}$
$x_{i,j}^{k} = 1$ if postman k transvered from i to j 
$x_{i,j}^{k} = 0$ otherwise

* z: the artificial variable used to minimize the maximum tour cost



#### Constraints.

(1) Every place is visited by exactly one postman 

$\sum_{k \in K} \sum_{j \in A^{+}(i)} x_{i,j}^{k} = \sum_{k \in K} \sum_{j \in A^{-}(i)} x_{i,j}^{k} = 1$ $\forall i \in \{1,...,N\}$

(2) Balanced flow constraint: 

$\sum_{j \in A^{+}(i)} x_{i,j}^{k} = \sum_{j \in A^{-}(i)} x_{i,j}^{k}$ $\forall k \in \{1,...,K\}$ and $\forall i \in \{1,...,N\}$

(3) There are exactly K postmans departing from the depot and arriving to the depot

$\sum_{j \in N} x_{0,j}^{k} = \sum_{i \in N} x_{i,0}^{k} = 1$ $\forall k \in \{1,...,K\}$ 

(4) Imply that the maximum cost vehicle route is minimized

$\sum_{i,j \in N} d[i,j] x_{i,j}^{k} \le z$ $\forall k \in \{1,...,K\}$

(5) Subtour elimination constraint: 

$\sum_{i,j \in S} x_{i,j}^{k} \le |S| - 1$ $\forall S \subset N: 2 \le |S| \le |N|-1$, $\forall k \in {1,...,K}$

#### Objective function.

MIN $obj_1 = z$

MIN $obj_2 = \sum_{i \in N} \sum_{j \in N} d[i,j]x_{i,j}^{k}$

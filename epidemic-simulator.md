---
layout: post
title: SEIRD Epidemic Simulator
date: 24/02/2022
tags: networks - graphtheory - epidemics
githublink: https://github.com/jouleffect/SEIRD-Epidemics-Simulator
githubzip_url: https://github.com/jouleffect/SEIRD-Epidemics-Simulator/archive/refs/heads/main.zip
---

<h2> A network-based epidemic simulator</h2>

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

  
This project was realized for the "Complex Networks" course, hold at the Department of Information Technology of University of Palermo.<br>

The goal is to analyze the time evoulition of epidemics spread, based on the SEIRD model.<br>
The population is rapresented by a random network (Poisson Erdos-Renyi), generated by choosing a fixed number of nodes and a fixed 
edge probabiltity between them. 

<p><h3>This is the schema of the epidemic states used in the model:</h3></p>

<p>
  <img src="https://user-images.githubusercontent.com/53179989/153436667-6edace91-6e51-42e7-a313-127633eba619.png" style="width:500px;">
</p>

A Susceptible node can be catch the disease if it has an edge with an Exposed or Infected one. <br>
If it happens, the node becomes Exposed for a specific time, after which it becomes automatically Infected. <br>
During the Infection period, the node could become Recovered, but also it could fall in the Severe Infected state. <br>
If the node falls in the Severe Infected state, there is a probability that it could die.<br>
Note that, the node in the Dead state is not removed from the network, but it is just not taken in account for the next steps.<br>
<br>
The scripts of the program are the following:

- main.py
- model.py
- simulator.py

In the main script, in addition to the GUI objects, there is a function with this lines:

```python
def start_sim():
  sim = simulator.Simulator()
  net = model.Network(sim)
  for i in range(sim.num_iter):
    net.update_states(i,sim)
    net.t_state = net.t_state + sim.dt_state
    new_cases = net.get_new_cases(i,sim)
    sim.s_to_e(net,new_cases)
    sim.e_to_i(net)
    sim.i_to_r(net)
    sim.i_to_ig(net,i)
    sim.ig_to_d(net,i)

  if i>=plot_freq and i%plot_freq==0:
  p = net.plot(i,sim)
```

Inside the loop, these funcions are performed:

1. update_states(): updates the table states for each iteration
2. get_new_cases(): returns new cases of exposed to disease, according to the adjacency list
3. s_to_e(): takes the new cases and updates the state of the exposed nodes.
4. e_to_i(): updates the state from exposed to infected
5. i_to_r(): updates the state from infected to recovered
6. i_to_ig(): set which infected nodes go to the severe infected state
7. ig_to_d(): set which severe infected nodes go to the dead state
8. plot(): plot funcion of the epidemic states


* * *

<h3>HOW TO INSTALL:</h3> 

- Download the zip file from GitHub.
- install requirements:

<pre><code>pip install -r requirements.txt</code></pre>

<h3> HOW TO RUN:</h3>

Run the script:

<pre><code>python3 main.py</code></pre>

The GUI will open and you can start to use the simulator.

<h3> Interface example:</h3>

<p>
  <img src="https://user-images.githubusercontent.com/53179989/154806110-5482b180-3284-469b-8539-53986b42a3d0.png" style="width:500px;">
</p>

### Parameters

- Number of nodes: number of individuals of the population
- Link probability: mean connection rate between individuals
- Number of iterations: number of days to analyze
- Initial exposed: initial number of individuals affected from the disease
- Incubation period: incubation time of the disease
- Disease period: time of the disease
- Transmission rate (α)
- Severe infected rate (β).
- Mortality rate (γ).

* * *

<h2>REFERENCES:</h2>

Erdos-Renyi network model, LT03 - Spread of epidemics models, LT11 - Spread of epidemics networked models, LT12. Prof. Salvatore Miccichè - Complex Networks 2021/2022. Master in Informatics, University of Palermo.

A. Kuzdeuov, A. Karabay, D. Baimukashev, B. Ibragimov and  H. A. Varol, "A Particle-Based COVID-19 Simulator With Contact Tracing  and Testing," in IEEE Open Journal of Engineering in Medicine and  Biology, vol. 2, pp. 111-117, 2021, doi: 10.1109/OJEMB.2021.3064506.

A. Karabay, A. Kuzdeuov, S. Ospanova, M. Lewis and H. A. Varol, "A Vaccination Simulator for COVID-19: Effective and Sterilizing Immunization Cases," in IEEE Journal of Biomedical and Health Informatics, vol. 25, no. 12, pp. 4317-4327, Dec. 2021, doi: 10.1109/JBHI.2021.3114180.

A. Kuzdeuov *et al*., "A Network-Based Stochastic Epidemic Simulator: Controlling COVID-19 With Region-Specific Policies," in *IEEE Journal of Biomedical and Health Informatics*, vol. 24, no. 10, pp. 2743-2754, Oct. 2020, doi: 10.1109/JBHI.2020.3005160.

* * *

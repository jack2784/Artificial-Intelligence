# Fuzzy Car Control
# This is an implementation of a speed control and car seperation using fuzzy logic
# It is based on a solution to the "tipping problem" using fuzzy logic, avaliable at:
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

## New Antecedent/Consequent objects hold universe variables and membership
# functions
speed_deviation = ctrl.Antecedent(np.arange(-20, 21, 1), 'Speed Deviation')
distance_from_car = ctrl.Antecedent(np.arange(0, 50, 1), 'Distance from car')
throttle= ctrl.Consequent(np.arange(-100, 100, 1), 'Throttle')

# Auto-membership function population is possible with .automf(3, 5, or 7)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
throttle['break'] = fuzz.trimf(throttle.universe, [-10000000, -50, 0])
throttle['maintain'] = fuzz.trimf(throttle.universe, [-10, 0, 10])
throttle['speed up'] = fuzz.trimf(throttle.universe, [0, 50, 10000000])

speed_deviation['slow'] = fuzz.trimf(speed_deviation.universe, [-10000000, -10, 0])
speed_deviation['right'] = fuzz.trimf(speed_deviation.universe, [-2, 0, 2])
speed_deviation['fast'] = fuzz.trimf(speed_deviation.universe, [0, 10, 10000000])

distance_from_car['close'] = fuzz.trimf(distance_from_car.universe, [-10000000, 0, 29])
distance_from_car['right'] = fuzz.trimf(distance_from_car.universe, [28, 30, 33])
distance_from_car['far'] = fuzz.trimf(distance_from_car.universe, [32, 35, 10000000])

# You can see how these look with .view()
speed_deviation.view()

distance_from_car.view()

throttle.view()

rule1 = ctrl.Rule(speed_deviation['fast'] & distance_from_car['close'], throttle['break'])
rule2 = ctrl.Rule(speed_deviation['slow'] & distance_from_car['far'], throttle['high'])
rule3 = ctrl.Rule(speed_deviation['slow'] & distance_from_car['close'], throttle['break'])
rule4 = ctrl.Rule(speed_deviation['fast'] & distance_from_car['far'], throttle['break'])
rule5 = ctrl.Rule(speed_deviation['right'] & distance_from_car['right'], throttle['maintain'])
rule6 = ctrl.Rule(speed_deviation['right'] & distance_from_car['close'], throttle['break'])
rule7 = ctrl.Rule(speed_deviation['slow'] & distance_from_car['right'], throttle['maintain'])
rule8 = ctrl.Rule(speed_deviation['right'] & distance_from_car['far'], throttle['maintain'])
rule9 = ctrl.Rule(speed_deviation['fast'] & distance_from_car['right'], throttle['break'])

rule1.view()

throttle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

throttling = ctrl.ControlSystemSimulation(throttle_ctrl)


# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
throttling.input['Speed Deviation'] = 500
throttling.input['Distance from car'] = 100
# Crunch the numbers
throttling.compute()


print(throttling.output['Throttle'])

throttle.view(sim=throttling)

throttle.view(throttling)
# Fuzzy Car Control

# This is an implementation of a speed control and car seperation using fuzzy logic

# It is based on a solution to the "tipping problem" using fuzzy logic, avaliable at:

# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem.html



import numpy as np

import skfuzzy as fuzz

from skfuzzy import control as ctrl

import matplotlib.pyplot as plt



## New Antecedent/Consequent objects hold universe variables and membership

# functions

#Possible values -20..21
speed_deviation = -20
#Possible values 0..100
distance_to_car = 0


x_speed = np.arange(-20, 21, 1)
x_distance = np.arange(0, 100, 1)
x_throttle = np.arange(-100, 100, 1)

speed_slow = fuzz.trapmf(x_speed,[-100,-75,-10,0])
speed_right = fuzz.trapmf(x_speed, [-2, -1,1, 2])
speed_fast = fuzz.trapmf(x_speed, [0, 10, 100,100])

distance_close = fuzz.trimf(x_distance, [0, 0, 29])
distance_right = fuzz.trimf(x_distance, [28, 30, 33])
distance_far = fuzz.trapmf(x_distance, [32, 50,1000 ,1000])

throttle_break = fuzz.trapmf(x_throttle, [-100,-100, -75, 0])
throttle_maintain = fuzz.trimf(x_throttle, [-10, 0, 10])
throttle_acc= fuzz.trapmf(x_throttle, [0, 75, 100,100])

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_speed, speed_slow, 'b', linewidth=1.5, label='Slow')
ax0.plot(x_speed, speed_right, 'g', linewidth=1.5, label='Decent')
ax0.plot(x_speed, speed_fast, 'r', linewidth=1.5, label='Fast')
ax0.set_title('Speed deviation')
ax0.legend()

ax1.plot(x_distance, distance_close, 'b', linewidth=1.5, label='Close')
ax1.plot(x_distance, distance_right, 'g', linewidth=1.5, label='OK')
ax1.plot(x_distance, distance_far, 'r', linewidth=1.5, label='Far')
ax1.set_title('Separation')
ax1.legend()

ax2.plot(x_throttle, throttle_break, 'b', linewidth=1.5, label='Break')
ax2.plot(x_throttle, throttle_maintain, 'g', linewidth=1.5, label='Maintain')
ax2.plot(x_throttle, throttle_acc, 'r', linewidth=1.5, label='Speed up')
ax2.set_title('Throttle amount')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

speed_level_slow = fuzz.interp_membership(x_speed,speed_slow,speed_deviation)
speed_level_right = fuzz.interp_membership(x_speed,speed_right,speed_deviation)
speed_level_fast = fuzz.interp_membership(x_speed,speed_fast,speed_deviation)

distance_level_close = fuzz.interp_membership(x_distance,distance_close,distance_to_car)
distance_level_right = fuzz.interp_membership(x_distance,distance_right,distance_to_car)
distance_level_far = fuzz.interp_membership(x_distance,distance_far,distance_to_car)

print("Speed membership: " + str(speed_level_slow) + " " + str(speed_level_right)+ " " + str(speed_level_fast))
print("Distance membership: " + str(distance_level_close) + " " + str(distance_level_right)+ " " + str(distance_level_far))


rule1 = np.fmin(speed_level_fast,distance_level_close)
throttle1 = np.fmin(rule1,throttle_break)

rule2 = np.fmin(speed_level_slow,distance_level_far)
throttle2 = np.fmin(rule2,throttle_acc)


rule3 = np.fmin(speed_level_slow,distance_level_close)
throttle3 = np.fmin(rule3,throttle_break)

rule4 = np.fmin(speed_level_fast,distance_level_far)
throttle4 = np.fmin(rule4,throttle_break)

rule5 = np.fmin(speed_level_right,distance_level_right)
throttle5 = np.fmin(rule5,throttle_maintain)

rule6 = np.fmin(speed_level_right,distance_level_close)
throttle6 = np.fmin(rule6,throttle_break)

rule7 = np.fmin(speed_level_slow,distance_level_right)
throttle7 = np.fmin(rule7,throttle_maintain)

rule8 = np.fmin(speed_level_right,distance_level_far)
throttle8 = np.fmin(rule8,throttle_maintain)

rule9 = np.fmin(speed_level_fast,distance_level_right)
throttle9 = np.fmin(rule9,throttle_break)


thottle0 = np.zeros_like(x_throttle)
# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.fill_between(x_throttle, thottle0, throttle1, facecolor='b', alpha=0.7)
ax0.fill_between(x_throttle, thottle0, throttle3, facecolor='b', alpha=0.7)
ax0.fill_between(x_throttle, thottle0, throttle4, facecolor='b', alpha=0.7)
ax0.fill_between(x_throttle, thottle0, throttle6, facecolor='b', alpha=0.7)
ax0.fill_between(x_throttle, thottle0, throttle9, facecolor='b', alpha=0.7)
ax0.plot(x_throttle, throttle_break, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_throttle, thottle0, throttle5, facecolor='g', alpha=0.7)
ax0.plot(x_throttle, throttle_maintain, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(x_throttle, thottle0, throttle2, facecolor='r', alpha=0.7)
ax0.plot(x_throttle, throttle_acc, 'r', linewidth=0.5, linestyle='--')
ax0.set_title('Output membership activity')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

aggregated = np.fmax(throttle1,np.fmax(throttle2,np.fmax(throttle3,np.fmax(throttle4,np.fmax(throttle5,
            np.fmax(throttle6,np.fmax(throttle7,np.fmax(throttle8,throttle9))))))))




som = fuzz.defuzz(x_throttle, aggregated, 'som') 
lom = fuzz.defuzz(x_throttle, aggregated, 'lom')
throttlesetting = lom
if abs(som)<abs(lom):
    throttlesetting = som

print(throttlesetting)

throttley = fuzz.interp_membership(x_throttle, aggregated, throttlesetting)  # for plot

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.plot(x_throttle, throttle_break, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(x_throttle, throttle_maintain, 'g', linewidth=0.5, linestyle='--')
ax0.plot(x_throttle, throttle_acc, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_throttle, thottle0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([throttlesetting, throttlesetting], [0, throttley], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Aggregated membership and result (line)')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

previous_dose = np.random.uniform(1, 9.99)

def update_display(frame):
    global previous_dose
    ax.clear()
    
    random_dose = previous_dose + np.random.uniform(-1, 1)
    random_dose = max(1, min(10, random_dose))
    previous_dose = random_dose
    
    ax.text(0.5, 0.5, f"{random_dose:.2f}", fontsize=100, ha='center', va='center', color='#00FF00', family='monospace')
    ax.text(0.5, 0.1, 'EQUIVALENT DOSE RATE', fontsize=15, ha='center', va='center', color='white', family='monospace')
    ax.text(0.9, 0.6, 'μSv/h', fontsize=15, ha='center', va='center', color='white', family='monospace')
    ax.set_facecolor('black')
    ax.axis('off')

fig, ax = plt.subplots()
fig.patch.set_facecolor('black')

ani = animation.FuncAnimation(fig, update_display, interval=9000)

plt.show()

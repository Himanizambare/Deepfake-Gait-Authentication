import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set a slightly different style
sns.set(style="ticks", palette="pastel")

# -------------------------------------------------------------------
# 1. GENERATE DUMMY DATA
# -------------------------------------------------------------------

# --- Data for Bar Chart (Limb Symmetry) ---
# Comparing Pre-Op and Post-Op for left vs. right limbs
sym_data = {
    'Condition': ['Pre-Op', 'Pre-Op', 'Post-Op', 'Post-Op',
                  'Pre-Op', 'Pre-Op', 'Post-Op', 'Post-Op'],
    'Limb': ['Left', 'Right', 'Left', 'Right',
             'Left', 'Right', 'Left', 'Right'],
    'Parameter': ['Step Length (m)', 'Step Length (m)', 'Step Length (m)', 'Step Length (m)',
                  'Swing Time (s)', 'Swing Time (s)', 'Swing Time (s)', 'Swing Time (s)'],
    'Value': [0.55, 0.65, 0.62, 0.64,  # Step Length (becomes more symmetrical)
              0.45, 0.38, 0.41, 0.40]   # Swing Time (becomes more symmetrical)
}
sym_df = pd.DataFrame(sym_data)


# --- Data for Line Plots (Kinematics & Kinetics) ---
gait_cycle = np.linspace(0, 100, 101)

# Dummy Kinematics (Ankle Angle)
# Simulating plantarflexion/dorsiflexion
ankle_angle_pre = 10 * np.sin(np.deg2rad(gait_cycle * 3.6)) - 5 * np.sin(np.deg2rad(gait_cycle * 7.2)) - 5
ankle_angle_post = 12 * np.sin(np.deg2rad(gait_cycle * 3.6 + 10)) - 4 * np.sin(np.deg2rad(gait_cycle * 7.2)) - 2

# Dummy Kinetics (Ankle Moment)
# Simulating plantarflexor moment during push-off
x = gait_cycle
moment_pre = 1.2 * np.exp(-0.005 * (x - 80)*2) - 0.3 * np.exp(-0.01 * (x - 20)*2)
moment_post = 1.6 * np.exp(-0.005 * (x - 82)*2) - 0.2 * np.exp(-0.01 * (x - 18)*2) # Stronger push-off


# --- Data for Box Plot (Variability) ---
# Simulating 100 step widths for each condition
np.random.seed(42) # for reproducible results
step_width_pre = np.random.normal(loc=0.25, scale=0.08, size=100) # Wider, more variable
step_width_post = np.random.normal(loc=0.20, scale=0.04, size=100) # Narrower, less variable

# Combine into a DataFrame for seaborn
box_data_pre = pd.DataFrame({'Condition': 'Pre-Op', 'Step Width (m)': step_width_pre})
box_data_post = pd.DataFrame({'Condition': 'Post-Op', 'Step Width (m)': step_width_post})
box_df = pd.concat([box_data_pre, box_data_post])


# -------------------------------------------------------------------
# 2. CREATE PLOTS
# -------------------------------------------------------------------

# Create a 2x2 figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Gait Analysis Report: Pre-Op vs. Post-Op (Dummy Data)', fontsize=20)

# --- Plot 1: Bar Chart (Symmetry) ---
# Using catplot's 'hue' feature to group by limb
g = sns.catplot(
    data=sym_df,
    x='Parameter',
    y='Value',
    hue='Limb',
    col='Condition', # Create separate columns for Pre/Post
    kind='bar',
    palette='Blues',
    height=5, # Need to adjust plot creation slightly
    aspect=0.8,
)
# catplot creates its own Figure, so we can't place it in 'axes'
# We'll just show it separately after the main 2x2 grid.
# For simplicity in this example, I'll replace it with a standard barplot.

# --- Plot 1 (Alternative): Grouped Bar Chart in axes[0, 0] ---
sns.barplot(
    data=sym_df,
    x='Parameter',
    y='Value',
    hue='Limb',
    ci=None, # Turn off error bars for this dummy data
    ax=axes[0, 0]
)
axes[0, 0].set_title('Spatio-temporal Parameters (Left vs. Right)')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('Value')


# --- Plot 2: Line Plot (Kinematics) ---
axes[0, 1].plot(gait_cycle, ankle_angle_pre, label='Pre-Op', color='purple', linewidth=2)
axes[0, 1].plot(gait_cycle, ankle_angle_post, label='Post-Op', color='green', linestyle='--', linewidth=2)
axes[0, 1].set_title('Ankle Angle Kinematics')
axes[0, 1].set_xlabel('Gait Cycle (%)')
axes[0, 1].set_ylabel('Angle (deg)')
axes[0, 1].axhline(y=0, color='gray', linestyle=':', label='Neutral (0°)')
axes[0, 1].legend()
axes[0, 1].text(5, 12, 'Dorsiflexion', color='gray')
axes[0, 1].text(5, -18, 'Plantarflexion', color='gray')


# --- Plot 3: Line Plot (Kinetics) ---
axes[1, 0].plot(gait_cycle, moment_pre, label='Pre-Op', color='purple', linewidth=2)
axes[1, 0].plot(gait_cycle, moment_post, label='Post-Op', color='green', linestyle='--', linewidth=2)
axes[1, 0].set_title('Ankle Moment (Kinetics)')
axes[1, 0].set_xlabel('Gait Cycle (%)')
axes[1, 0].set_ylabel('Moment (Nm/kg)')
axes[1, 0].axhline(y=0, color='gray', linestyle=':')
axes[1, 0].legend()
axes[1, 0].text(70, 1.0, 'Plantarflexor Moment', color='gray')
axes[1, 0].text(10, -0.2, 'Dorsiflexor Moment', color='gray')


# --- Plot 4: Box Plot (Variability) ---
sns.boxplot(
    data=box_df,
    x='Condition',
    y='Step Width (m)',
    palette=['purple', 'green'],
    ax=axes[1, 1]
)
# Add swarmplot to show individual data points
sns.swarmplot(
    data=box_df,
    x='Condition',
    y='Step Width (m)',
    color=".25",
    size=3,
    ax=axes[1, 1]
)
axes[1, 1].set_title('Step Width Distribution & Variability')
axes[1, 1].set_xlabel('Condition')
axes[1, 1].set_ylabel('Step Width (m)')


# --- Final Show ---
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
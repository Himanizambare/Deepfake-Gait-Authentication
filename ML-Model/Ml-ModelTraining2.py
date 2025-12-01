import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set a style for prettier plots
sns.set(style="whitegrid")

# -------------------------------------------------------------------
# 1. GENERATE DUMMY DATA
# -------------------------------------------------------------------

# --- Data for Bar Chart (Spatio-temporal Parameters) ---
# We'll compare a 'Control' group vs. a 'Patient' group
st_data = {
    'Group': ['Control', 'Control', 'Patient', 'Patient',
              'Control', 'Control', 'Patient', 'Patient',
              'Control', 'Control', 'Patient', 'Patient'],
    'Leg': ['Left', 'Right', 'Left', 'Right',
            'Left', 'Right', 'Left', 'Right',
            'Left', 'Right', 'Left', 'Right'],
    'Parameter': ['Step Length (m)', 'Step Length (m)', 'Step Length (m)', 'Step Length (m)',
                  'Stance Time (%)', 'Stance Time (%)', 'Stance Time (%)', 'Stance Time (%)',
                  'Cadence (steps/min)', 'Cadence (steps/min)', 'Cadence (steps/min)', 'Cadence (steps/min)'],
    'Value': [0.75, 0.74, 0.62, 0.55,  # Step Lengths
              62.0, 61.8, 68.0, 71.0,  # Stance Times
              118, 118, 105, 105]      # Cadence
}
st_df = pd.DataFrame(st_data)

# --- Data for Line Plots (Kinematics & Kinetics) ---
# Data over a single gait cycle (0% to 100%)
gait_cycle = np.linspace(0, 100, 101)  # 101 data points

# Dummy Kinematics (Joint Angles)
# Simulating a basic knee flexion/extension wave
knee_angle_control = 5 + 35 * (1 - np.cos(np.deg2rad(gait_cycle * 3.6)))
knee_angle_patient = 10 + 25 * (1 - np.cos(np.deg2rad(gait_cycle * 3.6 - 10))) # Less flexion

# Dummy Kinetics (Ground Reaction Force - Vertical)
# Simulating the classic 'M' (double-peak) shape
x = gait_cycle
peak1_control = 1.2 * np.exp(-0.01 * (x - 20)**2)
peak2_control = 1.1 * np.exp(-0.01 * (x - 75)**2)
grf_v_control = peak1_control + peak2_control + 0.1 * np.sin(np.deg2rad(x*3.6))

peak1_patient = 0.8 * np.exp(-0.01 * (x - 25)**2)  # Lower first peak
peak2_patient = 0.9 * np.exp(-0.01 * (x - 70)**2)  # Lower second peak
grf_v_patient = peak1_patient + peak2_patient

# --- Data for Histogram (Variability) ---
# Simulating 100 step times for each group
steps_control = np.random.normal(loc=1.02, scale=0.02, size=100)
steps_patient = np.random.normal(loc=1.15, scale=0.08, size=100) # Slower and more variable


# -------------------------------------------------------------------
# 2. CREATE PLOTS
# -------------------------------------------------------------------

# Create a 2x2 figure to hold all our plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Gait Analysis Report (Dummy Data)', fontsize=20)

# --- Plot 1: Bar Chart (Spatio-temporal) ---
# We'll show just Step Length and Stance Time for clarity
param_df = st_df[st_df['Parameter'].isin(['Step Length (m)', 'Stance Time (%)'])]
sns.barplot(
    data=param_df,
    x='Parameter',
    y='Value',
    hue='Group',
    palette='muted',
    ax=axes[0, 0]
)
axes[0, 0].set_title('Spatio-temporal Parameters')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('Value')


# --- Plot 2: Line Plot (Kinematics) ---
axes[0, 1].plot(gait_cycle, knee_angle_control, label='Control', color='blue', linewidth=2)
axes[0, 1].plot(gait_cycle, knee_angle_patient, label='Patient', color='red', linestyle='--', linewidth=2)
axes[0, 1].set_title('Knee Angle Kinematics')
axes[0, 1].set_xlabel('Gait Cycle (%)')
axes[0, 1].set_ylabel('Knee Flexion Angle (deg)')
axes[0, 1].axvline(x=60, color='gray', linestyle=':', label='Avg. Toe-Off') # Typical toe-off
axes[0, 1].legend()


# --- Plot 3: Line Plot (Kinetics) ---
axes[1, 0].plot(gait_cycle, grf_v_control, label='Control', color='blue', linewidth=2)
axes[1, 0].plot(gait_cycle, grf_v_patient, label='Patient', color='red', linestyle='--', linewidth=2)
axes[1, 0].set_title('Vertical Ground Reaction Force (GRF)')
axes[1, 0].set_xlabel('Gait Cycle (%)')
axes[1, 0].set_ylabel('Force (Body Weight)')
axes[1, 0].axhline(y=1, color='gray', linestyle=':', label='Body Weight')
axes[1, 0].legend()


# --- Plot 4: Histogram (Variability) ---
sns.histplot(steps_control, label='Control', color='blue', kde=True, ax=axes[1, 1])
sns.histplot(steps_patient, label='Patient', color='red', kde=True, ax=axes[1, 1])
axes[1, 1].set_title('Step Time Variability')
axes[1, 1].set_xlabel('Step Time (s)')
axes[1, 1].set_ylabel('Frequency (Count)')
axes[1, 1].legend()


# --- Final Show ---
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
plt.show()
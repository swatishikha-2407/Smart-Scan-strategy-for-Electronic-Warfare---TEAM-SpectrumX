"""
Configuration settings for the simulated RF environment.

This file contains default values only.
Other team members should import these settings rather than
hard-coding simulation values throughout the project.
"""

# ============================================================
# GENERAL SIMULATION SETTINGS
# ============================================================

# Number of simulated frequency bands.
# Example:
# 20 bands means band IDs will be 0 to 19.
NUM_BANDS = 20

# Number of simulation time steps.
SIMULATION_TIME_STEPS = 500

# Default random seed.
# Using the same seed makes experiments reproducible.
DEFAULT_SEED = 42


# ============================================================
# EMITTER SETTINGS
# ============================================================

# Default probability that a random/intermittent emitter
# is active during a time step.
DEFAULT_ACTIVITY_PROBABILITY = 0.5

# Probability that an emitter changes its band when using
# frequency-changing behavior.
DEFAULT_FREQUENCY_CHANGE_PROBABILITY = 0.2

# Default probability of an intermittent emitter becoming active.
DEFAULT_INTERMITTENT_PROBABILITY = 0.4


# ============================================================
# EMITTER BEHAVIOR TYPES
# ============================================================

PERIODIC = "periodic"
RANDOM = "random"
FREQUENCY_CHANGING = "frequency_changing"
INTERMITTENT = "intermittent"


# ============================================================
# DEFAULT PERIODIC SETTINGS
# ============================================================

# Default number of time steps between periodic transmissions.
DEFAULT_PERIOD = 5

# Default duration of a periodic transmission.
DEFAULT_DURATION = 1


# ============================================================
# VALID BEHAVIOR TYPES
# ============================================================

VALID_EMITTER_TYPES = {
    PERIODIC,
    RANDOM,
    FREQUENCY_CHANGING,
    INTERMITTENT,
}

import modes

mode = modes.allModes()[2]
new = {
    "upper_rate_limit": 150,
    "lower_rate_limit": 60,
    "ventricular_amplitude": 3.5,
    "ventricular_pulse_width": 0.05,
    "hysteresis": True
}
print(modes.saveParamValues(mode, new))
print(mode.params)

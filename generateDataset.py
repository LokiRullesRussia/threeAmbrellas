import pandas as pd
import numpy as np
import random
import os

NUM_USERS = 500

W_T = 0.5
W_D = 0.5
W_A = 0.8
W_C = 0.7
W_TD = 0.1
W_TA = 0.1
W_DA = 0.1
W_TC = 0.3
W_DC = 0.3
W_AC = 0.4
LAMBDA = 0.5

def normalizeCommands(c):
    return 1 - np.exp(-LAMBDA * c)

def generateCommands():
    r = random.random()
    if r < 0.7:
        return 0
    elif r < 0.9:
        return random.randint(1, 3)
    else:
        return random.randint(4, 10)

def calculate_R(t, d, a, c):
    c_norm = normalizeCommands(c)
    return (W_T * t + W_D * d + W_A * a +
            W_C * c_norm +
            W_TD * t * d + W_TA * t * a +
            W_DA * d * a +
            W_TC * t * c_norm +
            W_DC * d * c_norm +
            W_AC * a * c_norm)

def classify(R):
    if R <= 2:
        return "GREEN"
    elif R <= 6:
        return "ORANGE"
    else:
        return "RED"

def generateTime():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def generateDevice():
    knownDevices = ["PC-1234", "PC-5678", "Laptop-001"]
    if random.random() < 0.6:
        return random.choice(knownDevices)
    else:
        return f"DEV-{random.randint(1000, 9999)}"

def generateAction():
    actions = ["read", "write", "delete", "rename", "copy"]
    return random.choice(actions)

def generateCommandsList():
    allCmds = ["cmd.exe", "powershell.exe", "whoami", "net user", "sc query", "schtasks", "ipconfig"]
    if random.random() < 0.7:
        return []
    else:
        num = random.randint(1, 2)
        return random.sample(allCmds, num)

def time_to_t(time_str):
    hour = int(time_str.split(':')[0])
    return 1 if (hour < 6 or hour >= 22) else 0

def device_to_d(device):
    knownDevices = ["PC-1234", "PC-5678", "Laptop-001"]
    return 0 if device in knownDevices else 1

def action_to_a(action):
    return 0 if action == "read" else 1

records = []
answers = []

for i in range(NUM_USERS):
    time_str = generateTime()
    device = generateDevice()
    action = generateAction()
    commands = generateCommandsList()

    t = time_to_t(time_str)
    d = device_to_d(device)
    a = action_to_a(action)
    c = len(commands)

    R = calculate_R(t, d, a, c)
    phase = classify(R)

    records.append({
        'user': f'user_{i+1}',
        'time': time_str,
        'device': device,
        'action': action,
        'commands': ';'.join(commands),
        't': t,
        'd': d,
        'a': a,
        'c': c
    })

    answers.append({
        'user': f'user_{i+1}',
        'R': round(R, 3),
        'phase': phase,
        'attack': 0 if phase == "GREEN" else 1
    })

if not os.path.exists('data'):
    os.makedirs('data')

df_records = pd.DataFrame(records)
df_answers = pd.DataFrame(answers)

df_records.to_csv('data/dataset.csv', index=False)
df_answers.to_csv('data/answers.csv', index=False)

print(f"Создано {NUM_USERS} записей")
print(" data/dataset.csv")
print(" data/answers.csv")
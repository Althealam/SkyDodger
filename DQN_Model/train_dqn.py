import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # 把上级目录加入搜索路径
from rl_env import SkyDodgerEnv
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from dqn_model import QNetwork
from replay_buffer import ReplayBuffer

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 超参数
BATCH_SIZE = 64
GAMMA = 0.99
LR = 1e-3
EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 0.995
TARGET_UPDATE = 50
EPISODES = 800

def train_dqn():
    env = SkyDodgerEnv(max_steps=1500, spawn_prob=0.06)
    state_dim = len(env.reset())
    action_dim = len(env.ACTIONS)

    policy_net = QNetwork(state_dim, action_dim).to(DEVICE)
    target_net = QNetwork(state_dim, action_dim).to(DEVICE)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    buffer = ReplayBuffer(100000)

    eps = EPS_START
    rewards = []

    for ep in range(EPISODES):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            # ε-greedy 策略
            if np.random.rand() < eps:
                action = np.random.randint(action_dim)
            else:
                with torch.no_grad():
                    q_vals = policy_net(torch.tensor(state, dtype=torch.float32).to(DEVICE))
                    action = int(torch.argmax(q_vals).item())

            next_state, reward, done, info = env.step(action)
            buffer.push(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            # 经验回放更新
            if len(buffer) >= BATCH_SIZE:
                s, a, r, s2, d = buffer.sample(BATCH_SIZE)
                s = torch.tensor(s, dtype=torch.float32).to(DEVICE)
                a = torch.tensor(a, dtype=torch.int64).unsqueeze(1).to(DEVICE)
                r = torch.tensor(r, dtype=torch.float32).unsqueeze(1).to(DEVICE)
                s2 = torch.tensor(s2, dtype=torch.float32).to(DEVICE)
                d = torch.tensor(d, dtype=torch.float32).unsqueeze(1).to(DEVICE)

                q_val = policy_net(s).gather(1, a)
                with torch.no_grad():
                    target_q = target_net(s2).max(1, keepdim=True)[0]
                    target = r + GAMMA * target_q * (1 - d)
                loss = nn.functional.mse_loss(q_val, target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # 更新 target 网络
        if ep % TARGET_UPDATE == 0:
            target_net.load_state_dict(policy_net.state_dict())

        eps = max(EPS_END, eps * EPS_DECAY)
        rewards.append(total_reward)
        if (ep + 1) % 20 == 0:
            print(f"[EP {ep+1:4d}] reward={total_reward:7.2f}  eps={eps:.3f}")

    torch.save(policy_net.state_dict(), "./models/dqn_model.pth")
    print("✅ DQN training finished. Model saved as dqn_model.pth")

if __name__ == "__main__":
    train_dqn()

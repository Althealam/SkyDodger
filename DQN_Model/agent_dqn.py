# agent_dqn.py
import torch
import numpy as np
from DQN_Model.dqn_model import QNetwork
from settings import W, H, PLAYER_SPEED

class DQNAgent:
    """
    基于训练好的 DQN 模型的智能体，用于控制飞机。
    输入：当前飞机位置、陨石坐标列表
    输出：动作编号（0:停 1:上 2:下 3:左 4:右）
    """
    def __init__(self, model_path="dqn_model.pth", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = QNetwork(state_dim=8, action_dim=5).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def get_state(self, px, py, meteors):
        """构建与训练时一致的观测向量"""
        obs = [px / W, py / H]
        mets = sorted(meteors, key=lambda m: (m[1]-py)**2 + (m[0]-px)**2)[:3]
        for i in range(3):
            if i < len(mets):
                x, y = mets[i]
                obs += [(x - px) / W, (y - py) / H]
            else:
                obs += [0.0, 0.0]
        return np.array(obs, dtype=np.float32)

    def act(self, px, py, meteors):
        """根据当前游戏状态输出动作"""
        state = self.get_state(px, py, meteors)
        with torch.no_grad():
            q_values = self.model(torch.tensor(state, dtype=torch.float32).to(self.device))
            action = int(torch.argmax(q_values).item())
        return action

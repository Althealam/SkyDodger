# dqn_model.py
import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """
    一个简单的前馈神经网络 (MLP)，用于 Q-learning 的函数近似。
    输入：状态向量 s
    输出：每个动作 a 的 Q(s, a)
    """
    def __init__(self, state_dim, action_dim, hidden_dim=128):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, action_dim)

        # 初始化（可提升稳定性）
        nn.init.kaiming_uniform_(self.fc1.weight, nonlinearity="relu")
        nn.init.kaiming_uniform_(self.fc2.weight, nonlinearity="relu")
        nn.init.xavier_uniform_(self.fc3.weight)

    def forward(self, x):
        if isinstance(x, list):
            x = torch.tensor(x, dtype=torch.float32)
        elif not torch.is_tensor(x):
            x = torch.tensor(x, dtype=torch.float32)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

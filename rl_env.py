# rl_env.py
import math, random
import numpy as np
from settings import W, H, SAFE_MARGIN, PLAYER_SPEED, OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED

class SkyDodgerEnv:
    """
    一个简化版的 Sky Dodger 环境（用于强化学习训练）。
    不使用图像，只模拟位置和碰撞逻辑。
    """

    ACTIONS = ["STAY", "UP", "DOWN", "LEFT", "RIGHT"]

    def __init__(self, max_steps=1500, spawn_prob=0.05, k_nearest=3):
        self.max_steps = max_steps
        self.spawn_prob = spawn_prob   # 陨石生成概率
        self.k = k_nearest             # 每次选最近的 k 个陨石
        self.r_player = 18             # 飞机碰撞半径
        self.r_meteor = (20, 30)       # 陨石碰撞半径范围
        self.reset()

    # -----------------------------------
    # 重置环境
    # -----------------------------------
    def reset(self, seed=None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.t = 0
        self.score = 0
        self.px = W // 2
        self.py = H - 120
        self.v = PLAYER_SPEED
        self.meteors = []   # 陨石 [x, y, vy, r]
        for _ in range(2):
            self._spawn()
        return self._observe()

    # -----------------------------------
    # 每步执行（Agent 调用）
    # -----------------------------------
    def step(self, a_idx: int):
        self.t += 1
        action = self.ACTIONS[a_idx]

        # === 执行动作 ===
        dx, dy = 0, 0
        if action == "UP":    dy = -self.v
        if action == "DOWN":  dy =  self.v
        if action == "LEFT":  dx = -self.v
        if action == "RIGHT": dx =  self.v
        self.px = int(np.clip(self.px + dx, SAFE_MARGIN, W - SAFE_MARGIN))
        self.py = int(np.clip(self.py + dy, SAFE_MARGIN, H - SAFE_MARGIN))

        # === 随机生成新陨石 ===
        if random.random() < self.spawn_prob:
            self._spawn()

        # === 陨石移动 ===
        reward = 0.1  # 存活奖励
        new_meteors = []
        for x, y, vy, r in self.meteors:
            y += vy
            if y - r > H:
                reward += 1.0   # 成功避过陨石
                self.score += 10
            else:
                new_meteors.append([x, y, vy, r])
        self.meteors = new_meteors

        # === 碰撞检测（圆形） ===
        done = False
        for x, y, vy, r in self.meteors:
            dist_sq = (self.px - x)**2 + (self.py - y)**2
            if dist_sq <= (self.r_player + r)**2:
                reward -= 10.0
                done = True
                break

        # === 终止条件 ===
        if self.t >= self.max_steps:
            done = True

        obs = self._observe()
        info = {"score": self.score, "t": self.t}
        return obs, reward, done, info

    # -----------------------------------
    # 状态构造函数
    # -----------------------------------
    def _observe(self):
        """
        返回观测向量:
        [px_norm, py_norm, dx1, dy1, dx2, dy2, dx3, dy3]
        """
        obs = [self.px / W, self.py / H]

        # 按距离选最近的 k 个陨石
        mets = sorted(
            self.meteors,
            key=lambda m: (m[0] - self.px)**2 + (m[1] - self.py)**2
        )[:self.k]

        for i in range(self.k):
            if i < len(mets):
                x, y, vy, r = mets[i]
                obs += [(x - self.px) / W, (y - self.py) / H]
            else:
                obs += [0.0, 0.0]
        return np.array(obs, dtype=np.float32)

    # -----------------------------------
    # 生成陨石
    # -----------------------------------
    def _spawn(self):
        r = random.randint(*self.r_meteor)
        x = random.randint(SAFE_MARGIN + r, W - SAFE_MARGIN - r)
        y = -r
        vy = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED)
        self.meteors.append([x, y, vy, r])

    # -----------------------------------
    # 离散化函数（Q-Table 用）
    # -----------------------------------
    def discretize(self, obs, bins=(10, 10, 5, 8)):
        """
        把连续状态离散化成单个索引 ID
        仅在 Q-Learning 表格法中使用
        """
        px, py = int(np.clip(obs[0]*bins[0], 0, bins[0]-1)), int(np.clip(obs[1]*bins[1], 0, bins[1]-1))

        def bucket_dxdy(dx, dy):
            bx = int(np.clip(np.round(dx*2), -2, 2)) + 2
            by = int(np.clip(np.floor((dy+1)/2 * 8), 0, 7))
            return bx, by

        bx1, by1 = bucket_dxdy(obs[2], obs[3])
        bx2, by2 = bucket_dxdy(obs[4], obs[5])
        bx3, by3 = bucket_dxdy(obs[6], obs[7])

        state_id = (((((px*bins[1] + py)*5 + bx1)*8 + by1)*5 + bx2)*8 + by2)
        state_id = (((state_id*5 + bx3)*8) + by3)
        return int(state_id)

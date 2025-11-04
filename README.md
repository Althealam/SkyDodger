# 🛩️ Sky Dodger  
_A minimal 2D airplane dodging game built with **Pygame**, designed for both playing and reinforcement learning (Q-Learning / DQN) training._  
一个使用 **Pygame** 开发的 2D 飞机躲避游戏，既可供玩家游玩，也能扩展为强化学习（Q-Learning / DQN）环境。  

---

## 📖 Table of Contents | 目录
- [🌟 Features | 功能特色](#-features--功能特色)  
- [🎮 Gameplay | 游戏玩法](#-gameplay--游戏玩法)  
- [⚙️ Installation | 安装](#️-installation--安装)  
- [🚀 Run the Game | 运行游戏](#-run-the-game--运行游戏)  
- [🧩 Train DQN Agent ｜ 训练DQN智能体]()
- [📂 Project Structure | 项目结构](#-project-structure--项目结构)   

---

## 🌟 Features | 功能特色

| English | 中文 |
|----------|------|
| 🎮 **Playable in real time** — Control the plane with arrow keys. | 🎮 **实时可玩** —— 使用方向键控制飞机移动。 |
| ☁️ **Dynamic obstacles** — Meteors with random speed and spawn positions. | ☁️ **动态障碍** —— 陨石坠落速度和位置随机生成。 |
| 🧱 **Modular design** — Code split into multiple files for clarity and scalability. | 🧱 **模块化结构** —— 多文件分离，结构清晰，便于扩展。 |
| 🧠 **RL-ready** — Can be wrapped as a Gym environment for Q-Learning or DQN. | 🧠 **强化学习友好** —— 可封装为 Gym 环境，进行 Q-Learning / DQN 训练。 |
| 🎨 **Simple UI** — Clean interface with FPS-stable 2D visuals. | 🎨 **轻量界面** —— 简洁 HUD，稳定 60 FPS。 |

---

## 🎮 Gameplay | 游戏玩法

**🎯 Goal | 目标**  
Avoid the falling meteors as long as possible and get the highest score!  
尽可能长时间地存活，避开陨石，获得更高分数！  

**⌨️ Controls | 操作说明**
| Key | Action | 按键 | 动作 |
|------|---------|------|------|
| ↑ / ↓ / ← / → | Move up/down/left/right | ↑ / ↓ / ← / → | 控制飞机移动 |
| P | Pause / Resume | P | 暂停或继续 |
| R | Restart after Game Over | R | 游戏结束后重开 |
| ESC | Quit | ESC | 退出游戏 |

---

## ⚙️ Installation | 安装

Make sure you have **Python 3.8+** installed.  
确保已安装 **Python 3.8 及以上版本**。

```bash
git clone https://github.com/yourusername/SkyDodger.git
cd SkyDodger
pip install pygame
```
---

## 🎮 Run the game | 运行游戏
```bash
python main.py # Manual Mode | 手动模式（Use arrow keys to control the plane manually）
python main.py --ai # AI Model | DQN智能体模式 
```
When the window opens, use arrow keys to control the plane and avoid the meteors. 
运行后使用方向键控制飞机，避开下落的陨石。

---

## 🧩 Train DQN Agent | 训练DQN智能体
```bash
python DQN_Model/train_dqn.py
```
After training, the model will be saved to `models/dqn_model.pth`.
Then test it in the visual game: 
```
python main.py --ai
```

---
## 📖 Project Structure | 项目结构
```bash
SkyDodger/
│
├── assets/                     # 图像资源（plane.png, meteor.png, background.png）
│
├── DQN_Model/                  # 强化学习模块
│   ├── agent_dqn.py            # 加载训练模型的智能体（推理）
│   ├── dqn_model.py            # Q-Network 模型定义
│   ├── replay_buffer.py        # 经验回放缓存
│   └── train_dqn.py            # 训练主脚本
│
├── models/
│   └── dqn_model.pth           # ✅ 训练生成的模型文件
│
├── rl_env.py                   # 数值版强化学习环境（用于训练）
├── game.py                     # 游戏主逻辑循环（含 AI 控制接口）
├── main.py                     # 程序入口（玩家/AI 两种模式）
├── player.py                   # 飞机类（玩家）
├── obstacle.py                 # 陨石类（障碍物）
├── ui.py                       # HUD 与结算界面
├── settings.py                 # 全局常量设置
└── README.md                   # 项目说明文件

```

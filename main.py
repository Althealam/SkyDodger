# main.py
import sys
from game import run_game

if __name__ == "__main__":
    if "--ai" in sys.argv:
        from DQN_Model.agent_dqn import DQNAgent
        agent = DQNAgent("./models/dqn_model.pth")
        run_game(agent=agent)
    else:
        run_game()

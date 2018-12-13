from Dealer import Dealer
from MCPlayer import MC_Player
from Arena import Arena
from Evaluate import Evaluate
from Draw import draw_value, draw_policy
from utils import epsilon_greedy_policy

A = ["继续叫牌", "停止叫牌"]
display = False
# 创建一个玩家一个庄家，玩家使用原始策略，庄家使用其固定的策略
player = MC_Player(A=A, display=display)
dealer = Dealer(A=A, display=display)
# 创建一个场景
arena = Arena(A=A, display=display)
# 生成num个完整的对局

evaluation = Evaluate(arena, player, dealer, 200000)
evaluation.policy_evaluate()

draw_value(player.Q, useable_ace=True, is_q_dict=True, A=player.A)
draw_policy(epsilon_greedy_policy, player.A,
            player.Q, epsilon=1e-10, useable_ace=True)
draw_value(player.Q, useable_ace=False, is_q_dict=True, A=player.A)
draw_policy(epsilon_greedy_policy, player.A, player.Q,
            epsilon=1e-10, useable_ace=False)

draw_value(evaluation.V, useable_ace=True, A=A)  # 绘制状态价值图
draw_value(evaluation.V, useable_ace=False, A=A)  # 绘制状态价值图

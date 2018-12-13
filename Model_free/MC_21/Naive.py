from Dealer import Dealer
from Player import Player
from Arena import Arena
from Evaluate import Evaluate
from Draw import draw_value

A = ["继续叫牌", "停止叫牌"]
display = False
# 创建一个玩家一个庄家，玩家使用原始策略，庄家使用其固定的策略
player = Player(A=A, display=display)
dealer = Dealer(A=A, display=display)
# 创建一个场景
arena = Arena(A=A, display=display)
# 生成num个完整的对局

evaluation = Evaluate(arena, player, dealer, 200000)
evaluation.policy_evaluate()

draw_value(evaluation.V, useable_ace=True, A=A)  # 绘制状态价值图
draw_value(evaluation.V, useable_ace=False, A=A)  # 绘制状态价值图

from utils import set_dict, get_dict, str_key
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def draw_value(value_dict, useable_ace=True, is_q_dict=False, A=None):
    # 定义figure
    fig = plt.figure()
    # 将figure变为3d
    ax = Axes3D(fig)
    # 定义x, y
    x = np.arange(1, 11, 1)  # 庄家第一张牌
    y = np.arange(12, 22, 1)  # 玩家总分数
    # 生成网格数据
    X, Y = np.meshgrid(x, y)
    # 从V字典检索Z轴的高度
    row, col = X.shape
    Z = np.zeros((row, col))
    if is_q_dict:
        n = len(A)
    for i in range(row):
        for j in range(col):
            state_name = str(X[i, j])+"_"+str(Y[i, j])+"_"+str(useable_ace)
            if not is_q_dict:
                Z[i, j] = get_dict(value_dict, state_name)
            else:
                assert(A is not None)
                for a in A:
                    new_state_name = state_name + "_" + str(a)
                    q = get_dict(value_dict, new_state_name)
                    if q >= Z[i, j]:
                        Z[i, j] = q
    # 绘制3D曲面
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color="lightgray")
    plt.show()


def draw_policy(policy, A, Q, epsilon, useable_ace=False):
    def value_of(a):
        if a == A[0]:
            return 0
        else:
            return 1
    rows, cols = 11, 10
    useable_ace = bool(useable_ace)
    Z = np.zeros((rows, cols))
    dealer_first_card = np.arange(1, 12)  # 庄家第一张牌
    player_points = np.arange(12, 22)
    for i in range(11, 22):  # 玩家总牌点
        for j in range(1, 11):  # 庄家第一张牌
            s = j, i, useable_ace
            s = str_key(s)
            a = policy(A, s, Q, epsilon)
            Z[i-11, j-1] = value_of(a)
            #print(s, a)

    plt.imshow(Z, cmap=mpl.cm.cool, interpolation=None,
               origin="lower", extent=[0.5, 11.5, 10.5, 21.5])

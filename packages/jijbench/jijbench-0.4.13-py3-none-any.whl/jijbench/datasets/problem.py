from __future__ import annotations

import json
import os
import pathlib
from typing import Dict, List, Tuple, Union

import jijmodeling as jm

from jijbench import datasets

__all__ = []


class JijModelingTarget:
    def __init__(
        self, problem, instance: Union[Tuple[str, Dict], List[Tuple[str, Dict]]]
    ):
        self.problem = problem
        self.instance = instance


class DefaultInstanceMixin:
    def _instance_dir(self, size: str):
        instance_dir = (
            pathlib.Path(__file__)
            .parent.joinpath("Instances")
            .joinpath(size)
            .joinpath(self.problem_name)
        )
        return instance_dir

    def instance_names(self, size: str) -> List[str]:
        instance_dir = self._instance_dir(size)
        instance_names = [
            p.name.split(".")[0]
            for p in instance_dir.glob(os.path.join("**", "*.json"))
        ]
        return instance_names

    def small_instance(self) -> List[Tuple[str, Dict]]:
        return [
            (name, self.load("small", name)) for name in self.instance_names("small")
        ]

    def medium_instance(self) -> List[str]:
        return [
            (name, self.load("medium", name)) for name in self.instance_names("medium")
        ]

    def large_instance(self) -> List[str]:
        return [
            (name, self.load("large", name)) for name in self.instance_names("large")
        ]

    def get_instance(self, size: str, instance_name: str) -> Dict:
        return self.load(size, instance_name=instance_name)

    def load(self, size: str, instance_name: str):
        instance_file_path = None
        for file_path in self._instance_dir(size).glob(os.path.join("**", "*.json")):
            if file_path.name.split(".")[0] == instance_name:
                instance_file_path = file_path
        if instance_file_path is None:
            raise FileNotFoundError(
                f"'{size}/{self.problem_name}/{instance_name}.json' is not found."
            )

        instance_path = instance_file_path.resolve()
        with open(instance_path, "r") as f:
            instance_data = json.load(f)

        return instance_data


class Knapsack(JijModelingTarget, DefaultInstanceMixin):
    def _problem(problem_name):
        w = jm.Placeholder("w", dim=1)
        v = jm.Placeholder("v", dim=1)
        n = jm.Placeholder("n")
        c = jm.Placeholder("c")
        x = jm.Binary("x", shape=(n,))

        # i: itemの添字
        i = jm.Element("i", n)

        problem = jm.Problem(problem_name)

        # objective function
        obj = jm.Sum(i, v[i] * x[i])
        problem += -1 * obj

        # Constraint: knapsack 制約
        const = jm.Constraint("knapsack-constraint", jm.Sum(i, w[i] * x[i]) - c <= 0)
        problem += const

        return problem

    problem_name = "knapsack"
    problem = _problem(problem_name)

    def __init__(self):
        super().__init__(self.problem, self.small_instance()[0])


class BinPacking(JijModelingTarget, DefaultInstanceMixin):
    def _problem(problem_name):
        w = jm.Placeholder("w", dim=1)
        num_items = jm.Placeholder("n")
        c = jm.Placeholder("c")

        # y[j]: bin j を使用するかしないか
        y = jm.Binary("y", shape=(num_items,))
        # x[i][j]: item i を bin j に入れるとき1
        x = jm.Binary("x", shape=(num_items, num_items))

        # i: itemの添字
        i = jm.Element("i", num_items)
        # j: binの添字
        j = jm.Element("j", num_items)

        problem = jm.Problem(problem_name)

        # objective function
        obj = y[:]
        problem += obj

        # Constraint1: 各itemをちょうど1つのbinにぶち込む
        const1 = jm.Constraint(
            "onehot-constraint", jm.Sum(j, x[i, j]) - 1 == 0, forall=i
        )
        problem += const1

        # Constraint2: knapsack制約
        const2 = jm.Constraint(
            "knapsack-constraint", jm.Sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j
        )
        problem += const2

        return problem

    problem_name = "bin-packing"
    problem = _problem(problem_name)

    def __init__(self):
        super().__init__(self.problem, self.small_instance()[0])


class NurseScheduling(JijModelingTarget, DefaultInstanceMixin):
    def _problem(problem_name):
        # 問題
        problem = jm.Problem(problem_name)

        I = jm.Placeholder("I")  # 人の数
        D = jm.Placeholder("D")  # 日数 D%7=0 とし, 月曜日からstartするとする
        W = jm.Placeholder("W")  # 週の数
        T = jm.Placeholder("T")  # シフトのタイプ数

        N = jm.Placeholder("N", dim=2)  # N[i] = 人iが必ず休む日

        # シフトtの次の日に働ないtypeのシフト R = [type1, type2, type3, ... ] = [[1, 2], [0, ], [], ...]
        R = jm.Placeholder("R", dim=2)
        l = jm.Placeholder("l", shape=(I,))  # シフトtの労働時間
        m_max = jm.Placeholder("m_max", shape=(I, T)).set_latex(
            r"\mathrm{m\_max}"
        )  # 従業員にシフトtを割当てられる最大回数
        b_min = jm.Placeholder("b_min", shape=(I,)).set_latex(
            r"\mathrm{b\_min}"
        )  # 各従業員の労働時間の最小値
        b_max = jm.Placeholder("b_max", shape=(I,)).set_latex(
            r"\mathrm{b\_max}"
        )  # 各従業員の労働時間の最大値
        c_min = jm.Placeholder("c_min", shape=(I,)).set_latex(
            r"\mathrm{c\_min}"
        )  # 各従業員の最小連続勤務数
        c_max = jm.Placeholder("c_max", shape=(I,)).set_latex(
            r"\mathrm{c\_max}"
        )  # 各従業員の最大連続勤務数
        o_min = jm.Placeholder("o_min", shape=(I,)).set_latex(
            r"\mathrm{o\_min}"
        )  # 各従業員の連続最低休日日数
        a_max = jm.Placeholder("a_max", shape=(I,)).set_latex(
            r"\mathrm{a\_max}"
        )  # 各従業員の週末働ける最大の回数
        # q[i, d, t] = 1, 人iは日にちdにtype tの仕事をしたい
        q = jm.Placeholder("q", shape=(I, D, T))
        # p[i, d, t] = 1, 人iは日にちdにtype tの仕事をしたくない
        p = jm.Placeholder("p", shape=(I, D, T))
        u = jm.Placeholder("u", shape=(D, T))  # 日にちd, type tの必要人数
        v_min = jm.Placeholder("v_min", shape=(D, T)).set_latex(
            r"\mathrm{v\_min}"
        )  # 人員不足のペナルティーの重み
        v_max = jm.Placeholder("v_max", shape=(D, T)).set_latex(
            r"\mathrm{v\_max}"
        )  # 人員過剰のペナルティーの重み

        len_R = R.shape[0]

        # Element
        i = jm.Element("i", (0, I))
        d = jm.Element("d", (0, D))
        t = jm.Element("t", (0, T))
        w = jm.Element("w", (0, W))
        dt = jm.Element("dt", (0, len_R))
        j = jm.Element("j", (0, D))
        s = jm.Element("s", (0, D))

        # 決定変数
        x = jm.Binary("x", shape=(I, D, T))  # 人iを日にちdにシフトtを割当てるかどうか
        k = jm.Binary("k", shape=(I, W))  # week wに働いたかどうか
        y = jm.Integer("y", lower=0, upper=u, shape=(D, T))  # 日dのシフトtの不足人数
        z = jm.Integer("z", lower=0, upper=u, shape=(D, T))  # 日dのシフトtの過剰人数

        # Objective Function
        term1 = jm.Sum([i, d, t], q[i, d, t] * (1 - x[i, d, t]))  # シフト入りの希望を叶える
        term2 = jm.Sum([i, d, t], p[i, d, t] * x[i, d, t])  # シフト休みの希望を叶える
        term3 = jm.Sum([d, t], y[d, t] * v_min[d, t])  # 人員不足のペナルティー
        term4 = jm.Sum([d, t], z[d, t] * v_max[d, t])  # 人員過剰のペナルティー
        problem += term1 + term2 + term3 + term4

        # Constraint1: 1人一つの仕事しか割り当てられない
        const1 = jm.Sum(t, x[i, d, t])
        problem += jm.Constraint("assign", const1 - 1 <= 0, forall=[i, d])

        # Constraint2: 特定の仕事を行った次の日に, 特定の仕事を行うことはできない
        problem += jm.Constraint(
            "shift-rotation",
            x[i, d, t] + x[i, (d + 1), dt] - 1 <= 0,
            forall=[i, (d, (d != D - 1)), t, (dt, (R[t, dt] != -1))],
        )

        # Constraint3: 従業員に割り当てられる各タイプのシフトの最大数
        const3 = jm.Sum(d, x[i, d, t]) - m_max[i, t]
        problem += jm.Constraint("assign-max", const3 <= 0, forall=[i, t])

        # Constraint4: 最低・最高労働時間
        const4 = jm.Sum([d, t], l[t] * x[i, d, t])
        problem += jm.Constraint(
            "minimum-work-time",
            b_min[i] - const4 <= 0,
            forall=[
                i,
            ],
        )
        problem += jm.Constraint(
            "maximum-work-time",
            const4 - b_max[i] <= 0,
            forall=[
                i,
            ],
        )

        # Constraint5: 最大連続勤務
        j5 = jm.Element("j5", (d, d + c_max[i] + 1))
        const5 = jm.Sum([j5, t], x[i, j5, t])
        problem += jm.Constraint(
            "maximum-consecutive-shifts",
            const5 - c_max[i] <= 0,
            forall=[i, (d, d <= D - (c_max[i] + 1))],
        )

        # Constraint6: 最小連続勤務
        s6 = jm.Element("s6", (1, c_min[i]))
        j6 = jm.Element("j6", (d + 1, d + s6 + 1))
        problem += jm.Constraint(
            "minimum-consecutive-shifts",
            jm.Sum(t, x[i, d, t])
            + (s6 - jm.Sum([j6, t], x[i, j6, t]))
            + jm.Sum(t, x[i, d + s6 + 1, t])
            - 1
            >= 0,
            forall=[i, s6, (d, d < (D - (s6 + 1)))],
        )

        # Constraint7: 最低連続休暇日数
        s7 = jm.Element("s7", (1, o_min[i]))
        j7 = jm.Element("j7", (d + 1, d + s7 + 1))
        problem += jm.Constraint(
            "minimum-consecutive-days-off",
            (1 - jm.Sum(t, x[i, d, t]))
            + jm.Sum([j7, t], x[i, j7, t])
            + (1 - jm.Sum(t, x[i, d + s7 + 1, t]))
            - 1
            >= 0,
            forall=[i, s7, (d, d < (D - (s7 + 1)))],
        )

        # Constraint8: 週末休みの最大回数
        const8 = jm.Sum(t, x[i, 7 * (w + 1) - 2, t]) + jm.Sum(
            t, x[i, 7 * (w + 1) - 1, t]
        )
        problem += jm.Constraint(
            "variable-k-lower", k[i, w] - const8 <= 0, forall=[i, w]
        )
        problem += jm.Constraint(
            "variable-k-upper", const8 - 2 * k[i, w] <= 0, forall=[i, w]
        )
        problem += jm.Constraint(
            "maximum-number-of-weekends",
            jm.Sum(w, k[i, w]) - a_max[i] <= 0,
            forall=[
                i,
            ],
        )

        # Constraint9: 働けない日の制約
        d_o = jm.Element("do", N[i]).set_latex(r"{\mathrm d\_o}")
        problem += jm.Constraint(
            "days-off", x[i, d_o, t] == 0, forall=[i, (d_o, d_o != -1), t]
        )

        # Constraint10: 必要人数に関する制約
        const10 = jm.Sum(i, x[i, d, t]) - z[d, t] + y[d, t] - u[d, t]
        problem += jm.Constraint("cover-requirements", const10 == 0, forall=[d, t])

        return problem

    problem_name = "nurse-scheduling"
    problem = _problem(problem_name)

    def __init__(self):
        super().__init__(self.problem, self.small_instance()[0])


class TSPTW(JijModelingTarget, DefaultInstanceMixin):
    def _problem(problem_name):
        # 問題
        problem = jm.Problem(problem_name)

        # 距離行列
        dist = jm.Placeholder("d", dim=2)  # 距離行列
        N = jm.Placeholder("N")
        e = jm.Placeholder("e", shape=(N,))  # ready time
        l = jm.Placeholder("l", shape=(N,))  # due time
        x = jm.Binary("x", shape=(N, N))
        t = jm.Integer("t", shape=(N,), lower=e, upper=l)

        i = jm.Element("i", N)
        j = jm.Element("j", N)

        # Objevtive Function: 距離の最小化
        sum_list = [i, (j, j != i)]
        obj = jm.Sum(sum_list, dist[i, j] * x[i, j])
        problem += obj

        # Const1: 都市iから出る辺は1つ
        term1 = jm.Sum((j, j != i), x[i, j])
        problem += jm.Constraint(
            "onehot-constraint1",
            term1 == 1,
            forall=[
                i,
            ],
        )

        # Const2: 都市iに入る辺は1つ
        term2 = jm.Sum((j, j != i), x[j, i])
        problem += jm.Constraint(
            "onehot-constraint2",
            term2 == 1,
            forall=[
                i,
            ],
        )

        # Const3: Time Windows制約
        term3 = t[i] + dist[i, j] - t[j] - 20 * (1 - x[i, j])
        forall_list = [(j, j != 0), (i, (i != 0) & (i != j))]
        problem += jm.Constraint(
            "time-window-constraint", term3 <= 0, forall=forall_list
        )

        return problem

    problem_name = "travelling-salesman-with-time-windows"
    problem = _problem(problem_name)

    def __init__(self):
        super().__init__(self.problem, self.small_instance()[0])


class TSP(JijModelingTarget, DefaultInstanceMixin):
    def _problem(problem_name):
        # 問題
        problem = jm.Problem(problem_name)
        dist = jm.Placeholder("d", dim=2)
        N = jm.Placeholder("N")

        x = jm.Binary("x", shape=(N, N))
        i = jm.Element("i", N)
        j = jm.Element("j", N)

        t = jm.Element("t", N)

        # Objective Funtion
        sum_list = [t, i, j]
        obj = jm.Sum(sum_list, dist[i, j] * x[t, i] * x[(t + 1) % N, j])
        problem += obj

        # const1: onehot for time
        const1 = x[t, :]
        problem += jm.Constraint(
            "onehot-time",
            const1 == 1,
            forall=[
                t,
            ],
        )

        # const2: onehot for location
        const2 = x[:, i]
        problem += jm.Constraint(
            "onehot-location",
            const2 == 1,
            forall=[
                i,
            ],
        )

        return problem

    problem_name = "travelling-salesman"
    problem = _problem(problem_name)

    def __init__(self):
        super().__init__(self.problem, self.small_instance()[0])


def get_problem(problem_name):
    return getattr(datasets, problem_name).problem

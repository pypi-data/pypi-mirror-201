import pandas as pd


class CalcTop5Class:
    def __init__(self):
        self._data = []
        self._top5 = []
        self._dropped = []

    def count_top5(self, target_row):
        """
        Top5のデータを集計する（上位6位以下の合計を計算し、Othersとする）
        """
        self._data = target_row.value_counts(sort=True) / target_row.value_counts().sum() * 100
        self._top5 = self._data[:5]
        self._dropped = self._data.drop(self._top5.index)
        self._top5["(Others)"] = pd.Series(self._dropped[0:].sum(), dtype="float64").to_string(index=False)
        return self._top5


class DrawPiChartClass:
    def __init__(self):
        self._colors = ["#2466a9", "#3f86bf", "#609fc6", "#88b5ce", "#bcd4e5", "#B2B2B2"]  # Blue palette
        self._wedgeprops = {"alpha": 0.9, "edgecolor": "white", "linewidth": 1, "width": 0.7}
        self._textprops = {"weight": "bold", "color": "#ffff00", "fontsize": "12"}

    def pi_chart(self, ax, data, title):
        """
        円グラフを描画する
        """
        ax.pie(data, colors=self._colors, startangle=90, counterclock=False,
               labels=data.index, pctdistance=0.7,
               autopct=lambda p: "{: .0f}%".format(p) if p >= 3 else "",
               wedgeprops=self._wedgeprops, textprops=self._textprops, labeldistance=None)
        ax.legend(loc="upper left", bbox_to_anchor=(1.3, 0.9),
                  prop={"size": "14", "weight": "bold"}, frameon=False, ncol=1)
        ax.set_title(title, loc="left", pad=10, fontsize="20", fontweight="bold", color="black")


def draw_pi_chart(data_frame, fig_a, fig_b):
    """
    Draw pi chart for top 5
    """
    global top5
    top5 = [0] * 4

    calc = CalcTop5Class()

    for i in range(len(top5)):
        top5[i] = calc.count_top5(data_frame.iloc[:, i + 1])

    fig_a.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)
    fig_b.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)

    ax_a_1 = fig_a.add_subplot(2, 1, 1)
    ax_a_2 = fig_a.add_subplot(2, 1, 2)
    ax_b_1 = fig_b.add_subplot(2, 1, 1)
    ax_b_2 = fig_b.add_subplot(2, 1, 2)

    ax_a_1.set_position([0.02, 0.46, 0.4, 0.3])
    ax_a_2.set_position([0.02, 0.06, 0.4, 0.3])
    ax_b_1.set_position([0.02, 0.46, 0.4, 0.3])
    ax_b_2.set_position([0.02, 0.06, 0.4, 0.3])

    draw = DrawPiChartClass()

    draw.pi_chart(ax_a_1, top5[0], "Terminating Rule Group")
    draw.pi_chart(ax_a_2, top5[1], "URI")
    draw.pi_chart(ax_b_1, top5[2], "IP Address")
    draw.pi_chart(ax_b_2, top5[3], "Country")

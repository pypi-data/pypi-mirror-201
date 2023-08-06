import datetime
import numpy as np


class DrawHistgramClass:
    def __init__(self):
        self._hours = 3
        self._bins = 0
        self._label_and_count = ""
        self._xlocation = []
        self._all_xlocation = []
        self._xlabel = []
        self._jst_offset = 3600 * 9 * 1000
        self._1day_seconds = 3600 * 24 * 1000
        self._xlabel_threshold = 0

    def histgram(self, ax, time, target, label, color):
        """
        Create settings for histgram
        """
        self._calc_xticks_and_labels(time[0], time[len(time) - 1])
        self._bins = int((self._last_xlocation - self._first_xlocation - self._1day_seconds)
                         / 1000 / (3600 * self._hours)) + 8  # margin = 8
        self._label_and_count = label + " (" + str(len(target)) + ")"
        ax.axhspan(10, 20, color="gray", alpha=0.05)
        ax.axhspan(30, 40, color="gray", alpha=0.05)
        ax.hist(target, alpha=0.7, bins=self._bins, range=(self._first_xlocation, self._last_xlocation),
                label=self._label_and_count, color=color, edgecolor="white", linewidth=0)
        ax.grid(True)
        ax.set_ylim(0, 50)
        ax.legend(loc="upper left", prop={"size": 12}, fancybox=True,
                  edgecolor="gray", facecolor="white", framealpha=1)

        self._calc_xticks_and_labels(time[0], time[len(time) - 1])
        ax.set_xticks(self._xlocation)
        ax.set_xticklabels(self._xlabel)
        ax.tick_params(labelsize=10)

    def _calc_xticks_and_labels(self, end_time, start_time):
        self._last_xlocation = end_time - end_time % (self._1day_seconds) + self._1day_seconds - self._jst_offset
        self._first_xlocation = start_time - start_time % (self._1day_seconds) - self._jst_offset
        self._number_of_labels = int((self._last_xlocation - self._first_xlocation) / self._1day_seconds) + 1
        self._all_xlocation = np.linspace(self._last_xlocation, self._first_xlocation, self._number_of_labels, dtype=int)

        self._xlabel_threshold = int(self._number_of_labels / 5) if (int(self._number_of_labels / 5)) > 2 else 2

        self._xlocation = []
        if self._number_of_labels > 7:
            for i in range(len(self._all_xlocation)):
                if (i % self._xlabel_threshold == 1):
                    self._xlocation.append(self._all_xlocation[i])
        else:
            self._xlocation = self._all_xlocation

        self._xlabel = []
        for i in range(len(self._xlocation)):
            self._xlabel.append(datetime.datetime
                                .fromtimestamp(self._xlocation[i] / 1000.0)
                                .strftime("%m/%d(%a) %H:%M"))


def draw_histgram(waf_log, fig):
    """
    Draw two histgrams
    """
    TITLE_OF_TOTAL = "Total Number of Access"
    TITLE_OF_RULES = "AWS Managed Rule and Third Party Rule"

    fig.subplots_adjust(top=0.8, left=-0.5, hspace=0.2)
    ax_1 = fig.add_subplot(2, 1, 1)
    ax_2 = fig.add_subplot(2, 1, 2)

    ax_1.set_position([0.1, 0.48, 0.8, 0.2])
    ax_2.set_position([0.1, 0.14, 0.8, 0.2])

    ax_1.set_title(TITLE_OF_TOTAL, loc="left", pad=10, fontsize="20", fontweight="bold", color="black")
    ax_2.set_title(TITLE_OF_RULES, loc="left", pad=10, fontsize="20", fontweight="bold", color="black")

    aws_managed = waf_log[waf_log.rule.str.match('^AWS')]
    third_party = waf_log[waf_log.rule.str.match('^(?!AWS)')]

    draw = DrawHistgramClass()

    draw.histgram(ax_1, waf_log["time"], waf_log["time"], "Total", "gray",)
    draw.histgram(ax_2, waf_log["time"], aws_managed["time"], "AWS Managed", "indianred",)
    draw.histgram(ax_2, waf_log["time"], third_party["time"], "Third Party", "skyblue",)

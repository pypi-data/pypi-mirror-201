import datetime
import json
import site
import os
import matplotlib.lines as lines
from PIL import Image

# REPORT_MAIN_COLOR = "#883D1A"
# MAIN_COLOR = "#56c3ed"
LOGO_FILE = "logo_trans_small.png"


class WriteHeaderFooterClass():
    """
    Write header and footer class
    """

    def __init__(self):

        self._dic_box = {
            "facecolor": "White",
            "edgecolor": "#2b7700",
            "boxstyle": "Square, pad=0.5",
            "linewidth": 3,
        }

    def header_footer(self, fig, page_number, term, color):
        with open("./previous_music.json", mode="r") as f:
            settings_dict = json.load(f)

        MAIN_COLOR = color

        # Header
        page_title = "AWS WAF Log  ( Action: " + settings_dict["mode"] + " )"
        web_acl = settings_dict["web_acl"].lstrip("aws-waf-logs-")
        fig.add_artist(lines.Line2D([0, 1], [0.94, 0.94], color=MAIN_COLOR, linewidth=80, zorder=0))

        fig.text(0.05, 0.91, page_title, color="#ffffff", fontsize=26, fontweight="bold")
        fig.text(0.70, 0.8, "WebACL: " + web_acl, color="#2b7700", fontsize=16, fontweight="bold", bbox=self._dic_box)
        fig.text(0.72, 0.74, term, color="black", fontsize=12)

        # Footer
        fig.add_artist(lines.Line2D([0, 1], [0.0004, 0.0004], color=MAIN_COLOR, linewidth=80, zorder=0))
        fig.text(0.9, 0.025, page_number, color="#d3b734", fontsize=20, fontweight="bold")

        # Logo
        logo_path = "".join(site.getsitepackages()) + "/accompanist/resource/" + LOGO_FILE
        if os.path.isfile(logo_path):
            fig.figimage(Image.open(logo_path), xo=500, yo=7)
        else:
            print("Logo file is not found.")


def calc_term(time):
    """
    Show term
    """
    with open("./previous_music.json", mode="r") as f:
        settings_dict = json.load(f)

    oldest_time = datetime.datetime.fromtimestamp(time[len(time) - 1] / 1000.0).strftime("%m/%d %H:%M")
    latest_time = datetime.datetime.fromtimestamp(time[0] / 1000.0).strftime("%m/%d %H:%M")

    days = str(settings_dict["days"])
    return oldest_time + " - " + latest_time + " ( " + days + " days )"


def write_header_and_footer(waf_log_time, figs, color):
    """
    Add header and footer
    """
    term = calc_term(waf_log_time)

    write = WriteHeaderFooterClass()

    for fig in (figs):
        page_number = str(figs.index(fig) + 1) + " / " + str(len(figs))
        write.header_footer(fig, page_number, term, color)


def write_comment(fig):
    """
    Add comment page (last page)
    """
    with open("config.json", mode="r") as f:
        config_dict = json.load(f)

    comment_item_1 = config_dict["comment"][0]
    comment_item_2 = config_dict["comment"][1]
    comment_item_3 = config_dict["comment"][2]
    comment_item_4 = config_dict["comment"][3]
    comment_item_5 = config_dict["comment"][4]

    fig.text(0.1, 0.7, "Comment", color="black", fontsize=20, fontweight="bold")
    fig.text(0.1, 0.6, comment_item_1, color="black", fontsize=20, wrap=True, fontfamily="YuGothic")
    fig.text(0.1, 0.5, comment_item_2, color="black", fontsize=20, wrap=True, fontfamily="YuGothic")
    fig.text(0.1, 0.4, comment_item_3, color="black", fontsize=20, wrap=True, fontfamily="YuGothic")
    fig.text(0.1, 0.3, comment_item_4, color="black", fontsize=20, wrap=True, fontfamily="YuGothic")
    fig.text(0.1, 0.2, comment_item_5, color="black", fontsize=20, wrap=True, fontfamily="YuGothic")

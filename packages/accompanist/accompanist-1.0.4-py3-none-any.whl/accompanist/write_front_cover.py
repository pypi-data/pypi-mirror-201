import site
import matplotlib.lines as lines
from PIL import Image

LOGO_FILE = "logo_trans.png"


def write_front_cover(fig, color):
    """
    Write cover of report
    """
    fig.add_artist(lines.Line2D([0, 1], [0.24, 0.24], color=color, linewidth=306, zorder=0))

    title_1 = "AWS WAF Log"
    title_2 = "Analysis Report"
    empowerd = "empowered by"

    fig.text(0.1, 0.80, title_1, color="#000000", fontsize=50, fontweight="bold")
    fig.text(0.1, 0.66, title_2, color="#000000", fontsize=50, fontweight="bold")
    fig.text(0.41, 0.36, empowerd, color="#ffffff", fontsize=24)

    logo_location = "".join(site.getsitepackages()) + "/accompanist/resource/" + LOGO_FILE
    fig.figimage(Image.open(logo_location), xo=360, yo=100)

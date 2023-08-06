import json
import numpy as np


def draw_table(waf_log, fig):
    """
    Draw a table
    """
    TABLE_TITLE = "Number of Requests per URI"
    uri_data = calc_count_of_uris(waf_log)

    fig.subplots_adjust(top=0.8, left=0.2, right=0.8, hspace=0.1)
    ax = fig.add_subplot(1, 1, 1)
    ax.axis("off")
    ax.set_title(TABLE_TITLE, loc="left", y=0.8, x=-0.14, fontsize="20",
                 fontweight="bold", color="black")

    col_labels = ["No.", "URI", "Count"]
    col_widths = [0.1, 0.7, 0.1]
    col_colors = ["#000000", "#000000", "#000000"]

    cell_colors = np.full_like(uri_data, "", dtype=object)
    for i in range(len(uri_data)):
        if i % 2 == 0:
            for j in range(3):
                cell_colors[i, j] = "#FFFFFF"
        else:
            for j in range(3):
                cell_colors[i, j] = "#F2F2F2"

    uri_table = ax.table(cellText=uri_data,
                         cellColours=cell_colors,
                         colLabels=col_labels,
                         colColours=col_colors,
                         colWidths=col_widths,
                         colLoc="center",
                         loc="center",
                         )

    for i in range(1, len(uri_data) + 1):
        uri_table[i, 0]._text.set_horizontalalignment("center")
        uri_table[i, 1]._text.set_horizontalalignment("left")
        uri_table[i, 2]._text.set_horizontalalignment("right")

    for j in range(0, 3):
        uri_table[0, j]._text.set_color("white")

    for i in range(0, len(uri_data)):
        if int(uri_data[i][2]) >= 10:
            uri_table[i + 1, 2]._text.set_color("red")
        elif int(uri_data[i][2]) >= 2:
            uri_table[i + 1, 2]._text.set_color("orange")

    uri_table.scale(1.44, 2.6)
    uri_table.auto_set_font_size(False)
    uri_table.set_fontsize(20)


def calc_count_of_uris(waf_log):
    """
    Count the number of URIs
    """

    f = open("./config.json", "r")
    settings_file = json.load(f)
    f.close()

    uris = settings_file["target_uri"]
    counted_uris = []
    for uri in uris:
        count = 0
        index = uris.index(uri) + 1
        if uri in waf_log["uri"].values:
            count = waf_log.groupby("uri").get_group(uri)["uri"].count()
        counted_uris.append([index, uri, count])

    return (counted_uris)

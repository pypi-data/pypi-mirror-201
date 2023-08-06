import click
import subprocess

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages as pp

import accompanist.write_front_cover as wf
import accompanist.draw_histgram as dh
import accompanist.draw_pi_chart as dp
import accompanist.draw_table as dt
import accompanist.utility_module as um


@click.command(name="play")
@click.option("--color", required=False, default="#be5126")
def play(color):
    INPUT_CSV_FILE = "./waf-log.csv"
    OUTPUT_PDF_FILE = "./waf-report.pdf"
    A4_SIZE = (11.69, 8.27)

    # Pre-Process
    waf_log = pd.read_csv(INPUT_CSV_FILE, header=None)
    waf_log.columns = ["time", "rule", "uri", "ip", "country"]

    plt.rcParams["font.family"] = "Arial"

    fig_1 = plt.figure(figsize=A4_SIZE)
    fig_2 = plt.figure(figsize=A4_SIZE)
    fig_3 = plt.figure(figsize=A4_SIZE)
    fig_4 = plt.figure(figsize=A4_SIZE)
    fig_5 = plt.figure(figsize=A4_SIZE)
    fig_6 = plt.figure(figsize=A4_SIZE)

    figs = [fig_1, fig_2, fig_3, fig_4, fig_5, fig_6]
    body_page = [fig_2, fig_3, fig_4, fig_5, fig_6]

    # Add front cover
    wf.write_front_cover(fig_1, color)

    # Calculation & Draw
    dh.draw_histgram(waf_log, fig_2)
    dp.draw_pi_chart(waf_log, fig_3, fig_4)
    dt.draw_table(waf_log, fig_5)
    um.write_comment(fig_6)

    # Post-Process
    um.write_header_and_footer(waf_log["time"], body_page, color)

    pdf = pp(OUTPUT_PDF_FILE)

    for i in figs:
        pdf.savefig(i)

    pdf.close()

    subprocess.Popen("open " + OUTPUT_PDF_FILE, shell=True)

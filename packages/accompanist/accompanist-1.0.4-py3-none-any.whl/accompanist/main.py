import click
from accompanist.listen import listen as listen_cmd
from accompanist.play import play as play_cmd


@click.group()
def cmd():
    pass


cmd.add_command(listen_cmd)
cmd.add_command(play_cmd)

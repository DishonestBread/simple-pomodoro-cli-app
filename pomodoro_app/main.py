import sys
import time
from typing import Annotated, Optional
import typer
import chime
import os
import subprocess

app = typer.Typer(help="Pomodoro timer")

@app.command()
def main(
    work_time: Annotated[int, typer.Option(prompt="Work period in minutes: ")],
    rest_time: Annotated[int, typer.Option(prompt="Break period in minutes: ")],
):
    timer(work_time, rest_time)

def timer(work_time: int, rest_time: int):
    clear()

    countdown(work_time * 60)

    if typer.confirm("Type y to start a break or n to end"):
        clear()
        countdown(rest_time * 60)
    else:
        typer.echo("Pomodoro ended")
        return
    

def countdown(total_seconds):
    for remaining in range(total_seconds, -1, -1):
        mins, secs = divmod(remaining, 60)

        sys.stdout.write(f"\rTime remaining: {mins:02d}:{secs:02d}")
        sys.stdout.flush()

        if remaining > 0:
            time.sleep(1)

    sys.stdout.write("\rTimes up \n")
    chime.success()

def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
        app()
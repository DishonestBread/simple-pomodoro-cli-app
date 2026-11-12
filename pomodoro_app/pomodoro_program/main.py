import sys
import time
from typing import Annotated, Optional
import typer
import chime
import os
import subprocess
import shutil
import pyfiglet
import math

app = typer.Typer(help="Pomodoro timer")

@app.command()
def main(
    work_time: Annotated[int, typer.Option(prompt="Work period in minutes")] = 50,
    rest_time: Annotated[int, typer.Option(prompt="Break period in minutes")] = 10,
    sound: Annotated[str, typer.Option(prompt="Sounds (minecraft, rain, lofi+rain)")] = "",
):
    if (sound == ""):
        timer(work_time, rest_time, 0)
    else:
        mpv = start_sound(sound)
        try: 
            timer(work_time, rest_time, 0)
        finally:
            stop_sound(mpv)


def timer(work_time, rest_time, session):
    session += 1

    clear()

    notify("Timer started")

    countdown(work_time * 60, session)

    if typer.confirm("Start break?"):
        clear()
        countdown(rest_time * 60, session)

        if typer.confirm("Start Work?"):
            clear()
            timer(work_time, rest_time, session)
        else:
            typer.echo("Pomodoro ended")
            return
    else:
        typer.echo("Pomodoro ended")
        return
    

def countdown(total_seconds, session):
    end = time.monotonic() + total_seconds
    last_shown = None

    width = shutil.get_terminal_size().columns
    spaces = " " * (width//2 - (49//2))
    height = shutil.get_terminal_size().lines
    top = "\n" * (height//2 - (8//2) - 3)

    sys.stdout.write("\033[?25l")

    try:
        while True:
            remaining = max(0, math.ceil(end - time.monotonic()))

            if remaining != last_shown:
                last_shown = remaining
                mins, secs = divmod(remaining, 60)
                response = pyfiglet.figlet_format(
                    f"{mins:02d}:{secs:02d}", font="banner3-D", width=width
                )

                txt = response.split("\n")
                spaces_txt = "\n".join(spaces + i for i in txt)

                sys.stdout.write("\033[H\033[J")
                sys.stdout.write("Session: " + str(session) + "\n" + "Time remaining:\n\n" + top + spaces_txt + "\n")
                sys.stdout.flush()

            if remaining == 0:
                break

            time.sleep(0.1)
    finally:
        sys.stdout.write("\033[?25h")

    notify("Timer end")
    chime.success()


def notify(message):

    img_file_path = "/home/dishonestbread/Pictures/catthrowingtomato.jpg"
    subprocess.run(["notify-send", "-i", img_file_path, "Pomo", message])
    

def start_sound(sound):

    sound_files = {
        "minecraft" : "/home/dishonestbread/Videos/no more thinking tonight... (minecraft music w⧸ soft rain) [yJ6Lbsmb1lY].webm",
        "rain" : "/home/dishonestbread/Videos/Rain Sound On Window with Thunder SoundsㅣHeavy Rain for Sleep, Study and Relaxation, Meditation [mPZkdNFkNps].webm",
        "lofi+rain" : "/home/dishonestbread/Videos/Dreamy Lofi Rain 🌧️ Rain & Lofi for Insomnia Relief [uEQ7fH7ViXo].webm"
    }

    return subprocess.Popen(
        ["mpv", "--no-video", "--loop=inf", "--volume=100", "--af=volume=6dB,alimiter=limit=0.95", sound_files[sound]],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def stop_sound(mpv):
    mpv.terminate()
    mpv.wait()


def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
        app()
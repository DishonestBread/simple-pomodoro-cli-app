import sys
import time
from typing import Annotated, Optional
import typer
import chime
import os
import subprocess
import shutil
import pyfiglet


app = typer.Typer(help="Pomodoro timer")

@app.command()
def main(
    work_time: Annotated[int, typer.Option(prompt="Work period in minutes")] = 25,
    rest_time: Annotated[int, typer.Option(prompt="Break period in minutes")] = 5,
    sound: Annotated[str, typer.Option(prompt="Sounds (minecraft, lofi, lofi+rain)")] = "",
):
    if (work_time  and rest_time == " "):
        timer(50, 10)
    else:
        if (sound == ""):
            timer(work_time,rest_time)
        else:
            mpv = start_sound(sound)
            try: 
                timer(work_time, rest_time)
            finally:
                stop_sound(mpv)


def timer(work_time: int, rest_time: int):
    clear()

    notify("Timer started")

    countdown(work_time * 60)

    if typer.confirm("Start break? "):
        clear()
        countdown(rest_time * 60)

        if typer.confirm("Start Work? "):
            clear()
            timer(work_time, rest_time)
        else:
            typer.echo("Pomodoro ended")
            return
    else:
        typer.echo("Pomodoro ended")
        return
    

def countdown(total_seconds):
    for remaining in range(total_seconds, -1, -1):
        mins, secs = divmod(remaining, 60)

        width = shutil.get_terminal_size().columns
        result = pyfiglet.figlet_format(
            f"Time remaining: {mins:02d}:{secs:02d}", font = "banner3-D", width=width
        )
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(result)
        sys.stdout.flush()

        if remaining > 0:
            time.sleep(1)

    sys.stdout.write("\rTimes up \n")
    notify("Timer end")
    chime.success()


def notify(message):

    img_file_path = "/home/dishonestbread/Pictures/catthrowingtomato.jpg"
    subprocess.run(["notify-send", "-i", img_file_path, "Pomo", message])
    

def start_sound(sound):

    sound_files = {
        "minecraft" : "/home/dishonestbread/Videos/no more thinking tonight... (minecraft music w⧸ soft rain) [yJ6Lbsmb1lY].webm",
        "rain" : "Rain Sound On Window with Thunder SoundsㅣHeavy Rain for Sleep, Study and Relaxation, Meditation [mPZkdNFkNps].webm",
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
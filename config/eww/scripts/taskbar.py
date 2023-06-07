import subprocess as sp
import json
import os
import sys

# Environment variables
HOME = os.getenv("HOME")


def pinned_window(theme: str):
    pack = "We10X" if theme == "light" else "We10X-dark"
    icon = lambda name: f"{HOME}/.local/share/icons/{pack}/apps/scalable/{name}.svg"

    return [
        {"class": "org.gnome.Nautilus", "icon": icon("nautilus"), "count": 0},
        {"class": "firefox", "icon": icon("firefox"), "count": 0, "run": "firefox &"},
        {
            "class": "Alacritty",
            "icon": icon("terminal"),
            "count": 0,
            "run": "alacritty &",
        },
        {"class": "Code", "icon": icon("vscode"), "count": 0, "run": "code &"},
        {
            "class": "pamac-manager",
            "icon": icon("software-store"),
            "count": 0,
            "run": "pamac-manager &",
        },
        {
            "class": "gnome-control-center",
            "icon": icon("gnome-control-center"),
            "count": 0,
            "run": "gnome-control-center &",
        },
    ]


def remove_duplicates(input_data):
    classes = []
    clients = []
    for client in input_data:
        if not (client["class"] in classes):
            classes.append(client["class"])
            clients.append(client)
    return clients


def count_duplicates(openned_windows, pinned_windows):
    aux_pinned = pinned_windows.copy()
    for pinned in aux_pinned:
        for window in openned_windows:
            if pinned["class"] == window["class"]:
                pinned["count"] += 1
    return aux_pinned


def get_windows():
    output = sp.check_output(
        "hyprctl clients -j | jq 'map(select(.class != \"\")) | map({ class: .class })'",
        shell=True,
    )
    return json.loads(output)


def get_active_window():
    output = sp.check_output("hyprctl activewindow -j", shell=True)
    data = json.loads(output)
    return data.get("class", "") or data.get("initialClass", "")


def get_current_theme():
    with open(f"{HOME}/.config/eww/widgets/variables.yuck", "r") as f:
        theme = "".join(filter(str.isalnum, f.readline().split(" ")[-1]))
    return theme


if __name__ == "__main__":
    theme = get_current_theme()

    windows = get_windows()
    acitve_window = get_active_window()
    pinned = pinned_window(theme)

    clients = count_duplicates(windows, pinned)
    if clients:
        for client in clients:
            client["focused"] = acitve_window == client["class"]
        print(json.dumps(clients))
    else:
        print([])

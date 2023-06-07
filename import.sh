#!/bin/bash

# Variables
ALACRITTY="$HOME/.config/alacritty"
HYPR="$HOME/.config/hypr"
EWW="$HOME/.config/eww"
NVIM="$HOME/.config/nvim/"

if [ -d "config" ]; then 
    echo "Deleting already existing config directory"
    rm -rf ./config/*
else
    mkdir config
fi

# Alacritty
echo "Copying Alacritty config"
cp -r $ALACRITTY config/alacritty

# Hypr and Hyprland
echo "Copying Hypr config"
cp -r $HYPR config/hypr

# Eww
echo "Copying eww config"
cp -r $EWW config/eww

# Neovim + NvChad
echo "Copying nvim and nvChad config"
cp -r $NVIM config/nvim

echo "Done !"

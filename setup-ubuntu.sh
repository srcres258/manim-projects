#!/usr/bin/env bash

echo "Installing necessary apt packages..."
sudo apt update
sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg
sudo apt install texlive texlive-latex-extra

echo "Installing necessary LaTeX macro packages..."
sudo tlmgr install collection-basic amsmath babel-english cbfonts-fd cm-super ctex doublestroke\
                   dvisvgm everysel fontspec frcursive fundus-calligra gnu-freefont jknapltx\
                   latex-bin mathastext microtype ms physics preview ragged2e relsize rsfs\
                   setspace standalone tipa wasy wasysym xcolor xetex xkeyval\

echo "Installing necessary pip packages..."
pip install -r requirements.txt

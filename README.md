# Google Calendar for Conky

## Description

fetch google calendar events and write them to a (conky config) file  
in order to display it on the desktop

## Install

1. Copy `configuration/configuration.template.yaml` and rename it to `configuration/configuration.yaml`
2. Fill out the configuration based on the comments within
3. Add the start and end tags to your conky conf file
4. Install required python libraries with `pip install .` (or `pip install -e .` if you plan on editing the code)
5. run the program with `python fetch_today.py`
6. Install sytemd files
  a. Move files in `./systemd` to your system's `systemd` folder  
  b. Edit the variables (eg. paths, timer interval) in the sytemd files  
  c. Enable and start them  

## Miscellaneous

This is a hobby project.  
There will be bugs.  
Use this project at your own risk.  
I do not take any responsible for data loss or other damages.  
Should something be unclear or you find bugs - open an issue on [GitHub](https://github.com/TomLouisKeller/gcal_conky)

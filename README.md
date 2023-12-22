# noise solutions

do you live near an airport and can always hear the planes above and can't help but think of how we created these huge machines to fly people and things around the world in amounts of time inconveivable like 100 years ago now we can just go to another country whenever we want as long as we have a couple hundred bucks on hand??? and the likely irreperable damage it's doing to the environment all the while???? do you want the thoughts to stop???????

try noise solutions!

## setup

prerequesites:

1. You will need an ADBS-B RTL2832/R820T2 USB dongle with antenna plugged into your computer
2. Install dump1090 from here: https://github.com/antirez/dump1090
3. Have Python3 installed on your computer
4. Have Ableton Live installed (or another way of playing MIDI data sent from the `tones.py` script)

setup:

1. Clone this repo
2. Edit `./fetch_aicraft.sh` to add your latitude and longitude (you can find it by pinning your location on google maps and checking the URL for the numbers after the @ symbol):
   `dump1090 --lat <your latitude> --lon <your-longitude> --write-json json/`
3. Open up a terminal and run:

```
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. In one terminal window, run `./fetch_aicraft.sh`. This listens for radio signals from planes near you and writes their information to a JSON file.
4. Follow this guide to setup a virtual MIDI Bus to Ableton: https://help.ableton.com/hc/en-us/articles/209774225-How-to-setup-a-virtual-MIDI-bus
5. Open Ableton, set up a MIDI track and choose your virtual MIDI bus as the input, and choose a patch from the MIDI instruments
6. In a second terminal window `python3 tones.py`
7. You should hear the sounds created by the plane data playing through the patch you chose in Ableton

troubleshooting:

If `./fetch_aicraft.sh`, make sure `dump1090` is in your PATH, `export PATH=/usr/local/bin:$PATH` in my `.zshrc` (could be your `.bashrc`) worked for me.

If that doesn't work, run `fetch-aircraft.sh` from the directory you installed it from, and edit the script to:
`./dump1090 --lat <your latitude> --lon <your-longitude> --write-json json/`

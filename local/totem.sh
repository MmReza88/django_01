python -m http.server 80 --directory totem/ &
python rfid_totem.py &
DISPLAY=:0 firefox-esr --kiosk http://localhost:80/index.html
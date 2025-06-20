python -m http.server 8001 --directory totem/ &
python rfid_totem.py &
DISPLAY=:0 firefox-esr --kiosk http://localhost:80/index.html
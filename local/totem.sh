python -m http.server 8000 --directory totem/ &
python rfid_totem.py &
DISPLAY=:0 firefox-esr --kiosk http://localhost:8000/index.html
python -m http.server 8000 --directory controler/ &
python rfid_controler.py &
DISPLAY=:0 firefox-esr --kiosk http://localhost:8000/index.html
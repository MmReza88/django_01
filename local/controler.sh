python -m http.server 8000 --directory controler/ &
python rfid_controler.py &
rm -rf ~/.cache/mozilla/firefox
rm -rf ~/.mozilla/firefox/*.default-release/cache2
DISPLAY=:0 firefox-esr --kiosk http://localhost:8000/index.html

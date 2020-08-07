import eel

eel.init('web')

web_options = {
    # "mode": "chrome",
    "port": 8080,
    # "chromeFlags": ["-kiosk"]
}

eel.start('main.html', port=0, size=(600, 300))

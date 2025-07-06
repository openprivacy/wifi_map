# 📡 WiFi Access Points Map

## Install
Requirements: `uv` installed locally. See https://docs.astral.sh/uv/

```bash
git clone git@github.com:openprivacy/wifi_map.git
cd wifi_map
uv self update
uv venv
source .venv/bin/activate
uv pip install streamlit pandas folium streamlit-folium
```

## Run
```bash
streamlit run wifi_map_app.py
```

* Upload local CSV file
* Enjoy
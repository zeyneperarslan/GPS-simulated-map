# GPS Simulation Map Application

This project is a Python-based map application that simulates GPS movement using the `folium` library. Users can interactively visualize the movement of a point on a map based on coordinates provided through a text file. The application dynamically generates a route and displays it on a live map.

## 🌍 Features

- Visualizes location points on a map using Folium.
- Simulates GPS movement step-by-step.
- Automatically zooms and updates the map view as the simulated location changes.
- Easy-to-use interface via terminal.
- Supports `.txt` input with latitude and longitude data.

## 📁 Project Structure

```
project_folder/
│
├── coordinates.txt         # Text file with GPS coordinates (lat, lon per line)
├── map.py                 # Main Python script
```

## 🛠️ Requirements

- Python 3.x
- folium

Install dependencies via pip:

```bash
pip install folium
```

## ▶️ How to Use

- Enter latitude and longitude values into the GUI fields.

- Click Add Route Point to add the point to the route.

- After adding at least one point, select your preferred zoom and map type.

- Click Show and Simulate Map to open the interactive map window with the route and animated marker.

## 📸 Screenshots

![Map Simulation Screenshot](assets/screenshot.png) [Map Simulation Screenshot](assets/screenshot1.png)

## ✨ Future Improvements

- Add real-time coordinate input (e.g., from GPS sensor or API).
- Add GUI support.
- Export movement as a video or animation.

## 📄 License

This project is open-source and free to use under the MIT License.

---

Created with by Zeynep Erarslan
📫 Connect on LinkedIn: [https://linkedin.com/in/your-profile](https://www.linkedin.com/in/zeyneperarslan03/)

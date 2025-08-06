import tkinter as tk
from tkinter import messagebox
import folium
import webview
import tempfile
import json

route_points = []

map_types = {
    "OpenStreetMap": "OpenStreetMap",
    "Stamen Terrain": "Stamen Terrain",
    "Stamen Toner": "Stamen Toner",
    "CartoDB Positron": "CartoDB Positron",
    "CartoDB Dark Matter": "CartoDB Dark_Matter"
}

def add_point():
    try:
        lat = float(entry_lat.get())
        lng = float(entry_lng.get())
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError
        route_points.append((lat, lng))
        messagebox.showinfo("Success", f"Point added: ({lat}, {lng})")
        entry_lat.delete(0, tk.END)
        entry_lng.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid latitude (-90~90) and longitude (-180~180).")

def create_and_show_map():
    if not route_points:
        messagebox.showerror("Error", "You must add at least one point.")
        return

    zoom = zoom_scale.get()
    map_type = map_types[map_type_var.get()]

    map_obj = folium.Map(location=route_points[0], zoom_start=zoom, tiles=map_type)
    folium.PolyLine(route_points, color="blue", weight=5, opacity=0.7).add_to(map_obj)

    for idx, (lat, lng) in enumerate(route_points):
        if idx == 0:
            color = "red"        # Starting point in red
        elif idx == len(route_points) - 1:
            color = "blue"       # Ending point in blue
        else:
            color = "green"      # Intermediate points in green

        folium.Marker(
            [lat, lng],
            popup=f"Point {idx + 1}: {lat}, {lng}",
            tooltip=f"Route Point {idx + 1}",
            icon=folium.Icon(color=color)
        ).add_to(map_obj)

    path_js = json.dumps(route_points)
    sim_js = f"""
    <script>
    var map = window.map;
    var simMarker = L.marker({route_points[0]}).addTo(map);
    var path = {path_js};
    var i = 0;
    function moveMarker() {{
        simMarker.setLatLng(path[i]);
        i++;
        if (i < path.length) {{
            setTimeout(moveMarker, 1000);
        }}
    }}
    moveMarker();
    </script>
    """
    map_obj.get_root().html.add_child(folium.Element(sim_js))

    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        map_obj.save(f.name)
        html_file = f.name

    window.destroy()  # Close the Tkinter window
    webview.create_window("GPS Simulation Map", html_file)
    webview.start()

window = tk.Tk()
window.title("📡 GPS Simulation Map Application")
window.geometry("420x450")
window.configure(bg="#f9f9f9")

tk.Label(window, text="Latitude:", bg="#f9f9f9").pack(pady=5)
entry_lat = tk.Entry(window, width=30)
entry_lat.pack()

tk.Label(window, text="Longitude:", bg="#f9f9f9").pack(pady=5)
entry_lng = tk.Entry(window, width=30)
entry_lng.pack()

tk.Button(window, text="Add Route Point", command=add_point,
          bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

tk.Label(window, text="Zoom Level:", bg="#f9f9f9").pack(pady=5)
zoom_scale = tk.Scale(window, from_=1, to=20, orient="horizontal", length=200, bg="#f9f9f9")
zoom_scale.set(16)
zoom_scale.pack()

tk.Label(window, text="Map Type:", bg="#f9f9f9").pack(pady=5)
map_type_var = tk.StringVar()
map_type_var.set("OpenStreetMap")
option_menu = tk.OptionMenu(window, map_type_var, *map_types.keys())
option_menu.pack()

tk.Button(window, text="📍 Show and Simulate Map", command=create_and_show_map,
          bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=15)

window.mainloop()

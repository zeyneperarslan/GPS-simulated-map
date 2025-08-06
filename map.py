import tkinter as tk
from tkinter import messagebox
import folium
import webview
import tempfile
import json

rota_noktalari = []

harita_turleri = {
    "OpenStreetMap": "OpenStreetMap",
    "Stamen Terrain": "Stamen Terrain",
    "Stamen Toner": "Stamen Toner",
    "CartoDB Positron": "CartoDB Positron",
    "CartoDB Dark Matter": "CartoDB Dark_Matter"
}

def nokta_ekle():
    try:
        lat = float(entry_lat.get())
        lng = float(entry_lng.get())
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError
        rota_noktalari.append((lat, lng))
        messagebox.showinfo("Başarılı", f"Nokta eklendi: ({lat}, {lng})")
        entry_lat.delete(0, tk.END)
        entry_lng.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli enlem (-90~90) ve boylam (-180~180) giriniz.")

def harita_olustur_ve_goster():
    if not rota_noktalari:
        messagebox.showerror("Hata", "En az bir nokta eklemelisiniz.")
        return

    zoom = zoom_scale.get()
    harita_tipi = harita_turleri[harita_turu_var.get()]

    harita = folium.Map(location=rota_noktalari[0], zoom_start=zoom, tiles=harita_tipi)
    folium.PolyLine(rota_noktalari, color="blue", weight=5, opacity=0.7).add_to(harita)

    for idx, (lat, lng) in enumerate(rota_noktalari):
     if idx == 0:
        renk = "red"        # Başlangıç noktası kırmızı
     elif idx == len(rota_noktalari) - 1:
        renk = "blue"       # Varış noktası mavi (istersen "orange" veya "yellow" yapabilirsin)
     else:
        renk = "green"      # Ara noktalar yeşil

    folium.Marker(
        [lat, lng],
        popup=f"Nokta {idx + 1}: {lat}, {lng}",
        tooltip=f"Rota Noktası {idx + 1}",
        icon=folium.Icon(color=renk)
    ).add_to(harita)


    path_js = json.dumps(rota_noktalari)
    sim_js = f"""
    <script>
    var map = window.map;
    var simMarker = L.marker({rota_noktalari[0]}).addTo(map);
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
    harita.get_root().html.add_child(folium.Element(sim_js))

    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        harita.save(f.name)
        html_dosya = f.name

    # PyWebView burada main thread'de açılıyor ve Tkinter kapanıyor
    pencere.destroy()  # Tkinter penceresini kapat
    webview.create_window("GPS Simülasyonlu Harita", html_dosya)
    webview.start()

pencere = tk.Tk()
pencere.title("📡 GPS Simülasyonlu Harita Uygulaması")
pencere.geometry("420x450")
pencere.configure(bg="#f9f9f9")

tk.Label(pencere, text="Enlem (Latitude):", bg="#f9f9f9").pack(pady=5)
entry_lat = tk.Entry(pencere, width=30)
entry_lat.pack()

tk.Label(pencere, text="Boylam (Longitude):", bg="#f9f9f9").pack(pady=5)
entry_lng = tk.Entry(pencere, width=30)
entry_lng.pack()

tk.Button(pencere, text="Rota Noktası Ekle", command=nokta_ekle,
          bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

tk.Label(pencere, text="Yakınlaştırma (Zoom):", bg="#f9f9f9").pack(pady=5)
zoom_scale = tk.Scale(pencere, from_=1, to=20, orient="horizontal", length=200, bg="#f9f9f9")
zoom_scale.set(16)
zoom_scale.pack()

tk.Label(pencere, text="Harita Türü:", bg="#f9f9f9").pack(pady=5)
harita_turu_var = tk.StringVar()
harita_turu_var.set("OpenStreetMap")
option_menu = tk.OptionMenu(pencere, harita_turu_var, *harita_turleri.keys())
option_menu.pack()

tk.Button(pencere, text="📍 Haritayı Göster ve Simüle Et", command=harita_olustur_ve_goster,
          bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=15)

pencere.mainloop()

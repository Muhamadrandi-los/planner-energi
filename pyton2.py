import streamlit as st
import pandas as pd
import base64

# ================= FUNGSI BACA GAMBAR =================
def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ================= LOAD BACKGROUND =================
bg_image = get_base64_image("WhatsApp Image 2026-01-08 at 10.04.39.jpeg")

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Dashboard Listrik & PLTS",
    layout="wide",
    page_icon="⚡"
)

# ================= BACKGROUND CSS =================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.88);
    }}

    div.block-container {{
        background: rgba(255,255,255,0.88);
        padding: 2rem;
        border-radius: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ================= ISI APLIKASI =================
st.title("⚡ Dashboard PLTS")
st.success("Background WhatsApp Image berhasil dimuat 🔥")



# ================= HEADER =================
st.markdown("""
<div style="background:linear-gradient(90deg,#ff6fae,#ffc1dc);
padding:25px;border-radius:20px;
text-align:center;font-size:30px;
font-weight:800;color:white;">
⚡ Dashboard Konsumsi Listrik & PLTS  
<div style="font-size:15px;font-weight:400;">
Lengkap • Edukatif • Engineering Nyata
</div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🏷️ Identitas Lokasi")
    nama_lokasi = st.text_input("Nama lokasi", "Rumah / Masjid / Kantor")

    st.header("🔀 Mode Sistem PLTS")
    tipe_sistem = st.selectbox(
        "Pilih mode",
        ["On-Grid", "Off-Grid", "Hybrid"]
    )

    st.header("⚡ Sistem Listrik")
    tegangan = st.selectbox("Tegangan sistem (V)", [12, 24, 48])
    tarif = st.number_input("Tarif PLN (Rp/kWh)", value=1444)

    st.header("🔋 Baterai")
    baterai_ah = st.number_input("Kapasitas baterai (Ah)", 0, 50000, 200)
    dod = st.slider("Depth of Discharge (DoD)", 0.3, 0.8, 0.5)

    st.header("🌞 Matahari")
    sun_hours = st.slider("Jam matahari efektif (jam/hari)", 3.0, 6.5, 4.5)

    st.header("⚠️ Derating Sistem (Real)")
    loss_kabel = st.slider("Loss kabel (%)", 2, 10, 5) / 100
    eff_inverter = st.slider("Efisiensi inverter (%)", 85, 98, 92) / 100
    eff_scc = st.slider("Efisiensi SCC (%)", 90, 99, 95) / 100
    faktor_lingkungan = st.slider("Debu & suhu (%)", 90, 100, 95) / 100

    derating = (1 - loss_kabel) * eff_inverter * eff_scc * faktor_lingkungan
    st.markdown(f"**Derating total sistem:** `{derating:.2f}`")

    st.header("🧩 Preset Beban")
    preset_mode = st.selectbox(
        "Jenis bangunan",
        ["Manual", "Rumah", "Masjid", "Kantor"]
    )

# ================= PRESET =================
preset_data = {
    "Rumah": [
        {"nama": "Lampu", "watt": 10, "jam": 8},
        {"nama": "TV", "watt": 100, "jam": 5},
        {"nama": "Kulkas", "watt": 150, "jam": 24},
    ],
    "Masjid": [
        {"nama": "Lampu", "watt": 10, "jam": 10},
        {"nama": "Speaker", "watt": 200, "jam": 5},
        {"nama": "Kipas", "watt": 60, "jam": 6},
    ],
    "Kantor": [
        {"nama": "Lampu", "watt": 15, "jam": 9},
        {"nama": "AC", "watt": 800, "jam": 8},
        {"nama": "Komputer", "watt": 200, "jam": 8},
    ],
}

# ================= SESSION =================
if "alat" not in st.session_state:
    st.session_state.alat = []

if preset_mode != "Manual" and st.session_state.alat == []:
    st.session_state.alat = preset_data[preset_mode].copy()

# ================= INPUT ALAT =================
st.header("📋 Daftar Alat Listrik")

for i, alat in enumerate(st.session_state.alat):
    c1, c2, c3, c4 = st.columns([3,2,2,1])
    alat["nama"] = c1.text_input("Nama", alat["nama"], key=f"n{i}")
    alat["watt"] = c2.number_input("Daya (W)", 1, 30000, alat["watt"], key=f"w{i}")
    alat["jam"] = c3.number_input("Jam/hari", 0.1, 24.0, float(alat["jam"]), key=f"j{i}")
    if c4.button("❌", key=f"d{i}"):
        st.session_state.alat.pop(i)
        st.rerun()

st.button("➕ Tambah Alat", on_click=lambda: st.session_state.alat.append(
    {"nama": "Alat Baru", "watt": 100, "jam": 1}
))

# ================= PERHITUNGAN ENERGI =================
energi_harian_wh = sum(a["watt"] * a["jam"] for a in st.session_state.alat)
energi_harian_kwh = energi_harian_wh / 1000
energi_bulanan_kwh = energi_harian_kwh * 30
energi_tahunan_kwh = energi_bulanan_kwh * 12

# ================= BIAYA PLN =================
biaya_harian = energi_harian_kwh * tarif
biaya_bulanan = energi_bulanan_kwh * tarif
biaya_tahunan = energi_tahunan_kwh * tarif

# ================= OUTPUT ENERGI =================
st.markdown("---")
st.header("⚡ Pemakaian Listrik")

c1, c2, c3 = st.columns(3)
c1.metric("Per Hari", f"{energi_harian_kwh:.2f} kWh")
c2.metric("Per Bulan", f"{energi_bulanan_kwh:.1f} kWh")
c3.metric("Per Tahun", f"{energi_tahunan_kwh:.0f} kWh")

# ================= OUTPUT BIAYA =================
st.markdown("---")
st.header("💰 Biaya Listrik PLN")

b1, b2, b3 = st.columns(3)
b1.metric("Per Hari", f"Rp {biaya_harian:,.0f}")
b2.metric("Per Bulan", f"Rp {biaya_bulanan:,.0f}")
b3.metric("Per Tahun", f"Rp {biaya_tahunan:,.0f}")

# ================= PANEL SURYA =================
st.markdown("---")
st.header("🌞 Panel Surya")

kebutuhan_wp = energi_harian_wh / (sun_hours * derating)

daya_panel = st.number_input("Daya 1 panel (Wp)", 100, 1000, 550)
jumlah_panel = st.number_input("Jumlah panel", 1, 200, 4)

panel_wp = daya_panel * jumlah_panel
energi_panel_harian_wh = panel_wp * sun_hours * derating

st.metric("Kebutuhan Panel", f"{kebutuhan_wp:.0f} Wp")
st.metric("Panel Terpasang", f"{panel_wp} Wp")
st.metric("Energi Panel / Hari", f"{energi_panel_harian_wh:.0f} Wh")

# ================= SIMULASI PLN MATI =================
st.markdown("---")
st.header("🔌 Simulasi PLN Mati")

total_daya = sum(a["watt"] for a in st.session_state.alat)
energi_baterai = baterai_ah * tegangan * dod
backup_jam = energi_baterai / total_daya if total_daya > 0 else 0

if tipe_sistem in ["Off-Grid", "Hybrid"]:
    st.success(f"Baterai bertahan ± **{backup_jam:.1f} jam**")
else:
    st.warning("Mode ON-GRID tidak memiliki backup")

# ================= ESTIMASI BIAYA PLTS =================
st.markdown("---")
st.header("🔧 Estimasi Biaya Sistem PLTS")

harga_panel_wp = st.number_input("Harga panel (Rp/Wp)", value=5500)
harga_baterai_ah = st.number_input("Harga baterai (Rp/Ah)", value=2000)
harga_inverter = st.number_input("Harga inverter (Rp)", value=5_000_000)
harga_scc = st.number_input("Harga SCC (Rp)", value=2_000_000)

biaya_panel = panel_wp * harga_panel_wp
biaya_baterai = baterai_ah * harga_baterai_ah
total_plts = biaya_panel + biaya_baterai + harga_inverter + harga_scc

st.metric("Total Estimasi Biaya PLTS", f"Rp {total_plts:,.0f}")

# ================= TABEL =================
st.markdown("---")
st.header("📊 Ringkasan Alat")

df = pd.DataFrame(st.session_state.alat)
if not df.empty:
    df["Energi (Wh/hari)"] = df["watt"] * df["jam"]
    st.dataframe(df, use_container_width=True)

# ================= KESIMPULAN =================
st.markdown("---")
st.success(f"""
### 📌 Kesimpulan

- Lokasi: **{nama_lokasi}**
- Mode sistem: **{tipe_sistem}**
- Konsumsi: **{energi_bulanan_kwh:.1f} kWh/bulan**
- Biaya PLN: **Rp {biaya_bulanan:,.0f}/bulan**
- Panel terpasang: **{panel_wp} Wp**
- Backup baterai: **{backup_jam:.1f} jam**
- Estimasi biaya PLTS: **Rp {total_plts:,.0f}**
""")

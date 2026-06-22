import streamlit as st
import pandas as pd
import math

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="RPN Calculator Fix",
    page_icon="🧮",
    layout="wide"
)

# =========================
# CSS INTERNAL (PERBAIKAN MOBILE & LAPTOP)
# =========================
st.markdown("""
<style>
/* Background Utama Hitam */
.stApp {
    background-color: #06060c;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Judul RPN */
.calc-title {
    color: #ff2d8d;
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    text-shadow: 0 0 20px #ff2d8d;
    margin-bottom: 30px;
}

/* Sub-judul Text Pink */
.sub-pink {
    color: #ff2d8d;
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

/* Box Display Layar */
.display-box {
    background: #0d0d19;
    border: 2px solid #ff2d8d;
    border-radius: 15px;
    padding: 20px;
    text-align: right;
    min-height: 100px;
    box-shadow: 0 0 15px rgba(255, 45, 141, 0.2);
}

.display-main {
    font-size: 48px;
    font-weight: bold;
    color: #ffffff;
    font-family: monospace;
}

.display-sub {
    font-size: 20px;
    color: #ff2d8d;
    font-family: monospace;
    opacity: 0.8;
}

/* General button styling */
.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    transition: all 0.1s ease;
}

/* Angka */
.stButton > button[key*="num-"] {
    background-color: #16162a;
    color: white;
    border: 1px solid #ff2d8d22;
}
.stButton > button[key*="num-"]:hover {
    background-color: #ff2d8d;
    color: black;
    box-shadow: 0 0 15px #ff2d8d;
}

/* Operator */
.stButton > button[key*="op-"] {
    background-color: #ff2d8d;
    color: black;
}
.stButton > button[key*="op-"]:hover {
    background-color: #ff66b2;
    box-shadow: 0 0 20px #ff66b2;
}

/* Tombol Aksi */
.stButton > button[key*="act-"] {
    background-color: #333344;
    color: white;
}
.stButton > button[key*="act-"]:hover {
    background-color: #ff2d8d;
}

/* Tombol ENTER Tinggi di Desktop */
.stButton > button[key="act-enter"] {
    background-color: #ff2d8d;
    color: black;
    height: 196px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b0b15;
    border-right: 2px solid #ff2d8d;
}

/* ===================================================
   TRICK RESPONSIVE KHUSUS UNTUK HP (ANTI BERANTAKAN)
   =================================================== */
@media (max-width: 768px) {
    /* Paksa kolom bagian dalam (keypad) agar TETAP berjejer ke samping di HP */
    div[data-testid="column"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
        width: 100% !important;
    }

    /* Pastikan flexbox anak membagi ruang secara merata */
    div[data-testid="column"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
    }

    /* Sesuaikan ukuran tombol agar fit di layar HP */
    .stButton > button {
        height: 46px !important;
        font-size: 14px !important;
        border-radius: 8px !important;
    }

    /* Sesuaikan tinggi tombol ENTER khusus di HP agar pas dengan tinggi 3 baris angka */
    .stButton > button[key="act-enter"] {
        height: 150px !important;
    }
    
    /* Perkecil ukuran font judul di HP */
    .calc-title {
        font-size: 28px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# INITIALIZE MEMORI (SESSION STATE)
# =========================
if "stack" not in st.session_state:
    st.session_state.stack = []

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# FUNGSI INTERAKSI LOGIKA
# =========================
def input_angka(angka):
    st.session_state.current_input += str(angka)

def input_desimal():
    if "." not in st.session_state.current_input:
        if st.session_state.current_input == "":
            st.session_state.current_input = "0."
        else:
            st.session_state.current_input += "."

def aksi_enter():
    if st.session_state.current_input != "":
        try:
            val = float(st.session_state.current_input)
            st.session_state.stack.append(val)
            st.session_state.current_input = ""
        except ValueError:
            pass

def aksi_c():
    if st.session_state.current_input != "":
        st.session_state.current_input = ""
    elif len(st.session_state.stack) > 0:
        st.session_state.stack.pop()

def aksi_ac():
    st.session_state.stack = []
    st.session_state.current_input = ""

# Callback pengganti st.rerun() untuk menghapus riwayat aman
def aksi_hapus_riwayat():
    st.session_state.history = []

def eksekusi_matematika(operator):
    if st.session_state.current_input != "":
        aksi_enter()

    unary_ops = ["sqrt", "sin", "cos", "tan", "log", "+/-"]
    req_count = 1 if operator in unary_ops else 2

    if len(st.session_state.stack) >= req_count:
        try:
            if operator in unary_ops:
                a = st.session_state.stack.pop()
                if operator == "sqrt":
                    if a < 0: raise ValueError("Akar Negatif")
                    hasil = math.sqrt(a)
                    ekspresi = f"sqrt({a})"
                elif operator == "sin":
                    hasil = math.sin(math.radians(a))
                    ekspresi = f"sin({a})"
                elif operator == "cos":
                    hasil = math.cos(math.radians(a))
                    ekspresi = f"cos({a})"
                elif operator == "tan":
                    hasil = math.tan(math.radians(a))
                    ekspresi = f"tan({a})"
                elif operator == "log":
                    if a <= 0: raise ValueError("Log <= 0")
                    hasil = math.log10(a)
                    ekspresi = f"log10({a})"
                elif operator == "+/-":
                    hasil = -a
                    ekspresi = f"neg({a})"
            else:
                b = st.session_state.stack.pop()
                a = st.session_state.stack.pop()
                
                if operator == "+":
                    hasil = a + b
                    ekspresi = f"{a} + {b}"
                elif operator == "-":
                    hasil = a - b
                    ekspresi = f"{a} - {b}"
                elif operator == "*":
                    hasil = a * b
                    ekspresi = f"{a} * {b}"
                elif operator == "/":
                    if b == 0: raise ValueError("Bagi Nol!")
                    hasil = a / b
                    ekspresi = f"{a} / {b}"
                elif operator == "^":
                    hasil = a ** b
                    ekspresi = f"{a} ^ {b}"

            hasil = round(hasil, 6)
            st.session_state.stack.append(hasil)
            
            st.session_state.history.append({
                "Ekspresi": ekspresi,
                "Hasil Perhitungan": hasil
            })
        except Exception as e:
            st.error(f"Kesalahan Matematika: {str(e)}")
    else:
        st.warning(f"Gagal! Perlu minimal {req_count} angka di dalam Stack.")

# =========================
# NAVIGASI SIDEBAR MENU
# =========================
st.sidebar.markdown("<h2 style='color:#ff2d8d; text-align:center;'>MENU</h2>", unsafe_allow_html=True)
pilihan_menu = st.sidebar.radio("Pindah Halaman:", ["🧮 Kalkulator RPN", "📜 Riwayat Perhitungan", "ℹ️ Tentang Aplikasi"], label_visibility="collapsed")

# -------------------------
# HALAMAN 1: KALKULATOR
# -------------------------
if pilihan_menu == "🧮 Kalkulator RPN":
    st.markdown("<div class='calc-title'>RPN CALCULATOR</div>", unsafe_allow_html=True)

    # Membagi layout seimbang Kiri (Layar Stack aktif) dan Kanan (Keypad kalkulator)
    kol_kiri, kol_kanan = st.columns([1, 1.2], gap="large")

    with kol_kiri:
        st.markdown("<div class='sub-pink'>STACK ACTIVE (MEMORI DATA)</div>", unsafe_allow_html=True)
        
        s0 = st.session_state.stack[-1] if len(st.session_state.stack) >= 1 else "0"
        s1 = st.session_state.stack[-2] if len(st.session_state.stack) >= 2 else "0"
        s2 = st.session_state.stack[-3] if len(st.session_state.stack) >= 3 else "0"

        st.markdown(f"""
        <div class='display-box' style='margin-bottom:20px;'>
            <div class='display-sub'>[Stack Level 3] : {s2}</div>
            <div class='display-sub'>[Stack Level 2] : {s1}</div>
            <div class='display-sub' style='color:#ff2d8d; font-weight:bold;'>[Stack Level 1] : {s0}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sub-pink'>HASIL AKHIR / INPUT SEKARANG</div>", unsafe_allow_html=True)
        layar_bawah = st.session_state.current_input if st.session_state.current_input != "" else str(s0)
        st.markdown(f"""
        <div class='display-box'>
            <div class='display-main'>{layar_bawah}</div>
        </div>
        """, unsafe_allow_html=True)

    with kol_kanan:
        st.markdown("<div class='sub-pink'>INTERFACE KEYPAD</div>", unsafe_allow_html=True)
        
        # Grid Baris 1 - Fungsi Sains
        r1 = st.columns(5)
        r1[0].button("sqrt", key="op-sqrt", on_click=eksekusi_matematika, args=("sqrt",))
        r1[1].button("sin",  key="op-sin",  on_click=eksekusi_matematika, args=("sin",))
        r1[2].button("cos",  key="op-cos",  on_click=eksekusi_matematika, args=("cos",))
        r1[3].button("tan",  key="op-tan",  on_click=eksekusi_matematika, args=("tan",))
        r1[4].button("log",  key="op-log",  on_click=eksekusi_matematika, args=("log",))

        # Grid Baris 2 - Operator Utama & Pembersih
        r2 = st.columns(5)
        r2[0].button("+/-",  key="op-neg",  on_click=eksekusi_matematika, args=("+/-",))
        r2[1].button("^",    key="op-pow",  on_click=eksekusi_matematika, args=("^",))
        r2[2].button("C",    key="act-c",   on_click=aksi_c)
        r2[3].button("/",    key="op-div",  on_click=eksekusi_matematika, args=("/",))
        r2[4].button("x",    key="op-mul",  on_click=eksekusi_matematika, args=("*",))

        # Grid Kombinasi Angka dan ENTER samping kanan
        sub_kiri, sub_kanan = st.columns([4, 1])

        with sub_kiri:
            # Baris Angka 7, 8, 9, Minus
            k1 = st.columns(4)
            k1[0].button("7", key="num-7", on_click=input_angka, args=(7,))
            k1[1].button("8", key="num-8", on_click=input_angka, args=(8,))
            k1[2].button("9", key="num-9", on_click=input_angka, args=(9,))
            k1[3].button("-", key="op-sub", on_click=eksekusi_matematika, args=("-",))

            # Baris Angka 4, 5, 6, Plus
            k2 = st.columns(4)
            k2[0].button("4", key="num-4", on_click=input_angka, args=(4,))
            k2[1].button("5", key="num-5", on_click=input_angka, args=(5,))
            k2[2].button("6", key="num-6", on_click=input_angka, args=(6,))
            k2[3].button("+", key="op-add", on_click=eksekusi_matematika, args=("+",))

            # Baris Angka 1, 2, 3, Desimal
            k3 = st.columns(4)
            k3[0].button("1", key="num-1", on_click=input_angka, args=(1,))
            k3[1].button("2", key="num-2", on_click=input_angka, args=(2,))
            k3[2].button("3", key="num-3", on_click=input_angka, args=(3,))
            k3[3].button(".", key="num-dot", on_click=input_desimal)

        with sub_kanan:
            # Tombol Enter Panjang Vertikal (ENT agar tidak memotong di HP)
            st.button("ENT", key="act-enter", on_click=aksi_enter)

        # Baris Paling Bawah - Angka 0 Lebar dan Reset AC
        r4 = st.columns([3, 1, 1])
        r4[0].button("0", key="num-0", on_click=input_angka, args=(0,))
        r4[1].button("AC", key="act-ac", on_click=aksi_ac)
        r4[2].markdown("<div style='padding-top:15px; color:#444; font-size:12px; font-weight:bold; text-align:center;'>LIFO</div>", unsafe_allow_html=True)

# -------------------------
# HALAMAN 2: RIWAYAT (FIXED CLEAN)
# -------------------------
elif pilihan_menu == "📜 Riwayat Perhitungan":
    st.markdown("<div class='calc-title'>RIWAYAT PERHITUNGAN</div>", unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        df_logs = pd.DataFrame(st.session_state.history)
        st.dataframe(df_logs, use_container_width=True)
        
        # FITUR ST.RERUN KINI DIHAPUS TOTAL DAN DIGANTI DENGAN CALLBACK (on_click) AGAR SEHAT DAN AMAN
        st.button("Hapus Semua Riwayat", key="act-del-hist", on_click=aksi_hapus_riwayat)
    else:
        st.info("Belum ada riwayat operasi matematika yang tersimpan.")

# -------------------------
# HALAMAN 3: TENTANG APLIKASI
# -------------------------
elif pilihan_menu == "ℹ️ Tentang Aplikasi":
    st.markdown("<div class='calc-title'>INFORMASI DEVELOPER</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0d0d19; border:2px solid #ff2d8d; padding:25px; border-radius:15px; font-size:16px;'>
        <p><b>Nama :</b> Naufal Atha</p>
        <p><b>NIM :</b> 1225170082</p>
        <p><b>Project :</b> Kalkulator Sistem Reverse Polish Notation (RPN)</p>
        <hr style='border-color:#ff2d8d;'>
        <p style='color:#ff2d8d; font-weight:bold;'>💡 CARA PENJUMLAHAN RPN YANG BENAR (8 + 9 = 17):</p>
        <ol>
            <li>Tekan tombol angka <b>8</b>, lalu tekan tombol <b>ENTER</b>.</li>
            <li>Tekan tombol angka <b>9</b>, lalu tekan tombol <b>ENTER</b>.</li>
            <li>Tekan tombol operator tambah <b>+</b>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

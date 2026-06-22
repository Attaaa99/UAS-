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
# INITIALIZE MEMORI (SESSION STATE)
# =========================
if "stack" not in st.session_state:
    st.session_state.stack = []

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# CSS INTERNAL UTAMA
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #06060c;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.calc-title {
    color: #ff2d8d;
    text-align: center;
    font-size: clamp(24px, 5vw, 45px);
    font-weight: bold;
    text-shadow: 0 0 20px #ff2d8d;
    margin-bottom: 20px;
}
.sub-pink {
    color: #ff2d8d;
    font-size: clamp(13px, 3vw, 16px);
    font-weight: bold;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.display-box {
    background: #0d0d19;
    border: 2px solid #ff2d8d;
    border-radius: 15px;
    padding: 15px;
    text-align: right;
    min-height: 70px;
    box-shadow: 0 0 15px rgba(255, 45, 141, 0.2);
}
.display-main {
    font-size: clamp(28px, 6vw, 44px);
    font-weight: bold;
    color: #ffffff;
    font-family: monospace;
}
.display-sub {
    font-size: clamp(13px, 2.5vw, 18px);
    color: #ff2d8d;
    font-family: monospace;
    opacity: 0.8;
}
[data-testid="stSidebar"] {
    background-color: #0b0b15;
    border-right: 2px solid #ff2d8d;
}
/* Menyembunyikan tombol trigger python dari layar */
.element-container:has(.hidden-btn) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNGSI INTERAKSI LOGIKA
# =========================
def input_angka(angka):
    st.session_state.current_input += str(angka)

def input_desimal():
    if "." not in st.session_state.current_input:
        st.session_state.current_input = "0." if st.session_state.current_input == "" else st.session_state.current_input + "."

def aksi_enter():
    if st.session_state.current_input != "":
        try:
            st.session_state.stack.append(float(st.session_state.current_input))
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
                if operator == "+": hasil = a + b
                elif operator == "-": hasil = a - b
                elif operator == "*": hasil = a * b
                elif operator == "/":
                    if b == 0: raise ValueError("Bagi Nol!")
                    hasil = a / b
                elif operator == "^": hasil = a ** b
                ekspresi = f"{a} {operator} {b}"

            hasil = round(hasil, 6)
            st.session_state.stack.append(hasil)
            st.session_state.history.append({"Ekspresi": ekspresi, "Hasil Perhitungan": hasil})
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

    # Layout Utama Layar vs Keypad (Akan turun vertikal secara rapi HANYA pada layar utama)
    kol_kiri, kol_kanan = st.columns([1, 1.1], gap="medium")

    with kol_kiri:
        st.markdown("<div class='sub-pink'>STACK ACTIVE (MEMORI DATA)</div>", unsafe_allow_html=True)
        s0 = st.session_state.stack[-1] if len(st.session_state.stack) >= 1 else "0"
        s1 = st.session_state.stack[-2] if len(st.session_state.stack) >= 2 else "0"
        s2 = st.session_state.stack[-3] if len(st.session_state.stack) >= 3 else "0"

        st.markdown(f"""
        <div class='display-box' style='margin-bottom:15px;'>
            <div class='display-sub'>[Stack Level 3] : {s2}</div>
            <div class='display-sub'>[Stack Level 2] : {s1}</div>
            <div class='display-sub' style='color:#ff2d8d; font-weight:bold;'>[Stack Level 1] : {s0}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sub-pink'>HASIL AKHIR / INPUT SEKARANG</div>", unsafe_allow_html=True)
        layar_bawah = st.session_state.current_input if st.session_state.current_input != "" else str(s0)
        st.markdown(f"""
        <div class='display-box' style='margin-bottom:20px;'>
            <div class='display-main'>{layar_bawah}</div>
        </div>
        """, unsafe_allow_html=True)

    with kol_kanan:
        st.markdown("<div class='sub-pink'>INTERFACE KEYPAD</div>", unsafe_allow_html=True)
        
        # --- TOMBOL TERSEMBUNYI UNTUK DIKONTROL OLEH HTML GRID ---
        # Baris Sains & Operator
        for op in ["sqrt", "sin", "cos", "tan", "log", "+/-", "^", "/", "*", "-", "+"]:
            if st.button(op, key=f"py-op-{op}", help="hidden"): eksekusi_matematika(op)
        for num in range(10):
            if st.button(str(num), key=f"py-num-{num}"): input_angka(num)
        if st.button(".", key="py-num-dot"): input_desimal()
        if st.button("C", key="py-act-c"): aksi_c()
        if st.button("AC", key="py-act-ac"): aksi_ac()
        if st.button("ENTER", key="py-act-enter"): aksi_enter()

        # --- HTML & CSS GRID MURNI (Mencegah tombol hancur/ke bawah di HP) ---
        html_keypad = """
        <style>
        .grid-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            background-color: #06060c;
            padding: 2px;
            font-family: 'Segoe UI', sans-serif;
        }
        button {
            width: 100%;
            height: 52px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: all 0.1s ease;
        }
        .btn-num { background-color: #16162a; color: white; border: 1px solid #ff2d8d22; }
        .btn-num:hover { background-color: #ff2d8d; color: black; }
        .btn-op { background-color: #ff2d8d; color: black; }
        .btn-op:hover { background-color: #ff66b2; }
        .btn-act { background-color: #333344; color: white; }
        .btn-act:hover { background-color: #ff2d8d; }
        
        /* Spesifik posisi grid tombol enter span vertikal */
        .btn-enter {
            grid-column: 5;
            grid-row: 3 / span 3;
            height: 100%;
            background-color: #ff2d8d;
            color: black;
        }
        .btn-zero { grid-column: span 3; }
        </style>

        <div class="grid-container">
            <button class="btn-op" onclick="clickParent('py-op-sqrt')">sqrt</button>
            <button class="btn-op" onclick="clickParent('py-op-sin')">sin</button>
            <button class="btn-op" onclick="clickParent('py-op-cos')">cos</button>
            <button class="btn-op" onclick="clickParent('py-op-tan')">tan</button>
            <button class="btn-op" onclick="clickParent('py-op-log')">log</button>
            
            <button class="btn-op" onclick="clickParent('py-op-+/-')">+/-</button>
            <button class="btn-op" onclick="clickParent('py-op-^')">^</button>
            <button class="btn-act" onclick="clickParent('py-act-c')">C</button>
            <button class="btn-op" onclick="clickParent('py-op-/')">/</button>
            <button class="btn-op" onclick="clickParent('py-op-*')">x</button>
            
            <button class="btn-num" onclick="clickParent('py-num-7')">7</button>
            <button class="btn-num" onclick="clickParent('py-num-8')">8</button>
            <button class="btn-num" onclick="clickParent('py-num-9')">9</button>
            <button class="btn-op" onclick="clickParent('py-op--')">-</button>
            <button class="btn-op btn-enter" onclick="clickParent('py-act-enter')">ENT</button>
            
            <button class="btn-num" onclick="clickParent('py-num-4')">4</button>
            <button class="btn-num" onclick="clickParent('py-num-5')">5</button>
            <button class="btn-num" onclick="clickParent('py-num-6')">6</button>
            <button class="btn-op" onclick="clickParent('py-op-+')">+</button>
            
            <button class="btn-num" onclick="clickParent('py-num-1')">1</button>
            <button class="btn-num" onclick="clickParent('py-num-2')">2</button>
            <button class="btn-num" onclick="clickParent('py-num-3')">3</button>
            <button class="btn-num" onclick="clickParent('py-num-dot')">.</button>
            
            <button class="btn-num btn-zero" onclick="clickParent('py-num-0')">0</button>
            <button class="btn-act" onclick="clickParent('py-act-ac')">AC</button>
            <div style="color:#555; font-size:10px; font-weight:bold; display:flex; align-items:center; justify-content:center;">LIFO</div>
        </div>

        <script>
        function clickParent(key) {
            // Mengirim trigger click ke tombol python asli di luar iframe
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent === key || buttons[i].innerText.includes(key) || buttons[i].getAttribute('data-testid') === 'stButton' && buttons[i].innerHTML.includes(key)) {
                    buttons[i].click();
                    break;
                }
                // Metode fallback akurat menggunakan pencarian class unik bentukan streamlit key
                var targetBtn = window.parent.document.querySelector('button[id*="'+key+'"]');
                if(targetBtn){
                    targetBtn.click();
                    break;
                }
            }
        }
        </script>
        """
        # Render HTML Keypad yang super rapi dan anti pecah
        st.components.v1.html(html_keypad, height=340, scrolling=False)

# -------------------------
# HALAMAN 2: RIWAYAT (CLEAN)
# -------------------------
elif pilihan_menu == "📜 Riwayat Perhitungan":
    st.markdown("<div class='calc-title'>RIWAYAT PERHITUNGAN</div>", unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        df_logs = pd.DataFrame(st.session_state.history)
        st.dataframe(df_logs, use_container_width=True)
        st.button("Hapus Semua Riwayat", key="act-del-hist", on_click=aksi_hapus_riwayat)
    else:
        st.info("Belum ada riwayat operasi matematika yang tersimpan.")

# -------------------------
# HALAMAN 3: TENTANG APLIKASI
# -------------------------
elif pilihan_menu == "ℹ️ Tentang Aplikasi":
    st.markdown("<div class='calc-title'>INFORMASI DEVELOPER</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0d0d19; border:2px solid #ff2d8d; padding:20px; border-radius:15px; font-size:15px; line-height:1.6;'>
        <p><b>Nama :</b> Naufal Atha</p>
        <p><b>NIM :</b> 1225170082</p>
        <p><b>Project :</b> Kalkulator Sistem Reverse Polish Notation (RPN)</p>
        <hr style='border-color:#ff2d8d;'>
        <p style='color:#ff2d8d; font-weight:bold;'>💡 CARA PENJUMLAHAN RPN YANG BENAR (8 + 9 = 17):</p>
        <ol style='padding-left:20px;'>
            <li>Tekan tombol angka <b>8</b>, lalu tekan tombol <b>ENTER</b>.</li>
            <li>Tekan tombol angka <b>9</b>, lalu tekan tombol <b>ENTER</b>.</li>
            <li>Tekan tombol operator tambah <b>+</b>.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
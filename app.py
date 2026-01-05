import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def run():
    st.title("🎧 Case 2: Digital Interference")

    # Case 1 Check
    if 'inventory_audio_file' not in st.session_state:
        st.error("⛔ ACCESS DENIED: Complete Case 1 first.")
        return 
    st.success("✅ File Loaded.")

    if 'math_mode_2' not in st.session_state: st.session_state['math_mode_2'] = False
    
    if not st.session_state['math_mode_2']:
        st.markdown("**Mission:** Find the hidden frequency (Coordinate) within the noisy sound.")
    else:
        st.markdown(r"### 📐 FFT: Fourier Transform $$ X_k = \sum_{n=0}^{N-1} x_n e^{-i 2\pi k n / N} $$")

    # "Noise Level" is technically more accurate than "Filter" given how the code works (adding noise)
    noise_level = st.slider("Noise Level", 0.0, 5.0, 4.0)
    
    N = 600; T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N, endpoint=False)
    # 42.0 Hz is the target frequency
    y = np.sin(42.0 * 2.0 * np.pi * x) + np.random.normal(0, noise_level, N)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Time (Ear)")
        fig, ax = plt.subplots(); ax.plot(x, y); st.pyplot(fig)
    with col2:
        st.subheader("Frequency (Math)")
        yf = fft(y); xf = fftfreq(N, T)[:N//2]
        amp = 2.0/N * np.abs(yf[0:N//2])
        fig, ax = plt.subplots(); ax.plot(xf, amp, 'r'); st.pyplot(fig)
        
        peak = xf[np.argmax(amp)]
        st.metric("Detected", f"{peak:.2f} Hz")
        
        if 40 < peak < 44:
            st.success("CODE CRACKED! Coordinate: 0.0")
            st.session_state['inventory_coordinates'] = 0.0

    st.divider()
    if st.button("🔴 Red Pill"):
        st.session_state['math_mode_2'] = not st.session_state['math_mode_2']
        if hasattr(st, "rerun"): st.rerun() 
        else: st.experimental_rerun()

if __name__ == "__main__":
    run()
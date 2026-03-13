import streamlit as st
import requests

TOKEN    = "bd8b22e3e5ebbaa05ea0055aec4e16c357c29486"
VOICE    = "AntoineFromAfar22k_NV"
BASE_URL = "https://www.acapela-cloud.com/api/command/"
AUDIO_PREFIX = r'\audio=mix="CrowdLoud.raw";volume=10;repeat=on\ '

def generate_audio(texte, avec_foule, samplerate):
    text_final = (AUDIO_PREFIX + texte) if avec_foule else texte
    params = {
        "voice": VOICE, "text": text_final,
        "output": "stream", "type": "mp3",
        "samplerate": samplerate, "token": TOKEN,
    }
    r = requests.get(BASE_URL, params=params,
                     headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code == 200 and "audio" in r.headers.get("Content-Type", ""):
        return r.content
    return None

# --- UI ---
st.set_page_config(page_title="Antoine From Afar TTS", page_icon="🎙")
st.title("🎙 Antoine From Afar TTS")
st.caption("Acapela Cloud · AntoineFromAfar22k_NV")

texte = st.text_area("Phrases à générer (une par ligne) :",
                     value="Bonjour, c'est Antoine depuis très loin.",
                     height=150)

col1, col2 = st.columns(2)
avec_foule = col1.toggle("🎶 Fond sonore foule")
samplerate = col2.selectbox("Sample rate", [22050, 11025, 8000])

if st.button("▶ Générer", type="primary"):
    lignes = [l.strip() for l in texte.splitlines() if l.strip()]
    if not lignes:
        st.warning("Entre au moins une phrase.")
    else:
        for i, ligne in enumerate(lignes):
            with st.spinner(f"Génération {i+1}/{len(lignes)}…"):
                data = generate_audio(ligne, avec_foule, samplerate)
            if data:
                st.audio(data, format="audio/mp3")
                st.download_button(
                    label=f"💾 Télécharger antoine_{i+1:02d}.mp3",
                    data=data,
                    file_name=f"antoine_{i+1:02d}.mp3",
                    mime="audio/mp3"
                )
            else:
                st.error(f"Erreur sur : {ligne[:50]}")

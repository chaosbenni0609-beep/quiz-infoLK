import streamlit as st
from questions import questions

st.set_page_config(
    page_title="Quiz App",
    page_icon="🧠",
    layout="centered"
)

def reset():
    """Setzt den gesamten Quiz-Zustand zurück."""
    for key in ["phase", "thema", "frage_idx", "punkte", "antwort_gegeben", "letzte_korrekt"]:
        if key in st.session_state:
            del st.session_state[key]

def init():
    """Initialisiert fehlende Session-State-Werte."""
    defaults = {
        "phase": "start",        # start | quiz | ergebnis
        "thema": None,
        "frage_idx": 0,
        "punkte": 0,
        "antwort_gegeben": False,
        "letzte_korrekt": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

st.markdown("""
<style>
    .quiz-header   { font-size: large; font-weight: 700; margin-bottom: 0.2rem; }
    .quiz-sub      { color: #888; margin-bottom: 1.5rem; }
    .feedback-ok   { background:#d4edda; color:#155724; padding:0.8rem 1rem;
                     border-radius:8px; font-weight:600; margin:0.5rem 0; }
    .feedback-fail { background:#f8d7da; color:#721c24; padding:0.8rem 1rem;
                     border-radius:8px; font-weight:600; margin:0.5rem 0; }
    .score-box     { background:#19266b; padding:1.5rem; border-radius:12px;
                     text-align:center; font-size:1.3rem; margin:1rem 0; }
    div[data-testid="stButton"] button { width: 100%; }
</style>
""", unsafe_allow_html=True)


if st.session_state.phase == "start":
    st.markdown('<p class="quiz-header">🧠 Quiz App</p>', unsafe_allow_html=True)
    st.markdown('<p class="quiz-sub">Teste dein Wissen – wähle ein Thema und leg los!</p>',
                unsafe_allow_html=True)

    st.subheader("Thema auswählen")
    themen = list(questions.keys())

    cols = st.columns(len(themen))
    for i, thema in enumerate(themen):
        anzahl = len(questions[thema])
        if cols[i].button(f"**{thema}**\n\n{anzahl} Fragen", key=f"btn_{thema}"):
            st.session_state.thema = thema
            st.session_state.phase = "quiz"
            st.rerun()

    st.divider()
    st.caption("Viel Erfolg! 🚀  –  Erstellt von Felix, Benjamin & Benno")

elif st.session_state.phase == "quiz":
    thema     = st.session_state.thema
    fragen    = questions[thema]
    idx       = st.session_state.frage_idx
    gesamt    = len(fragen)
    aktuelle  = fragen[idx]


    st.markdown(f"**{thema}** – Frage {idx + 1} von {gesamt}")
    st.progress((idx + 1) / gesamt)
    st.markdown(f"⭐ Punkte: **{st.session_state.punkte}**")
    st.divider()


    st.subheader(aktuelle["frage"])

    if not st.session_state.antwort_gegeben:
        for i, antwort in enumerate(aktuelle["antworten"]):
            if st.button(antwort, key=f"a_{i}"):
                korrekt = aktuelle["richtig"]
                st.session_state.letzte_korrekt = (i == korrekt)
                if i == korrekt:
                    st.session_state.punkte += 1
                st.session_state.antwort_gegeben = True
                st.rerun()
    else:
        # Feedback anzeigen
        if st.session_state.letzte_korrekt:
            st.markdown('<div class="feedback-ok">✅ Richtig! Super gemacht!</div>',
                        unsafe_allow_html=True)
        else:
            richtige_antwort = aktuelle["antworten"][aktuelle["richtig"]]
            st.markdown(
                f'<div class="feedback-fail">❌ Falsch! '
                f'Die richtige Antwort war: <strong>{richtige_antwort}</strong></div>',
                unsafe_allow_html=True
            )

        # Weiter-Button
        naechste_label = "Nächste Frage ➡️" if idx + 1 < gesamt else "Ergebnis sehen 🏆"
        if st.button(naechste_label, type="primary"):
            if idx + 1 < gesamt:
                st.session_state.frage_idx += 1
                st.session_state.antwort_gegeben = False
                st.session_state.letzte_korrekt = None
            else:
                st.session_state.phase = "ergebnis"
            st.rerun()

    st.divider()
    if st.button("↩️ Abbrechen & neu starten"):
        reset()
        st.rerun()


elif st.session_state.phase == "ergebnis":
    thema  = st.session_state.thema
    punkte = st.session_state.punkte
    gesamt = len(questions[thema])
    prozent = round(punkte / gesamt * 100)

    st.markdown('<p class="quiz-header">🏆 Dein Ergebnis</p>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="score-box">'
        f'<span style="color:#f5f5f5;font-weight:700;"> Thema: {thema}</span> <br>'
        f'<span style="color:#f5f5f5;font-weight:700;"> Punkte: {punkte} / {gesamt} ({prozent} %)</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Bewertung
    if prozent == 100:
        st.success("🎉 Perfekt! Alle Fragen richtig – unschlagbar!")
    elif prozent >= 80:
        st.success("👏 Sehr gut! Du kennst dich wirklich aus!")
    elif prozent >= 60:
        st.info("🙂 Gut gemacht! Mit etwas Übung wird's noch besser.")
    elif prozent >= 40:
        st.warning("😅 Nicht schlecht, aber da ist noch Luft nach oben.")
    else:
        st.error("😬 Das Thema solltest du nochmal wiederholen!")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Gleiches Thema nochmal", type="primary"):
            gespeichertes_thema = st.session_state.thema
            reset()
            st.session_state.thema = gespeichertes_thema
            st.session_state.phase = "quiz"
            st.rerun()
    with col2:
        if st.button("🏠 Zurück zur Startseite"):
            reset()
            st.rerun()

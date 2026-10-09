import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.write("Type your name, choose a style, and bring your name to life!")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Customize your app")

name = st.sidebar.text_input("Enter your name", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font type",
    ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
)
font_size = st.sidebar.slider("Font size (px)", min_value=20, max_value=100, value=48, step=2)

backgrounds = {
    "Light": ("#ffffff", "#171717"),
    "Dark": ("#10131c", "#ffffff"),
    "Ocean": ("linear-gradient(135deg, #063970, #38bdf8)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #7c2d12, #fb7185, #fbbf24)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #052e16, #166534, #86efac)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #312e81, #a78bfa, #f5d0fe)", "#ffffff"),
}
background = st.sidebar.selectbox("Background", list(backgrounds.keys()))
name_mode = st.sidebar.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
effect = st.sidebar.selectbox(
    "Dynamic action",
    ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
)
speed_label = st.sidebar.select_slider(
    "Animation speed",
    options=["Slow", "Normal", "Fast"],
    value="Normal",
)
speed_seconds = {"Slow": 3.8, "Normal": 2.0, "Fast": 0.9}[speed_label]

bg, text_color = backgrounds[background]
safe_name = html.escape(name if name else "Hello World")
safe_font = font_family  # Selected from a fixed, trusted list above.
font_css = f'"{safe_font}", sans-serif'
if font_family in ("Arial", "Verdana", "Trebuchet MS", "Impact"):
    font_css = f'"{safe_font}", sans-serif'
elif font_family in ("Georgia", "Times New Roman"):
    font_css = f'"{safe_font}", serif'
else:
    font_css = f'"{safe_font}", monospace'

# Create decorative particles. CSS animations run continuously in the embedded browser
# without repeatedly rerunning the Streamlit Python script.
particle_config = {
    "Rain": ("💧", 34, "rain"),
    "Snow": ("❄", 30, "snow"),
    "Hail": ("🧊", 26, "hail"),
    "Wind gust": ("〰", 24, "wind"),
    "Confetti": ("🎉", 32, "confetti"),
    "Tornado": ("🌪️", 22, "tornado"),
}
particles = []
if effect in particle_config:
    symbol, count, animation_class = particle_config[effect]
    for i in range(count):
        left = random.randint(1, 98)
        delay = random.uniform(-speed_seconds, speed_seconds)
        duration = speed_seconds * random.uniform(0.75, 1.65)
        size = random.randint(13, 27) if effect != "Tornado" else random.randint(14, 24)
        # Escape symbol and keep all generated style values numeric.
        particles.append(
            f'<span class="particle {animation_class}" '
            f'style="left:{left}%; animation-delay:{delay:.2f}s; '
            f'animation-duration:{duration:.2f}s; font-size:{size}px;">{html.escape(symbol)}</span>'
        )

effect_layer = "".join(particles)

if name_mode == "Ticker Tape":
    name_content = f'<div class="ticker"><span>{safe_name}</span></div>'
elif name_mode == "Repeated":
    name_content = '<div class="repeated">' + "".join(
        f"<div>{safe_name}</div>" for _ in range(6)
    ) + "</div>"
else:
    name_content = f'<div class="center-name">{safe_name}</div>'

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative;
  width: 100%;
  height: 590px;
  overflow: hidden;
  border-radius: 16px;
  background: {bg};
  color: {text_color};
  font-family: {font_css};
}}
.effects {{
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  opacity: 0.88;
}}
.particle {{
  position: absolute;
  top: -50px;
  display: block;
  user-select: none;
  will-change: transform;
}}
.rain {{ animation-name: rain; animation-timing-function: linear; animation-iteration-count: infinite; }}
.snow {{ animation-name: snow; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
.hail {{ animation-name: hail; animation-timing-function: linear; animation-iteration-count: infinite; }}
.wind {{ top: auto; left: -12% !important; animation-name: wind; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
.confetti {{ animation-name: confetti; animation-timing-function: linear; animation-iteration-count: infinite; }}
.tornado {{ top: auto; animation-name: tornado; animation-timing-function: linear; animation-iteration-count: infinite; }}
@keyframes rain {{ 0% {{ transform: translateY(-30px) translateX(0); }} 100% {{ transform: translateY(680px) translateX(-45px); }} }}
@keyframes snow {{ 0% {{ transform: translateY(-35px) translateX(0) rotate(0deg); }} 50% {{ transform: translateY(300px) translateX(45px) rotate(180deg); }} 100% {{ transform: translateY(680px) translateX(-25px) rotate(360deg); }} }}
@keyframes hail {{ 0% {{ transform: translateY(-40px); }} 75% {{ transform: translateY(520px); }} 85% {{ transform: translateY(480px); }} 100% {{ transform: translateY(680px); }} }}
@keyframes wind {{ 0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0; }} 20% {{ opacity: 1; }} 100% {{ transform: translate(125vw, 90px) rotate(20deg); opacity: 0; }} }}
@keyframes confetti {{ 0% {{ transform: translateY(-40px) rotate(0deg); }} 100% {{ transform: translateY(680px) rotate(900deg); }} }}
@keyframes tornado {{ 0% {{ transform: translateY(0) translateX(-50px) scale(.6) rotate(0deg); }} 50% {{ transform: translateY(-270px) translateX(50px) scale(1.2) rotate(180deg); }} 100% {{ transform: translateY(-540px) translateX(-50px) scale(.6) rotate(360deg); }} }}
.name-layer {{
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 28px;
  text-align: center;
  font-size: {font_size}px;
  font-weight: 700;
  overflow: hidden;
  overflow-wrap: anywhere;
  text-shadow: 0 2px 8px rgba(0,0,0,.18);
}}
.center-name {{ width: 100%; }}
.ticker {{ width: 100%; overflow: hidden; white-space: nowrap; }}
.ticker span {{
  display: inline-block;
  padding-left: 100%;
  animation: marquee 10s linear infinite;
}}
@keyframes marquee {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-100%); }} }}
.repeated {{ width: 100%; line-height: 1.35; }}
@media (prefers-reduced-motion: reduce) {{
  .particle, .ticker span {{ animation-duration: 20s !important; }}
}}
</style>
</head>
<body>
  <div class="stage">
    <div class="effects">{effect_layer}</div>
    <div class="name-layer">{name_content}</div>
  </div>
</body>
</html>
"""

components.html(html_doc, height=610, scrolling=False)
st.caption("Tip: Try different backgrounds, fonts, display modes, and effects. The motion loops continuously inside the preview.")

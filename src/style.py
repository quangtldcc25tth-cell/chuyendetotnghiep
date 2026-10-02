"""Giao diện: CSS tùy chỉnh và các thành phần HTML dùng chung."""
import streamlit as st

PRIMARY = "#5B5BD6"
ACCENT = "#8B5CF6"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --primary: #5B5BD6;
  --accent: #8B5CF6;
  --bg: #F6F7FB;
  --card: #FFFFFF;
  --text: #1F2937;
  --muted: #6B7280;
  --border: #E5E7EB;
  --radius: 16px;
  --shadow: 0 1px 2px rgba(16,24,40,.04), 0 6px 18px rgba(16,24,40,.06);
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* Nền và khoảng cách trang */
[data-testid="stAppViewContainer"] { background: var(--bg); }
[data-testid="stHeader"] { background: transparent; }          /* giữ nút mở/đóng sidebar */
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }
#MainMenu, footer { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--card);
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding: 10px 14px;
  border-radius: 12px;
  transition: background .15s ease, transform .15s ease;
  cursor: pointer;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: #EEF0FF; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: #E8E8FF;
  font-weight: 600;
}

/* Banner tiêu đề trang */
.hero {
  background: linear-gradient(120deg, var(--primary) 0%, var(--accent) 100%);
  color: #fff;
  border-radius: 20px;
  padding: 26px 30px;
  margin-bottom: 22px;
  box-shadow: 0 10px 28px rgba(91,91,214,.28);
}
.hero h1 { color: #fff; font-size: 1.7rem; font-weight: 700; margin: 0 0 4px 0; padding: 0; }
.hero p  { color: rgba(255,255,255,.88); margin: 0; font-size: .98rem; }

/* Thẻ chỉ số (st.metric) */
[data-testid="stMetric"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 18px;
  box-shadow: var(--shadow);
}
[data-testid="stMetricLabel"] { color: var(--muted); font-weight: 500; }
[data-testid="stMetricValue"] { font-weight: 700; color: var(--text); }

/* Khung có viền (st.container(border=True)) -> thẻ bo góc */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--card);
  border-radius: var(--radius) !important;
  border-color: var(--border) !important;
  box-shadow: var(--shadow);
}

/* Form, expander, bảng dữ liệu */
[data-testid="stForm"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
}
[data-testid="stExpander"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
}
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* Ô nhập liệu */
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] {
  border-radius: 12px !important;
}
textarea, input { border-radius: 12px !important; }
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"]:focus-within {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(91,91,214,.18) !important;
}

/* Nút bấm */
.stButton > button, [data-testid="stFormSubmitButton"] > button {
  background: linear-gradient(120deg, var(--primary), var(--accent));
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: .55rem 1.4rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(91,91,214,.30);
  transition: transform .12s ease, box-shadow .12s ease;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 18px rgba(91,91,214,.38);
  color: #fff;
}
.stButton > button:active, [data-testid="stFormSubmitButton"] > button:active { transform: translateY(0); }

/* Thông báo (info/success/warning) */
[data-testid="stAlert"] { border-radius: 14px; }

/* Tiêu đề phụ */
h2, h3 { color: var(--text); font-weight: 600; letter-spacing: -.01em; }

/* Thẻ kết quả dự báo */
.risk-card { border-radius: 18px; padding: 22px 26px; margin: 8px 0 14px 0; border: 1px solid; }
.risk-card .pct { font-size: 2.8rem; font-weight: 800; line-height: 1.1; }
.risk-card .lbl { font-size: 1.05rem; font-weight: 600; margin-bottom: 2px; }
.risk-card .tip { margin-top: 6px; font-size: .95rem; }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="hero"><h1>{title}</h1>{sub}</div>', unsafe_allow_html=True)


def risk_card(p: float) -> None:
    if p >= 0.6:
        color, bg, lbl = "#B42318", "#FEF3F2", "Nguy cơ trễ hạn CAO"
        tip = "Nên đàm phán thêm thời gian hoặc giới hạn số vòng chỉnh sửa ngay từ đầu."
    elif p >= 0.4:
        color, bg, lbl = "#B54708", "#FFFAEB", "Nguy cơ trễ hạn TRUNG BÌNH"
        tip = "Theo dõi sát giai đoạn sản xuất và feedback; chuẩn bị thời gian dự phòng."
    else:
        color, bg, lbl = "#067647", "#ECFDF3", "Nguy cơ trễ hạn THẤP"
        tip = "Tiến độ dự kiến hợp lý; vẫn nên chốt rõ số vòng chỉnh sửa."
    st.markdown(
        f'<div class="risk-card" style="background:{bg};border-color:{color}55;color:{color}">'
        f'<div class="lbl">{lbl}</div><div class="pct">{p:.0%}</div>'
        f'<div class="tip">{tip}</div></div>',
        unsafe_allow_html=True,
    )

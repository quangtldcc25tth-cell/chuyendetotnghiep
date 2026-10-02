"""Đọc/ghi dữ liệu: CSV (dự án, giai đoạn) và JSON (chi tiết dự án, wiki quy trình)."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CHI_TIET_FILE = DATA / "chi_tiet_du_an.json"
QUY_TRINH_FILE = DATA / "quy_trinh.json"

# 7 giai đoạn theo sơ đồ quy trình nghiệp vụ (giữ đồng bộ với sinh_du_lieu_mo_phong.py)
QUY_TRINH_MAC_DINH = [
    {"ten": "1. Tiếp nhận yêu cầu & Khởi tạo dự án",
     "mo_ta": "Nhận thông tin từ khách hàng: thể loại nhạc, bài tham khảo, BPM, Key, ngân sách, deadline.\n"
              "- Phân tích yêu cầu khách hàng và xác định phạm vi công việc\n"
              "- Khách hàng đồng ý? Không: điều chỉnh yêu cầu rồi phân tích lại. Có: khởi tạo dự án và lưu thông tin"},
    {"ten": "2. Pre-production / Lên ý tưởng",
     "mo_ta": "Concept, Chord, Melody, MIDI Sketch.\n"
              "- Chọn VST / Sample, Sound Design\n"
              "- Xuất bản Demo\n"
              "- Demo đạt yêu cầu? Không: chỉnh sửa ý tưởng rồi xuất demo lại. Có: sang giai đoạn 3"},
    {"ten": "3. Production / Arranging",
     "mo_ta": "Dựng và sắp xếp bài:\n"
              "- Drum / Percussion\n- Bass / Chord / Lead\n- Pad / FX\n"
              "- Vocal / Instrument\n- Arrangement\n- Automation"},
    {"ten": "4. Mixing",
     "mo_ta": "Gain Staging, Volume / Panning, EQ, Compression.\n"
              "- Reverb / Delay, Stereo / Spatial\n"
              "- Balance các Stem, Export Mixdown\n"
              "- Mix đạt yêu cầu? Không: quay lại chỉnh mix. Có: sang Mastering"},
    {"ten": "5. Mastering",
     "mo_ta": "Master EQ, Compression, Limiting, Stereo Enhancement.\n"
              "- Kiểm tra Loudness và True Peak\n- Export Master"},
    {"ten": "6. Review & Revision",
     "mo_ta": "Gửi bản Preview cho khách hàng.\n"
              "- Khách hàng yêu cầu chỉnh sửa? Có: tiếp nhận Feedback, xác định phần cần sửa, rồi gửi lại bản Preview (vòng lặp)\n"
              "- Không: phê duyệt\n- Sau Review chuyển sang giai đoạn 7"},
    {"ten": "7. Final Delivery & Archiving",
     "mo_ta": "Bàn giao khách hàng: WAV / MP3, Final Master, Stems, Project File.\n"
              "- Lưu Project, lưu Audio / Stem, backup Cloud / Drive\n- Kết thúc dự án"},
]


@st.cache_data
def load_du_an() -> pd.DataFrame:
    df = pd.read_csv(DATA / "du_an.csv", parse_dates=["ngay_nhan_brief"])
    return df.sort_values("ngay_nhan_brief").reset_index(drop=True)


@st.cache_data
def load_giai_doan() -> pd.DataFrame:
    return pd.read_csv(DATA / "giai_doan.csv")


def _read_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return default
    return default


def _write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_chi_tiet() -> dict:
    return _read_json(CHI_TIET_FILE, {})


def save_chi_tiet(d: dict) -> None:
    _write_json(CHI_TIET_FILE, d)


def load_quy_trinh() -> list:
    return _read_json(QUY_TRINH_FILE, QUY_TRINH_MAC_DINH)


def save_quy_trinh(lst: list) -> None:
    _write_json(QUY_TRINH_FILE, lst)

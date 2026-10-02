"""Ứng dụng quản lý dự án sản xuất âm thanh. Chạy: streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="Quản lý dự án âm thanh", layout="wide")

from src import store, style, trang_dashboard, trang_du_an, trang_du_bao, trang_quy_trinh  # noqa: E402

style.inject_css()

TRANG = {
    "Dashboard": trang_dashboard,
    "Chi tiết dự án": trang_du_an,
    "Dự báo trễ hạn": trang_du_bao,
    "Sơ đồ & Quy trình": trang_quy_trinh,
}

st.sidebar.markdown("Quản lý dự án\nSản xuất âm thanh")
chon = st.sidebar.radio("Điều hướng", list(TRANG.keys()), label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("Dữ liệu: mô phỏng (xem README)")

try:
    df = store.load_du_an()
    gd = store.load_giai_doan()
except FileNotFoundError:
    st.error("Chưa có dữ liệu. Chạy: python sinh_du_lieu_mo_phong.py (sẽ tạo thư mục data/).")
    st.stop()

TRANG[chon].render(df, gd)

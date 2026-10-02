import pandas as pd
import streamlit as st

from src import style


def _card(title: str, chart_fn, data):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        chart_fn(data, color=style.PRIMARY)


def render(df: pd.DataFrame, gd: pd.DataFrame):
    style.hero("Dashboard KPI", "Tổng quan tiến độ và tỷ lệ trễ hạn của các dự án sản xuất âm thanh")

    with st.container(border=True):
        c1, c2 = st.columns(2)
        loai = c1.multiselect("Loại sản phẩm", sorted(df["loai_san_pham"].unique()),
                              default=sorted(df["loai_san_pham"].unique()))
        nam = c2.multiselect("Năm nhận brief", sorted(df["ngay_nhan_brief"].dt.year.unique()),
                             default=sorted(df["ngay_nhan_brief"].dt.year.unique()))
    d = df[df["loai_san_pham"].isin(loai) & df["ngay_nhan_brief"].dt.year.isin(nam)]
    if d.empty:
        st.warning("Không có dự án nào khớp bộ lọc.")
        return

    st.write("")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Số dự án", len(d))
    k2.metric("Tỷ lệ trễ hạn", f"{d['tre_han'].mean():.0%}")
    k3.metric("Ngày hoàn thành TB", f"{d['so_ngay_thuc_te'].mean():.1f}")
    k4.metric("Vòng chỉnh sửa TB", f"{d['so_vong_chinh_sua'].mean():.1f}")

    st.write("")
    a, b = st.columns(2)
    with a:
        _card("Tỷ lệ trễ hạn theo thể loại", st.bar_chart, d.groupby("the_loai")["tre_han"].mean())
    with b:
        _card("Tỷ lệ trễ hạn theo độ phức tạp brief", st.bar_chart,
              d.groupby("do_phuc_tap_brief")["tre_han"].mean())

    g = gd[gd["du_an_id"].isin(d["du_an_id"])]
    c, e = st.columns(2)
    with c:
        _card("Số ngày trung bình ở từng giai đoạn", st.bar_chart,
              g.groupby("giai_doan")["so_ngay"].mean())
    with e:
        theo_thang = d.groupby(d["ngay_nhan_brief"].dt.to_period("M").astype(str)).size()
        _card("Số dự án nhận theo tháng", st.bar_chart, theo_thang)

    with st.expander("Xem bảng dữ liệu"):
        st.dataframe(d, use_container_width=True)

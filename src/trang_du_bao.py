import pandas as pd
import streamlit as st

from src import model as ml
from src import style


def render(df: pd.DataFrame, gd: pd.DataFrame):
    style.hero("Dự báo nguy cơ trễ hạn", "Nhập thông tin brief để ước lượng khả năng trễ deadline")
    st.info("Mô hình baseline: Logistic Regression, huấn luyện trên dữ liệu MÔ PHỎNG. "
            "Kết quả chỉ mang tính hỗ trợ, không thay thế đánh giá của người quản lý dự án.")

    res = ml.train(df)

    with st.container(border=True):
        st.markdown("**Thông tin dự án mới**")
        c1, c2 = st.columns(2)
        loai = c1.selectbox("Loại sản phẩm", sorted(df["loai_san_pham"].unique()))
        the_loai = c2.selectbox("Thể loại", sorted(df["the_loai"].unique()))
        c3, c4, c5 = st.columns(3)
        bpm = c3.number_input("BPM", 40, 220, 100)
        so_track = c4.number_input("Số track", 1, 80, 12)
        so_vst = c5.number_input("Số VST/plugin", 0, 60, 10)
        c6, c7, c8 = st.columns(3)
        phuc_tap = c6.slider("Độ phức tạp brief (1-5)", 1, 5, 3)
        deadline = c7.number_input("Deadline (ngày)", 1, 90, 14)
        kh_moi = c8.checkbox("Khách hàng mới")
        tham_khao = c8.checkbox("Có bài tham khảo")
        bam = st.button("Dự báo")

    if bam:
        p = ml.predict_proba(res["model"], {
            "loai_san_pham": loai, "the_loai": the_loai, "bpm": bpm, "so_track": so_track,
            "so_vst": so_vst, "do_phuc_tap_brief": phuc_tap, "khach_hang_moi": int(kh_moi),
            "co_bai_tham_khao": int(tham_khao), "so_ngay_deadline": deadline})
        style.risk_card(p)

    st.markdown("### Đánh giá mô hình")
    st.caption(f"Chia theo thời gian: train {res['n_train']} dự án đầu, test {res['n_test']} dự án "
               f"từ {res['test_from']}. Random seed = {ml.SEED}.")
    m = res["metrics"]
    cols = st.columns(len(m))
    for col, (k, v) in zip(cols, m.items()):
        col.metric(k.split(" (")[0], f"{v:.2f}")
    st.caption(f"Baseline ngây thơ (luôn đoán lớp đa số): accuracy = {res['baseline_accuracy']:.2f}")

    a, b = st.columns(2)
    with a:
        with st.container(border=True):
            st.markdown("**Confusion matrix** (hàng: thực tế, cột: dự đoán)")
            st.dataframe(pd.DataFrame(res["confusion"], index=["Đúng hạn", "Trễ hạn"],
                                      columns=["Đoán đúng hạn", "Đoán trễ hạn"]),
                         use_container_width=True)
    with b:
        with st.container(border=True):
            st.markdown("**Hệ số mô hình** (dương: tăng nguy cơ trễ)")
            st.dataframe(res["coefs"].head(8).round(3), use_container_width=True, hide_index=True)

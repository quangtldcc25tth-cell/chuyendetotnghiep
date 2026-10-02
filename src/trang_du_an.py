import pandas as pd
import streamlit as st

from src import store, style


def render(df: pd.DataFrame, gd: pd.DataFrame):
    style.hero("Chi tiết dự án", "Thông tin dự án, ghi chú kỹ thuật, VST/Plugin và link tài nguyên")

    du_an_id = st.selectbox("Chọn dự án", df["du_an_id"].tolist())
    r = df[df["du_an_id"] == du_an_id].iloc[0]

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Loại:** {r['loai_san_pham']}")
        c1.write(f"**Thể loại:** {r['the_loai']} – {r['bpm']} BPM")
        c2.write(f"**Số track:** {r['so_track']} | **VST dự kiến:** {r['so_vst']}")
        c2.write(f"**Ngày nhận brief:** {r['ngay_nhan_brief'].date()}")
        trang_thai = "🔴 Trễ hạn" if r["tre_han"] == 1 else "🟢 Đúng hạn"
        c3.write(f"**Deadline:** {r['so_ngay_deadline']} ngày")
        c3.write(f"**Thực tế:** {r['so_ngay_thuc_te']} ngày – {trang_thai}")

    with st.container(border=True):
        st.markdown("**Thời gian từng giai đoạn (ngày)**")
        st.bar_chart(gd[gd["du_an_id"] == du_an_id].set_index("giai_doan")["so_ngay"], color=style.PRIMARY)

    st.markdown("### Ghi chú kỹ thuật và tài nguyên")
    chi_tiet = store.load_chi_tiet()
    cu = chi_tiet.get(du_an_id, {})
    with st.form(f"form_{du_an_id}"):
        vst = st.text_area("VST/Plugin đã dùng (mỗi dòng một plugin)", value=cu.get("vst", ""))
        a, b = st.columns(2)
        sd = a.text_area("Ghi chú Sound Design", value=cu.get("sound_design", ""))
        mx = b.text_area("Ghi chú Mixing", value=cu.get("mixing", ""))
        l1 = a.text_input("Link Google Drive – Stems", value=cu.get("link_stems", ""))
        l2 = b.text_input("Link Google Drive – Demo", value=cu.get("link_demo", ""))
        if st.form_submit_button("Lưu"):
            chi_tiet[du_an_id] = {"vst": vst, "sound_design": sd, "mixing": mx,
                                  "link_stems": l1, "link_demo": l2}
            store.save_chi_tiet(chi_tiet)
            st.success("Đã lưu.")

    cu = chi_tiet.get(du_an_id, {})
    if cu.get("link_stems"):
        st.markdown(f"[Mở thư mục Stems]({cu['link_stems']})")
    if cu.get("link_demo"):
        st.markdown(f"[Mở thư mục Demo]({cu['link_demo']})")

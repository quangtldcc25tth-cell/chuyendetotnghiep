import streamlit as st

from src import store, style


def render(df=None, gd=None):
    style.hero("Sơ đồ & Hướng dẫn quy trình",
               "Wiki 7 giai đoạn sản xuất – chỉnh sửa trực tiếp rồi bấm Lưu")
    qt = store.load_quy_trinh()

    with st.form("form_quy_trinh"):
        moi = []
        for i, gd_ in enumerate(qt):
            with st.expander(gd_["ten"], expanded=(i == 0)):
                mo_ta = st.text_area("Nội dung / checklist", value=gd_["mo_ta"], key=f"qt_{i}", height=140)
            moi.append({"ten": gd_["ten"], "mo_ta": mo_ta})
        if st.form_submit_button("Lưu thay đổi"):
            store.save_quy_trinh(moi)
            st.success("Đã lưu.")

    st.markdown("### Sơ đồ quy trình nghiệp vụ")
    up = st.file_uploader("Tải ảnh sơ đồ quy trình của bạn lên để hiển thị", type=["png", "jpg", "jpeg"])
    if up is not None:
        st.image(up, use_container_width=True)

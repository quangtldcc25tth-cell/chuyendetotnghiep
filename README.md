# Quản lý dự án sản xuất âm thanh (Mức 1 – Thực tập ngành)

Ứng dụng Streamlit: dashboard KPI, chi tiết dự án (VST/ghi chú/link Drive), dự báo nguy cơ trễ hạn
(baseline Logistic Regression), quy trình 7 giai đoạn.

## Cài đặt và chạy (Windows)
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python sinh_du_lieu_mo_phong.py      # tạo lại dữ liệu mô phỏng (đã có sẵn trong data/)
streamlit run app.py
```

## Cấu trúc
- `app.py`: điểm vào, điều hướng giữa các trang
- `src/store.py`: đọc/ghi dữ liệu; `src/model.py`: baseline ML; `src/trang_*.py`: từng trang
- `data/`: du_an.csv, giai_doan.csv, data_dictionary.csv (mô phỏng); chi_tiet_du_an.json và quy_trinh.json được tạo khi bạn lưu

## Lưu ý
- Dữ liệu là MÔ PHỎNG (seed=42). Kết quả ML chỉ chứng minh pipeline đúng.
- Chia train/test theo thời gian; không dùng so_vong_chinh_sua / so_ngay_tre làm feature (rò rỉ).

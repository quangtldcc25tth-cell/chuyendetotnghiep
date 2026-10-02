"""
sinh_du_lieu_mo_phong.py
------------------------
Sinh dữ liệu MÔ PHỎNG cho đề tài:
"Số hóa quy trình quản lý dự án sản xuất âm thanh và phát triển hệ thống
dự báo tiến độ, gợi ý thiết bị/sample bằng Machine Learning kết hợp Ontology"

Đầu ra (thư mục data/):
  - du_an.csv       : 1 dòng / dự án  (dùng cho ML + dashboard)
  - giai_doan.csv   : 1 dòng / (dự án, giai đoạn) (dùng cho dashboard thời gian từng giai đoạn)
  - data_dictionary.csv : mô tả từng cột

Cách chạy:
    pip install numpy pandas
    python sinh_du_lieu_mo_phong.py                # mặc định 250 dự án, seed=42
    python sinh_du_lieu_mo_phong.py --n 300 --seed 7

LƯU Ý KHI VIẾT BÁO CÁO:
  * Đây là dữ liệu mô phỏng, KHÔNG phải dữ liệu thật. Phải nêu rõ điều này.
  * Các "quy luật" dùng để sinh dữ liệu nằm ở phần QUY_LUAT bên dưới -- hãy mô tả
    chúng trong báo cáo (ví dụ: brief phức tạp, nhiều track, khách hàng mới
    => dễ trễ hạn hơn). Kết quả ML chỉ chứng minh quy trình hoạt động đúng,
    chưa chứng minh hiệu quả trên thực tế.
  * Nếu có dữ liệu thật (đã ẩn danh), hãy thay/trộn vào file du_an.csv với
    đúng tên cột.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# 1. CẤU HÌNH
# ----------------------------------------------------------------------------

# 7 giai đoạn theo sơ đồ quy trình nghiệp vụ 
    "1. Tiếp nhận yêu cầu & Khởi tạo dự án",
    "2. Pre-production / Lên ý tưởng",
    "3. Production / Arranging",
    "4. Mixing",
    "5. Mastering",
    "6. Review & Revision",
    "7. Final Delivery & Archiving",
]

# số ngày trung bình (cơ sở) của từng giai đoạn; tổng giữ nguyên 14.2 ngày
NGAY_CO_SO = np.array([0.7, 2.5, 5.0, 2.5, 1.0, 1.9, 0.6])

LOAI_SAN_PHAM = ["Bài hát", "Nhạc nền video", "Jingle quảng cáo", "Nhạc game"]
P_LOAI = [0.35, 0.30, 0.20, 0.15]
# hệ số khối lượng công việc theo loại sản phẩm
HE_SO_LOAI = {"Bài hát": 1.25, "Nhạc nền video": 1.0, "Jingle quảng cáo": 0.6, "Nhạc game": 1.1}

THE_LOAI = ["Pop", "EDM", "Lo-fi", "Cinematic", "Hip-hop", "Acoustic"]
P_THE_LOAI = [0.22, 0.18, 0.15, 0.15, 0.17, 0.13]
# (BPM thấp nhất, BPM cao nhất) theo thể loại
BPM_RANGE = {
    "Pop": (90, 130),
    "EDM": (120, 150),
    "Lo-fi": (65, 90),
    "Cinematic": (60, 110),
    "Hip-hop": (75, 105),
    "Acoustic": (70, 120),
}
# hệ số độ khó theo thể loại
HE_SO_THE_LOAI = {
    "Pop": 1.0, "EDM": 1.1, "Lo-fi": 0.8,
    "Cinematic": 1.3, "Hip-hop": 1.0, "Acoustic": 0.9,
}

# ----------------------------------------------------------------------------
# 2. QUY_LUAT (mô tả trong báo cáo)
#    Thời gian thực tế = khối lượng cơ bản
#                         x (1 + 0.22*(độ phức tạp brief - 3))
#                         x (1 + 0.012*(số track - 12))
#                         x (1.15 nếu khách hàng mới)
#                         x (0.9 nếu có bài tham khảo)
#                         x hệ số loại sản phẩm, thể loại
#                         + 1.8 ngày cho mỗi vòng chỉnh sửa
#                         + nhiễu ngẫu nhiên
#    Deadline kế hoạch = ước lượng "lạc quan" của người làm (thường thấp hơn
#    thực tế một chút) => tạo ra tỷ lệ trễ hạn khoảng 30-40%.
# ----------------------------------------------------------------------------


def sinh_du_an(n: int, rng: np.random.Generator) -> pd.DataFrame:
    # Ngày nhận brief: trải đều từ 01/01/2025 đến 30/09/2026, sắp xếp theo thời gian
    # (để có thể chia train/test theo thời gian, tránh rò rỉ dữ liệu)
    ngay_bat_dau = pd.Timestamp("2025-01-01")
    ngay_ket_thuc = pd.Timestamp("2026-09-30")
    tong_ngay = (ngay_ket_thuc - ngay_bat_dau).days
    offset = np.sort(rng.integers(0, tong_ngay, size=n))
    ngay_nhan_brief = ngay_bat_dau + pd.to_timedelta(offset, unit="D")

    loai = rng.choice(LOAI_SAN_PHAM, size=n, p=P_LOAI)
    the_loai = rng.choice(THE_LOAI, size=n, p=P_THE_LOAI)

    bpm = np.array([rng.integers(*BPM_RANGE[g]) for g in the_loai])

    # số track: jingle ít track hơn, bài hát nhiều hơn
    track_mean = {"Bài hát": 18, "Nhạc nền video": 12, "Jingle quảng cáo": 8, "Nhạc game": 14}
    so_track = np.array([max(3, int(rng.normal(track_mean[l], 4))) for l in loai])

    # số VST/plugin dùng, tương quan nhẹ với số track
    so_vst = np.clip((so_track * rng.uniform(0.6, 1.4, size=n)).astype(int), 2, 40)

    do_phuc_tap = np.clip(np.round(rng.normal(3, 1.1, size=n)), 1, 5).astype(int)
    khach_hang_moi = rng.binomial(1, 0.4, size=n)
    co_bai_tham_khao = rng.binomial(1, 0.6, size=n)

    # ----- khối lượng công việc & thời gian thực tế -----
    co_so = NGAY_CO_SO.sum()
    he_so = (
        np.array([HE_SO_LOAI[l] for l in loai])
        * np.array([HE_SO_THE_LOAI[g] for g in the_loai])
        * (1 + 0.22 * (do_phuc_tap - 3))
        * (1 + 0.012 * (so_track - 12))
        * np.where(khach_hang_moi == 1, 1.15, 1.0)
        * np.where(co_bai_tham_khao == 1, 0.9, 1.0)
    )
    he_so = np.clip(he_so, 0.4, None)

    # số vòng chỉnh sửa (khách hàng yêu cầu sửa) -- Poisson, phụ thuộc brief/khách mới/tham khảo
    lam = np.clip(
        0.8 + 0.35 * (do_phuc_tap - 3) + 0.6 * khach_hang_moi - 0.4 * co_bai_tham_khao,
        0.2, None,
    )
    so_vong_chinh_sua = rng.poisson(lam)

    nhieu = rng.normal(0, 1.5, size=n)
    so_ngay_thuc_te = np.round(co_so * he_so + 1.8 * so_vong_chinh_sua + nhieu).clip(3, None)

    # ----- deadline kế hoạch: ước lượng lạc quan -----
    uoc_luong = co_so * he_so * rng.normal(1.08, 0.18, size=n)  # chưa tính vòng chỉnh sửa
    so_ngay_deadline = np.round(uoc_luong + rng.normal(1.5, 1.5, size=n)).clip(3, None)

    tre_han = (so_ngay_thuc_te > so_ngay_deadline).astype(int)
    so_ngay_tre = np.maximum(0, so_ngay_thuc_te - so_ngay_deadline)

    df = pd.DataFrame(
        {
            "du_an_id": [f"DA{str(i + 1).zfill(3)}" for i in range(n)],
            "ngay_nhan_brief": ngay_nhan_brief.strftime("%Y-%m-%d"),
            "loai_san_pham": loai,
            "the_loai": the_loai,
            "bpm": bpm,
            "so_track": so_track,
            "so_vst": so_vst,
            "do_phuc_tap_brief": do_phuc_tap,
            "khach_hang_moi": khach_hang_moi,
            "co_bai_tham_khao": co_bai_tham_khao,
            "so_ngay_deadline": so_ngay_deadline.astype(int),
            # ---- các cột KẾT QUẢ (chỉ biết sau khi xong dự án) ----
            "so_vong_chinh_sua": so_vong_chinh_sua,
            "so_ngay_thuc_te": so_ngay_thuc_te.astype(int),
            "so_ngay_tre": so_ngay_tre.astype(int),
            "tre_han": tre_han,
        }
    )
    return df


def sinh_giai_doan(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Chia so_ngay_thuc_te của mỗi dự án cho 7 giai đoạn (tổng khớp đúng)."""
    rows = []
    ty_le_co_so = NGAY_CO_SO / NGAY_CO_SO.sum()
    for _, r in df.iterrows():
        w = ty_le_co_so * rng.uniform(0.7, 1.3, size=len(GIAI_DOAN))
        # giai đoạn 6 (Review & Revision) phình ra theo số vòng chỉnh sửa
        w[5] *= 1 + 0.5 * r["so_vong_chinh_sua"]
        w = w / w.sum()
        chia = w * r["so_ngay_thuc_te"]
        ngay = np.floor(chia).astype(int)
        # phần dư chia lần lượt cho các giai đoạn có phần thập phân lớn nhất
        du = int(r["so_ngay_thuc_te"] - ngay.sum())
        for i in np.argsort(-(chia - ngay))[:du]:
            ngay[i] += 1
        for gd, d in zip(GIAI_DOAN, ngay):
            rows.append({"du_an_id": r["du_an_id"], "giai_doan": gd, "so_ngay": int(d)})
    return pd.DataFrame(rows)


def data_dictionary() -> pd.DataFrame:
    rows = [
        ("du_an_id", "Mã dự án", "chuỗi", "Khóa chính", "Định danh"),
        ("ngay_nhan_brief", "Ngày nhận brief", "ngày (YYYY-MM-DD)", "Đã biết lúc bắt đầu", "Dùng để chia train/test theo thời gian"),
        ("loai_san_pham", "Loại sản phẩm", "phân loại", "Đã biết lúc bắt đầu", "Đặc trưng (feature)"),
        ("the_loai", "Thể loại nhạc", "phân loại", "Đã biết lúc bắt đầu", "Đặc trưng; sau này là khái niệm trong Ontology"),
        ("bpm", "Nhịp độ (BPM)", "số nguyên", "Đã biết lúc bắt đầu", "Đặc trưng"),
        ("so_track", "Số track dự kiến trong project DAW", "số nguyên", "Ước lượng lúc bắt đầu", "Đặc trưng"),
        ("so_vst", "Số VST/plugin dự kiến dùng", "số nguyên", "Ước lượng lúc bắt đầu", "Đặc trưng"),
        ("do_phuc_tap_brief", "Độ phức tạp của brief (1-5)", "số nguyên 1-5", "Đánh giá lúc nhận brief", "Đặc trưng"),
        ("khach_hang_moi", "Khách hàng mới (1) hay cũ (0)", "nhị phân", "Đã biết lúc bắt đầu", "Đặc trưng"),
        ("co_bai_tham_khao", "Brief có bài tham khảo (1) hay không (0)", "nhị phân", "Đã biết lúc bắt đầu", "Đặc trưng"),
        ("so_ngay_deadline", "Số ngày deadline đã thỏa thuận", "số nguyên", "Đã biết lúc bắt đầu", "Đặc trưng; cũng là mốc để xác định trễ hạn"),
        ("so_vong_chinh_sua", "Số vòng chỉnh sửa theo yêu cầu khách", "số nguyên", "CHỈ BIẾT SAU KHI XONG", "KHÔNG dùng khi dự báo lúc bắt đầu (rò rỉ dữ liệu); chỉ dùng cho phân tích"),
        ("so_ngay_thuc_te", "Số ngày thực tế hoàn thành", "số nguyên", "KẾT QUẢ", "Target cho bài toán hồi quy"),
        ("so_ngay_tre", "Số ngày trễ so với deadline (0 nếu đúng hạn)", "số nguyên", "KẾT QUẢ", "Chỉ dùng cho dashboard, KHÔNG làm feature"),
        ("tre_han", "Trễ hạn (1) hay đúng hạn (0)", "nhị phân", "KẾT QUẢ", "Target cho bài toán phân loại"),
    ]
    return pd.DataFrame(
        rows, columns=["cot", "y_nghia", "kieu_du_lieu", "thoi_diem_biet", "vai_tro_ghi_chu"]
    )


def main():
    ap = argparse.ArgumentParser(description="Sinh dữ liệu mô phỏng dự án sản xuất âm thanh")
    ap.add_argument("--n", type=int, default=250, help="số dự án (mặc định 250)")
    ap.add_argument("--seed", type=int, default=42, help="random seed để tái lập (mặc định 42)")
    ap.add_argument("--out", type=str, default="data", help="thư mục xuất file")
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = sinh_du_an(args.n, rng)
    gd = sinh_giai_doan(df, rng)

    df.to_csv(out / "du_an.csv", index=False, encoding="utf-8-sig")
    gd.to_csv(out / "giai_doan.csv", index=False, encoding="utf-8-sig")
    data_dictionary().to_csv(out / "data_dictionary.csv", index=False, encoding="utf-8-sig")

    print(f"Đã sinh {len(df)} dự án (seed={args.seed}) vào thư mục '{out}/'")
    print(f"Tỷ lệ trễ hạn: {df['tre_han'].mean():.1%}")
    print(f"Số ngày thực tế: trung bình {df['so_ngay_thuc_te'].mean():.1f}, "
          f"min {df['so_ngay_thuc_te'].min()}, max {df['so_ngay_thuc_te'].max()}")
    print("\n5 dòng đầu:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()

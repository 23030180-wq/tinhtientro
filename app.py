import streamlit as st
import pandas as pd

# ==========================
# CẤU HÌNH TRANG
# ==========================

st.set_page_config(
    page_title="Quản lý dãy phòng trọ",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HỆ THỐNG QUẢN LÝ TIỀN PHÒNG TRỌ")
st.caption("Quản lý tiền phòng - điện - nước - phụ phí cho toàn bộ dãy phòng")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("⚙️ CẤU HÌNH")

gia_phong = st.sidebar.number_input(
    "💰 Tiền phòng (VNĐ)",
    value=2500000,
    step=50000
)

gia_dien = st.sidebar.number_input(
    "⚡ Giá điện",
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "💧 Giá nước",
    value=15000,
    step=500
)

internet = st.sidebar.number_input(
    "🌐 Internet",
    value=100000,
    step=10000
)

rac = st.sidebar.number_input(
    "🗑️ Rác",
    value=30000,
    step=5000
)

gui_xe = st.sidebar.number_input(
    "🏍️ Tiền xe",
    value=100000,
    step=10000
)

phu_phi = st.sidebar.number_input(
    "📦 Phụ phí khác",
    value=20000,
    step=5000
)

so_phong = st.sidebar.slider(
    "🏠 Số phòng",
    1,
    50,
    10
)

st.divider()

st.header("📋 NHẬP THÔNG TIN CÁC PHÒNG")

ket_qua = []

tong_day = 0
tong_dien = 0
tong_nuoc = 0

for i in range(1, so_phong + 1):

    with st.expander(f"🏠 Phòng {i}", expanded=False):

        c1, c2 = st.columns(2)

        with c1:
            ten = st.text_input(
                "Tên người thuê",
                key=f"ten{i}"
            )

            sdt = st.text_input(
                "SĐT",
                key=f"sdt{i}"
            )

            songuoi = st.number_input(
                "Số người",
                min_value=1,
                value=1,
                key=f"nguoi{i}"
            )

        with c2:

            dien_cu = st.number_input(
                "Điện cũ",
                min_value=0,
                key=f"dc{i}"
            )

            dien_moi = st.number_input(
                "Điện mới",
                min_value=0,
                key=f"dm{i}"
            )

            nuoc_cu = st.number_input(
                "Nước cũ",
                min_value=0,
                key=f"nc{i}"
            )

            nuoc_moi = st.number_input(
                "Nước mới",
                min_value=0,
                key=f"nm{i}"
            )

        if dien_moi < dien_cu:
            st.error("❌ Chỉ số điện mới phải lớn hơn hoặc bằng điện cũ.")

        if nuoc_moi < nuoc_cu:
            st.error("❌ Chỉ số nước mới phải lớn hơn hoặc bằng nước cũ.")

        so_dien = max(dien_moi - dien_cu, 0)
        so_nuoc = max(nuoc_moi - nuoc_cu, 0)

        tien_dien = so_dien * gia_dien
        tien_nuoc = so_nuoc * gia_nuoc

        tong = (
            gia_phong
            + tien_dien
            + tien_nuoc
            + internet
            + rac
            + gui_xe
            + phu_phi
        )

        tong_day += tong
        tong_dien += so_dien
        tong_nuoc += so_nuoc

        ket_qua.append({
            "Phòng": i,
            "Người thuê": ten,
            "SĐT": sdt,
            "Số người": songuoi,
            "Điện tiêu thụ": so_dien,
            "Nước tiêu thụ": so_nuoc,
            "Tiền điện": tien_dien,
            "Tiền nước": tien_nuoc,
            "Tiền phòng": gia_phong,
            "Internet": internet,
            "Rác": rac,
            "Xe": gui_xe,
            "Phụ phí": phu_phi,
            "Tổng tiền": tong
        })

st.divider()

st.header("📊 BẢNG THỐNG KÊ")

df = pd.DataFrame(ket_qua)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "💰 Tổng doanh thu",
    f"{tong_day:,.0f} VNĐ"
)

c2.metric(
    "⚡ Tổng điện",
    f"{tong_dien} kWh"
)

c3.metric(
    "💧 Tổng nước",
    f"{tong_nuoc} m³"
)

st.divider()

csv = df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "📥 Xuất file CSV",
    csv,
    "BangTienPhong.csv",
    "text/csv"
)

st.success("✅ Hoàn thành bảng tính tiền phòng.")

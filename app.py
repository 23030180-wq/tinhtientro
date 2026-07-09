import streamlit as st
import pandas as pd

# ==========================================
# CẤU HÌNH TRANG
# ==========================================

st.set_page_config(
    page_title="Quản lý dãy phòng trọ",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 HỆ THỐNG QUẢN LÝ TIỀN PHÒNG TRỌ")
st.markdown("### Quản lý tiền phòng - điện - nước cho toàn bộ dãy phòng")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ CẤU HÌNH")

gia_phong = st.sidebar.number_input(
    "💰 Tiền phòng (VNĐ)",
    min_value=0,
    value=2500000,
    step=50000
)

gia_dien = st.sidebar.number_input(
    "⚡ Giá điện (VNĐ/kWh)",
    min_value=0,
    value=3500,
    step=100
)

gia_nuoc = st.sidebar.number_input(
    "💧 Giá nước (VNĐ/m³)",
    min_value=0,
    value=15000,
    step=500
)

internet = st.sidebar.number_input(
    "🌐 Internet",
    min_value=0,
    value=100000,
    step=10000
)

rac = st.sidebar.number_input(
    "🗑️ Tiền rác",
    min_value=0,
    value=30000,
    step=5000
)

gui_xe = st.sidebar.number_input(
    "🏍️ Tiền gửi xe",
    min_value=0,
    value=100000,
    step=10000
)

phu_phi = st.sidebar.number_input(
    "📦 Phụ phí khác",
    min_value=0,
    value=20000,
    step=5000
)

so_phong = st.sidebar.slider(
    "🏠 Số phòng",
    min_value=1,
    max_value=50,
    value=10
)

st.divider()

# ==========================================
# NHẬP CHỈ SỐ
# ==========================================

st.header("📋 NHẬP CHỈ SỐ ĐIỆN - NƯỚC")

ket_qua = []

tong_day = 0
tong_dien = 0
tong_nuoc = 0

for i in range(1, so_phong + 1):

    with st.expander(f"🏠 Phòng {i}", expanded=False):

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            dien_cu = st.number_input(
                "Điện cũ",
                min_value=0,
                key=f"dc{i}"
            )

        with c2:
            dien_moi = st.number_input(
                "Điện mới",
                min_value=0,
                key=f"dm{i}"
            )

        with c3:
            nuoc_cu = st.number_input(
                "Nước cũ",
                min_value=0,
                key=f"nc{i}"
            )

        with c4:
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
            "Điện tiêu thụ": so_dien,
            "Nước tiêu thụ": so_nuoc,
            "Tiền điện (VNĐ)": tien_dien,
            "Tiền nước (VNĐ)": tien_nuoc,
            "Tiền phòng (VNĐ)": gia_phong,
            "Internet": internet,
            "Rác": rac,
            "Gửi xe": gui_xe,
            "Phụ phí": phu_phi,
            "TỔNG TIỀN (VNĐ)": tong
        })

# ==========================================
# BẢNG KẾT QUẢ
# ==========================================

st.divider()

st.header("📊 BẢNG TÍNH TIỀN")

df = pd.DataFrame(ket_qua)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# THỐNG KÊ
# ==========================================

st.divider()

st.header("📈 THỐNG KÊ")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Tổng doanh thu",
        f"{tong_day:,.0f} VNĐ"
    )

with col2:
    st.metric(
        "⚡ Tổng điện tiêu thụ",
        f"{tong_dien} kWh"
    )

with col3:
    st.metric(
        "💧 Tổng nước tiêu thụ",
        f"{tong_nuoc} m³"
    )

# ==========================================
# XUẤT FILE CSV
# ==========================================

st.divider()

csv = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 Xuất file CSV",
    data=csv,
    file_name="BangTienPhong.csv",
    mime="text/csv"
)

st.success("✅ Hoàn thành bảng tính tiền phòng.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Bảng điểm, xếp loại và thống kê kết quả học tập.")

data = {
    "Họ và tên": [
        "Nguyễn Văn An", "Trần Thị Bình", "Lê Văn Cường",
        "Phạm Thị Dung", "Hoàng Văn Em", "Vũ Thị Phượng",
        "Đỗ Văn Giang", "Bùi Thị Hoa", "Ngô Văn Hùng",
        "Dương Thị Lan"
    ],
    "Chuyên cần": [8.5, 9.0, 7.0, 10.0, 6.5, 8.0, 9.5, 7.5, 8.5, 9.0],
    "Giữa kỳ": [7.0, 8.5, 6.0, 9.0, 5.5, 7.5, 8.0, 6.5, 7.0, 8.5],
    "Cuối kỳ": [7.5, 8.0, 6.5, 9.5, 6.0, 7.0, 8.5, 7.0, 8.0, 9.0]
}

df = pd.DataFrame(data)

df["Tong_ket"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
).round(2)

bins = [-float("inf"), 5.0, 7.0, 8.5, float("inf")]
labels = ["Yếu", "Trung bình", "Khá", "Giỏi"]

df["Xếp loại"] = pd.cut(
    df["Tong_ket"],
    bins=bins,
    labels=labels,
    right=False
)

loai_chon = st.sidebar.multiselect(
    "Chọn xếp loại",
    options=labels,
    default=labels
)

df_hien_thi = df[df["Xếp loại"].isin(loai_chon)]

st.subheader("📊 Thống kê kết quả")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Tổng số sinh viên", len(df))
col2.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
col3.metric("Điểm cao nhất", f"{df['Tong_ket'].max():.2f}")
col4.metric("Số sinh viên đạt", f"{(df['Tong_ket'] >= 5).sum()}/10")

st.subheader("📋 Bảng điểm sinh viên")

st.dataframe(
    df_hien_thi.rename(columns={"Tong_ket": "Điểm tổng kết"}),
    use_container_width=True,
    hide_index=True
)

st.subheader("📈 Biểu đồ điểm tổng kết")

if not df_hien_thi.empty:
    fig, ax = plt.subplots(figsize=(12, 5))

    bars = ax.bar(
        df_hien_thi["Họ và tên"],
        df_hien_thi["Tong_ket"]
    )

    ax.set_title("Điểm tổng kết của sinh viên")
    ax.set_xlabel("Họ và tên")
    ax.set_ylabel("Điểm")
    ax.set_ylim(0, 10)
    ax.tick_params(axis="x", rotation=35)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h:.2f}",
            (bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center"
        )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("Không có sinh viên thuộc xếp loại đã chọn.")

st.subheader("📌 Số lượng theo xếp loại")

dem_xep_loai = df["Xếp loại"].value_counts().reindex(
    labels, fill_value=0
)

st.bar_chart(dem_xep_loai)

st.caption(
    "Công thức: 20% chuyên cần + 30% giữa kỳ + 50% cuối kỳ."
)

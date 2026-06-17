# app.py

import streamlit as st
import pandas as pd

from database import (
    init_db,
    get_all_transactions,
    get_finance_summary,
    get_database_debug_info
)

from transaction_manager import save_transaction
from transaction_classifier import classify_transaction
from finance_agent import ask_finance_agent
from saving_advisor import get_extra_finance_analysis


st.set_page_config(
    page_title="AI Agent phân tích tài chính cá nhân",
    page_icon="💰",
    layout="wide"
)


# Ẩn biểu tượng trạng thái mặc định góc trên của Streamlit,
# nhưng vẫn giữ được st.spinner trong nội dung trang.
st.markdown(
    """
    <style>
    div[data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container {
        padding-top: 2rem;
    }

    .summary-card {
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(120, 120, 120, 0.25);
        background-color: rgba(120, 120, 120, 0.08);
        margin-bottom: 10px;
    }

    .summary-title {
        font-size: 14px;
        opacity: 0.75;
        margin-bottom: 4px;
    }

    .summary-value {
        font-size: 22px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


init_db()


def format_money(value):
    try:
        return f"{float(value):,.0f} VND"
    except Exception:
        return "0 VND"


def render_money_card(title, value):
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-title">{title}</div>
            <div class="summary-value">{format_money(value)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


left_col, right_col = st.columns([1.15, 1])


# =========================
# CỘT TRÁI: QUẢN LÝ THU CHI
# =========================
with left_col:
    st.subheader("1. Quản lý thu chi")

    with st.expander("Kiểm tra database đang dùng"):
        debug_info = get_database_debug_info()
        st.write("Database:", debug_info["database"])
        st.write("Các bảng:", debug_info["tables"])
        st.write("Cột bảng transactions:", debug_info["transactions_columns"])

    with st.form("transaction_form", clear_on_submit=True):
        trans_date = st.date_input("Ngày giao dịch")

        trans_type = st.selectbox(
            "Loại giao dịch",
            ["Chi", "Thu"]
        )

        amount = st.number_input(
            "Số tiền",
            min_value=0.0,
            step=1000.0,
            format="%.0f"
        )

        auto_classify = st.checkbox(
            "Tự động phân loại bằng AI",
            value=True
        )

        manual_category = st.selectbox(
            "Danh mục",
            [
                "",
                "Ăn uống",
                "Di chuyển",
                "Học tập",
                "Nhà ở",
                "Mua sắm",
                "Giải trí",
                "Sức khỏe",
                "Thu nhập",
                "Khác"
            ]
        )

        description = st.text_input(
            "Ghi chú thêm",
            placeholder="Ví dụ: ăn sáng, đổ xăng, mua sách..."
        )

        submitted = st.form_submit_button("Lưu giao dịch")

    if submitted:
        if auto_classify:
            category = classify_transaction(description, trans_type)
        else:
            category = manual_category if manual_category else "Khác"

        success, messages = save_transaction(
            trans_date=trans_date,
            trans_type=trans_type,
            amount=amount,
            description=description,
            category=category
        )

        if success:
            st.success(messages[0])
            st.info(f"Giao dịch được phân loại vào danh mục: **{category}**")
            st.rerun()
        else:
            for msg in messages:
                st.error(msg)


# =========================
# CỘT PHẢI: TÓM TẮT + AI
# =========================
with right_col:
    st.subheader("2. Tóm tắt tài chính")

    summary = get_finance_summary()

    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        render_money_card("Tổng thu", summary["total_income"])

    with card_col2:
        render_money_card("Tổng chi", summary["total_expense"])

    with card_col3:
        render_money_card("Số dư", summary["balance"])

    st.divider()

    st.subheader("3. AI Agent tài chính")

    user_question = st.text_area(
        "Nhập câu hỏi của bạn",
        placeholder="Ví dụ: Tháng này tôi chi tiền cho danh mục nào nhiều nhất?",
        height=120
    )

    agent_btn_col1, agent_btn_col2, agent_btn_col3 = st.columns(3)

    with agent_btn_col1:
        ask_clicked = st.button("Hỏi AI Agent", use_container_width=True)

    with agent_btn_col2:
        suggest_clicked = st.button("Đề xuất tiết kiệm", use_container_width=True)

    with agent_btn_col3:
        anomaly_clicked = st.button("Phân tích bất thường", use_container_width=True)

    if ask_clicked:
        with st.spinner("AI Agent đang phân tích câu hỏi..."):
            answer = ask_finance_agent(user_question)

        st.success("Câu trả lời")
        st.write(answer)

    if suggest_clicked:
        suggest_question = (
            "Hãy phân tích tình hình thu chi hiện tại của tôi và đề xuất "
            "cách tiết kiệm cụ thể, dễ thực hiện."
        )

        st.info(f"Câu hỏi tự động: {suggest_question}")

        with st.spinner("AI Agent đang đề xuất tiết kiệm..."):
            answer = ask_finance_agent(suggest_question)

        st.success("Kết quả đề xuất tiết kiệm")
        st.write(answer)

    if anomaly_clicked:
        anomaly_question = (
            "Hãy phát hiện các điểm bất thường hoặc rủi ro trong dữ liệu thu chi hiện tại của tôi."
        )

        st.info(f"Câu hỏi tự động: {anomaly_question}")

        with st.spinner("AI đang phân tích bất thường..."):
            answer = get_extra_finance_analysis(anomaly_question)

        st.success("Kết quả phân tích bất thường")
        st.write(answer)


st.divider()


# =========================
# DANH SÁCH GIAO DỊCH + LỌC + TỔNG
# =========================
st.subheader("4. Danh sách giao dịch và thống kê")

rows = get_all_transactions()

if rows:
    df = pd.DataFrame(
        rows,
        columns=["ID", "Ngày", "Loại", "Số tiền", "Ghi chú thêm", "Danh mục"]
    )

    df["Ngày"] = pd.to_datetime(df["Ngày"], errors="coerce")
    df["Số tiền"] = pd.to_numeric(df["Số tiền"], errors="coerce").fillna(0)

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        selected_types = st.multiselect(
            "Lọc theo loại",
            options=sorted(df["Loại"].dropna().unique().tolist()),
            default=sorted(df["Loại"].dropna().unique().tolist())
        )

    with filter_col2:
        selected_categories = st.multiselect(
            "Lọc theo danh mục",
            options=sorted(df["Danh mục"].dropna().unique().tolist()),
            default=sorted(df["Danh mục"].dropna().unique().tolist())
        )

    with filter_col3:
        min_date = df["Ngày"].min()
        max_date = df["Ngày"].max()

        if pd.isna(min_date) or pd.isna(max_date):
            date_range = None
        else:
            date_range = st.date_input(
                "Lọc theo ngày",
                value=(min_date.date(), max_date.date())
            )

    with filter_col4:
        keyword = st.text_input(
            "Tìm theo ghi chú",
            placeholder="Ví dụ: ăn, xăng, lương..."
        )

    filtered_df = df.copy()

    if selected_types:
        filtered_df = filtered_df[filtered_df["Loại"].isin(selected_types)]

    if selected_categories:
        filtered_df = filtered_df[filtered_df["Danh mục"].isin(selected_categories)]

    if date_range and isinstance(date_range, tuple) and len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])

        filtered_df = filtered_df[
            (filtered_df["Ngày"] >= start_date) &
            (filtered_df["Ngày"] <= end_date)
        ]

    if keyword.strip():
        filtered_df = filtered_df[
            filtered_df["Ghi chú thêm"]
            .astype(str)
            .str.lower()
            .str.contains(keyword.strip().lower(), na=False)
        ]

    total_income_filtered = filtered_df.loc[
        filtered_df["Loại"] == "Thu", "Số tiền"
    ].sum()

    total_expense_filtered = filtered_df.loc[
        filtered_df["Loại"] == "Chi", "Số tiền"
    ].sum()

    balance_filtered = total_income_filtered - total_expense_filtered

    total_col1, total_col2, total_col3, total_col4 = st.columns(4)

    with total_col1:
        st.metric("Số giao dịch sau lọc", len(filtered_df))

    with total_col2:
        st.metric("Tổng thu sau lọc", format_money(total_income_filtered))

    with total_col3:
        st.metric("Tổng chi sau lọc", format_money(total_expense_filtered))

    with total_col4:
        st.metric("Chênh lệch sau lọc", format_money(balance_filtered))

    st.divider()

    table_col, category_col = st.columns([1.35, 0.8])

    with table_col:
        display_df = filtered_df.copy()

        if not display_df.empty:
            display_df["Ngày"] = display_df["Ngày"].dt.strftime("%Y-%m-%d")
            display_df["Số tiền"] = display_df["Số tiền"].map(lambda x: f"{x:,.0f}")

        total_row = pd.DataFrame([{
            "ID": "",
            "Ngày": "",
            "Loại": "TỔNG",
            "Số tiền": f"{filtered_df['Số tiền'].sum():,.0f}",
            "Ghi chú thêm": "",
            "Danh mục": ""
        }])

        display_df = pd.concat([display_df, total_row], ignore_index=True)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    with category_col:
        st.markdown("### Chi theo danh mục")

        expense_df = filtered_df[filtered_df["Loại"] == "Chi"]

        if not expense_df.empty:
            category_summary = (
                expense_df
                .groupby("Danh mục", as_index=False)["Số tiền"]
                .sum()
                .sort_values("Số tiền", ascending=False)
            )

            category_summary["Số tiền"] = category_summary["Số tiền"].map(
                lambda x: f"{x:,.0f} VND"
            )

            st.dataframe(
                category_summary,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Không có dữ liệu chi tiêu trong bộ lọc hiện tại.")

else:
    st.info("Chưa có giao dịch nào.")
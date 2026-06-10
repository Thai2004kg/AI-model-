# app.py

import streamlit as st
import pandas as pd

from database import (
    init_db,
    get_all_transactions,
    get_finance_summary_text,
    get_database_debug_info
)

from transaction_manager import save_transaction
from transaction_classifier import classify_transaction
from saving_advisor import get_saving_advice, get_extra_finance_analysis


st.set_page_config(
    page_title="AI Agent phân tích tài chính cá nhân",
    page_icon="💰",
    layout="wide"
)


init_db()


st.title("💰 AI Agent phân tích tài chính cá nhân")

st.markdown("""
Hệ thống có 3 chức năng chính: **quản lý thu chi**, **phân loại giao dịch**, và **đề xuất tiết kiệm**.
""")


with st.expander("Kiểm tra database đang dùng"):
    debug_info = get_database_debug_info()
    st.write("Database:", debug_info["database"])
    st.write("Các bảng:", debug_info["tables"])
    st.write("Cột bảng transactions:", debug_info["transactions_columns"])


left_col, right_col = st.columns([1.2, 1])


with left_col:
    st.subheader("1. Quản lý thu chi")

    with st.form("transaction_form", clear_on_submit=True):
        trans_date = st.date_input("Ngày giao dịch")
        trans_type = st.selectbox("Loại giao dịch", ["Chi", "Thu"])
        amount = st.number_input("Số tiền", min_value=0.0, step=1000.0)
        description = st.text_input(
            "Mô tả giao dịch",
            placeholder="Ví dụ: ăn sáng, đổ xăng, mua sách..."
        )

        auto_classify = st.checkbox("Tự động phân loại bằng AI", value=True)

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
            st.info(f"AI phân loại giao dịch vào danh mục: **{category}**")
            st.rerun()
        else:
            for msg in messages:
                st.error(msg)

    st.divider()

    st.subheader("Danh sách giao dịch")

    rows = get_all_transactions()

    if rows:
        df = pd.DataFrame(
            rows,
            columns=["ID", "Ngày", "Loại", "Số tiền", "Mô tả", "Danh mục"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Chưa có giao dịch nào.")


with right_col:
    st.subheader("2. Tóm tắt tài chính")

    summary_text = get_finance_summary_text()
    st.text(summary_text)

    st.divider()

    st.subheader("3. Đề xuất tiết kiệm bằng AI")

    user_question = st.text_area(
        "Câu hỏi cho AI",
        placeholder="Ví dụ: Tháng này tôi chi tiêu có hợp lý không?",
        height=120
    )

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("Phân tích và đề xuất tiết kiệm"):
            with st.spinner("AI đang phân tích..."):
                advice = get_saving_advice(user_question)

            st.success("Kết quả phân tích")
            st.write(advice)

    with col_btn2:
        if st.button("Phân tích bất thường"):
            with st.spinner("AI đang kiểm tra bất thường..."):
                extra = get_extra_finance_analysis(user_question)

            st.success("Kết quả phân tích bất thường")
            st.write(extra)

    st.divider()

    st.markdown("""
### Mô hình AI sử dụng

Hệ thống sử dụng **6 mô hình AI local qua Ollama**, nhưng không gọi cả 6 mô hình cho mọi tác vụ.

- **Phân loại giao dịch**: Qwen AI + Phi AI
- **Đề xuất tiết kiệm**: Llama AI + Mistral AI
- **Phân tích bất thường**: Gemma AI + DeepSeek AI
- **Câu hỏi số liệu**: Python + SQLite

Các AI trong từng chức năng được gọi **song song** để giảm thời gian chờ.
""")
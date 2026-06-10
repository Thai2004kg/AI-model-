# transaction_manager.py

from database import add_transaction


def validate_transaction(trans_date, trans_type, amount, description):
    errors = []

    if not trans_date:
        errors.append("Thiếu ngày giao dịch.")

    if not trans_type:
        errors.append("Thiếu loại giao dịch.")

    if amount is None or amount <= 0:
        errors.append("Số tiền phải lớn hơn 0.")

    if not description or description.strip() == "":
        errors.append("Thiếu mô tả giao dịch.")

    return errors


def save_transaction(trans_date, trans_type, amount, description, category):
    errors = validate_transaction(trans_date, trans_type, amount, description)

    if errors:
        return False, errors

    add_transaction(
        trans_date=str(trans_date),
        trans_type=trans_type,
        amount=float(amount),
        description=description.strip(),
        category=category
    )

    return True, ["Lưu giao dịch thành công."]
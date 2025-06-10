def validate_transfer_payload(payload):
    required_fields = ['sender_email', 'receiver_email', 'payment_method', 'amount']
    for field in required_fields:
        if field not in payload:
            return False, f"{field} wajib diisi"
    if not isinstance(payload['amount'], (int, float)) or payload['amount'] <= 0:
        return False, "Jumlah transfer harus lebih dari 0"
    return True, ""
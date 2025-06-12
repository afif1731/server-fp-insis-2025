from donttrust import DontTrust, Schema

def validate_transfer_payload(payload):
    required_fields = ['sender_email', 'receiver_email', 'payment_method', 'amount']
    for field in required_fields:
        if field not in payload:
            return False, f"{field} wajib diisi"
    if not isinstance(payload['amount'], (int, float)) or payload['amount'] <= 0:
        return False, "Jumlah transfer harus lebih dari 0"
    return True, ""

transferBalanceValidator = DontTrust(
    sender_email=Schema().string().required().strip(),
    receiver_payment_method=Schema().string().required().allow('dopay', 'owo', 'ringaja'),
    receiver_email=Schema().string().required().strip(),
    amount=Schema().number().required().min(0)
    )
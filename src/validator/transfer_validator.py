from donttrust import DontTrust, Schema

transferBalanceValidator = DontTrust(
    sender_email=Schema().string().required().strip(),
    receiver_payment_method=Schema().string().required().allow('dopay', 'owo', 'ringaja'),
    receiver_email=Schema().string().required().strip(),
    amount=Schema().number().required().min(0)
    )

askBalanceValidator = DontTrust(
    email=Schema().string().required()
    )
from donttrust import DontTrust, Schema

getProductByIdValidator = DontTrust(
    product_id=Schema().string().required().strip()
)

buyProductValidator = DontTrust(buyer_email=Schema().string().required().strip(),
                                payment_method=Schema().string().required().allow('dopay', 'owo', 'ringaja'),
                                product_id=Schema().string().required(),
                                quantity=Schema().number().min(1).required()
                                )
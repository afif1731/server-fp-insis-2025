from donttrust import DontTrust, Schema

getProductByIdValidator = DontTrust(
    product_id=Schema().string().required().strip()
)
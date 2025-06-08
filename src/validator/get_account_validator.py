from donttrust import DontTrust, Schema

getAccountValidator = DontTrust(email=Schema().string().required().strip())

getWalletValidator = DontTrust(email=Schema().string().required().strip(),
                               payment_method=Schema().string().required()
                               )
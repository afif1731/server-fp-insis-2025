from src.config.prisma_config import prisma
from src.utils.hashing import hash_pass
import asyncio
import csv

async def users():
  print('🚶 Account Seeder')
  with open('./prisma/seeder_data/accounts.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    mydict = [row for row in reader]
    for user in mydict:
      user_pass = await hash_pass(user['password'])

      await prisma.accounts.upsert(
        where={'id': user['id']},
        data={
          'create': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'password': user_pass.decode('utf-8'),
            'role': user['role'],
          },
          'update': {
            'email': user['email'],
            'name': user['name'],
            'password': user_pass.decode('utf-8'),
            'role': user['role'],
          }
        }
      )
  print('✅ Success!')

async def payment_method():
  print('💸 Payment Method Seeder')
  with open('./prisma/seeder_data/payment_methods.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    mydict = [row for row in reader]
    for payment_method in mydict:
      await prisma.paymentmethods.upsert(
        where={'id': payment_method['id']},
        data={
            'create': {
            'id': payment_method['id'],
            'payment_name': payment_method['name'],
            'payment_slug': payment_method['slug'],
          },
          'update': {
            'payment_name': payment_method['name'],
            'payment_slug': payment_method['slug'],
          }
        }
      )
  print('✅ Success!')

async def user_wallet():
  print('👝 User Wallet Seeder')
  with open('./prisma/seeder_data/user_wallets.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    mydict = [row for row in reader]
    for user_wallet in mydict:
      await prisma.userwallets.upsert(
        where={'id': user_wallet['id']},
        data={
            'create': {
            'id': user_wallet['id'],
            'wallet_name': user_wallet['wallet_name'],
            'account_id': user_wallet['account_id'],
            'payment_method_slug': user_wallet['payment_method_slug'],
            'balance': int(user_wallet['balance']),
          },
          'update': {
            'wallet_name': user_wallet['wallet_name'],
            'account_id': user_wallet['account_id'],
            'payment_method_slug': user_wallet['payment_method_slug'],
            'balance': int(user_wallet['balance']),
          }
        }
      )
  print('✅ Success!')

async def shop_product():
  print('🛒 Shop Product Seeder')
  with open('./prisma/seeder_data/shop_products.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    mydict = [row for row in reader]
    for product in mydict:
      await prisma.shopproducts.upsert(
        where={'id': product['id']},
        data={
            'create': {
            'id': product['id'],
            'name': product['name'],
            'image_url': product['image_url'],
            'price': int(product['price']),
            'quantity': int(product['quantity']),
          },
          'update': {
            'name': product['name'],
            'image_url': product['image_url'],
            'price': int(product['price']),
            'quantity': int(product['quantity']),
          }
        }
      )
  print('✅ Success!')

async def wallet_transactions():
  print('💰 Wallet Transactions Seeder')
  with open('./prisma/seeder_data/wallet_transactions.csv', mode='r') as infile:
    reader = csv.DictReader(infile)
    mydict = [row for row in reader]
    for transaction in mydict:
      await prisma.wallettransactions.upsert(
        where={'id': transaction['id']},
        data={
            'create': {
            'id': transaction['id'],
            'transaction_type': transaction['transaction_type'],
            'description': transaction['description'],
            'balance_change': int(transaction['balance_change']),
            'user_wallet_id': transaction['user_wallet_id'],
          },
          'update': {
            'transaction_type': transaction['transaction_type'],
            'description': transaction['description'],
            'balance_change': int(transaction['balance_change']),
            'user_wallet_id': transaction['user_wallet_id'],
          }
        }
      )
  print('✅ Success!')

async def main():
    await prisma.connect()
    print('🕐 Starting the Seeder...')
    await users()
    await payment_method()
    await user_wallet()
    await shop_product()
    await wallet_transactions()
    print('💫 All Done!')
    await prisma.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
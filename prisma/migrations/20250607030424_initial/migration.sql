-- CreateEnum
CREATE TYPE "AccountRole" AS ENUM ('USER', 'ADMIN');

-- CreateEnum
CREATE TYPE "TransactionType" AS ENUM ('PURCHASE', 'TRANSFER', 'AUCTION');

-- CreateTable
CREATE TABLE "Accounts" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "role" "AccountRole" NOT NULL DEFAULT 'USER',
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Accounts_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PaymentMethods" (
    "id" TEXT NOT NULL,
    "payment_name" TEXT NOT NULL,
    "payment_slug" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "PaymentMethods_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "UserWallets" (
    "id" TEXT NOT NULL,
    "wallet_name" TEXT NOT NULL,
    "balance" INTEGER NOT NULL DEFAULT 100000,
    "account_id" TEXT NOT NULL,
    "payment_method_slug" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "UserWallets_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "WalletTransactions" (
    "id" TEXT NOT NULL,
    "transaction_type" "TransactionType" NOT NULL,
    "description" TEXT NOT NULL,
    "balance_change" INTEGER NOT NULL,
    "user_wallet_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "WalletTransactions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ShopProducts" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "image_url" TEXT NOT NULL,
    "price" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ShopProducts_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ShopTransactions" (
    "id" TEXT NOT NULL,
    "item_quantity" INTEGER NOT NULL,
    "total_price" INTEGER NOT NULL,
    "user_wallet_id" TEXT NOT NULL,
    "product_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ShopTransactions_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Accounts_email_key" ON "Accounts"("email");

-- CreateIndex
CREATE UNIQUE INDEX "PaymentMethods_payment_slug_key" ON "PaymentMethods"("payment_slug");

-- CreateIndex
CREATE UNIQUE INDEX "UserWallets_account_id_payment_method_slug_key" ON "UserWallets"("account_id", "payment_method_slug");

-- AddForeignKey
ALTER TABLE "UserWallets" ADD CONSTRAINT "UserWallets_account_id_fkey" FOREIGN KEY ("account_id") REFERENCES "Accounts"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "UserWallets" ADD CONSTRAINT "UserWallets_payment_method_slug_fkey" FOREIGN KEY ("payment_method_slug") REFERENCES "PaymentMethods"("payment_slug") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "WalletTransactions" ADD CONSTRAINT "WalletTransactions_user_wallet_id_fkey" FOREIGN KEY ("user_wallet_id") REFERENCES "UserWallets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ShopTransactions" ADD CONSTRAINT "ShopTransactions_user_wallet_id_fkey" FOREIGN KEY ("user_wallet_id") REFERENCES "UserWallets"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ShopTransactions" ADD CONSTRAINT "ShopTransactions_product_id_fkey" FOREIGN KEY ("product_id") REFERENCES "ShopProducts"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

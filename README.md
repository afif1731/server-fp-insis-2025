# BankIT

## Prerequisites

- uv
- npm

### Installation

```bash
uv sync
npm install prisma -g
```

### Run Docker for Database
```
docker compose up -d
```

### Migrate Database
```
prisma migrate dev --schema ./prisma/schema.prisma
```

### Use Data Seeder
```
python .\seeder.py
```

### Run Server
```
python .\main.py
```

## Penjelasan Direktori

- `main.py`: File utama, setelah selesai membuat logic di service dan controller, tambahkan topic yang akan di-subscribe ke file ini.
- `controller`: Bagian untuk mengolah topic dan validasi payload
- `service`: Logic utama untuk meng-handle request yang masuk
- `middleware`: Bukan middleware pada umumnya, tapi untuk membuat error dan response, gunakan class yang ada di `custom_error.py` dan `custom_response.py`
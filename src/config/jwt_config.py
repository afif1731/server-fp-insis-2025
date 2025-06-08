from dotenv import load_dotenv
import os

load_dotenv()

JWT = {
    'secret': os.getenv('JWT_SECRET', 'B-%YBx8Axbr@57En@eHXue9Tg$Prf*,RAJ8+$i/W9$:ZR#m)=[uGGLD[XMiy+X)?XTm5qj-ZCZ)vHuT]Wr6L'),
    'method': 'HS256',
    'duration': (24 * 60 * 60)
}
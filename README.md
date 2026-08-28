# RDP_CRACK
یک کرکر همه کاره

نصب پیش‌نیازها (یک بار)

sudo apt update && sudo apt install -y hydra nmap crowbar ssh-audit

ذخیره اسکریپت

nano vpcrack_nullactive.py


مثال های کاربردی: 

# کرک کامل تمام پورت‌ها
python3 vpcrack_nullactive.py 192.168.1.100

# کرک سریع (فقط پورت‌های معروف)
python3 vpcrack_nullactive.py 192.168.1.100 --quick

# کرک با وردلیست اختصاصی و ۸ ترد
python3 vpcrack_nullactive.py example.com -w rockyou.txt -t 8

# نمایش نسخه
python3 vpcrack_nullactive.py --version


سرویس	پورت	توضیح
🪟 RDP	3389	کرک ویندوز ریموت دسکتاپ
🪟 SMB	445	کرک اشتراک فایل ویندوز
🪟 WinRM	5985	ریموت مدیریت ویندوز
🪟 MSSQL	1433	کرک دیتابیس مایکروسافت
🐧 SSH	22	کرک شل لینوکس
🐧 MySQL	3306	کرک دیتابیس مایاِسکیوال
🐧 PostgreSQL	5432	کرک پستگرس
🐧 Redis	6379	کرک ردیس بدون پسورد
🐧 MongoDB	27017	کرک مونگو
🖥️ VNC	5900	کرک دسکتاپ از راه دور
📂 FTP	21	کرک افتی‌پی

هر سوالی داشتین تلگرام در خدمتم
@Net_activenull

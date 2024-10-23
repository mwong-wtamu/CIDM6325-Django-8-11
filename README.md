# CIDM 6325 - Fall 2024 - Chapter 8 - 11

To Run this Project:
RabbitMQ
docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
http://127.0.0.1:15672/

Celery
pip install gevent
celery -A myshop worker --loglevel=info -P gevent

Monitor Celery
celery -A myshop flower
http://localhost:5555/

Enable Stripe
stripe.exe listen --forward-to 127.0.0.1:8000/payment/webhook/

Run Webserver
python manage.py runserver

WeasyPrint Installation
    1) Download https://www.msys2.org/#installation
    2) Run command in MSYS2 MSYS
        a. pacman -S mingw-w64-x86_64-pango
    3) Set Environment Variable
        ○ Command Prompt
            § SET WEASYPRINT_DLL_DIRECTORIES=E:\msys64\mingw64\bin
        ○ PowerShell
            § $Env:WEASYPRINT_DLL_DIRECTORIES="E:\msys64\mingw64\bin"
    4) Download https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
    5) Verify Path for GTK3
        a. Powershell 
            i. $Env:PATH
        b. Example Output
            i. C:\Program Files\GTK3-Runtime Win64\bin
    6) Restart Visual Studio
    7) Open Bash in Terminal
    8) Run in Virtual Environment
        a. pip install weasyprint
        b. Verify Weasyprint works
            i. weasyprint --info
            ii. Example:
            System: Windows
            Machine: AMD64
            Version: 10.0.22631
            Release: 11
            
            WeasyPrint version: 62.3
            Python version: 3.12.5
            Pydyf version: 0.11.0
            Pango version: 15003

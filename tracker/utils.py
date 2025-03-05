# myapp/utils.py
import time
import threading
import requests
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import PriceAlert

def convert_price(price_str):
    # Remove currency symbols and commas, then convert to float
    return float(price_str.replace('₹', '').replace(',', '').strip())

def fetch_product_data(product_url):
    # Example POST request to your Django view to fetch product data
    try:
        response = requests.post("http://127.0.0.1:8000/get_product_data/", json={'product_url': product_url})
        response.raise_for_status()  # Raise an exception if the request failed
        data = response.json()
        return data.get("price")  # Assuming the view returns JSON with a "price" field
    except requests.RequestException as e:
        print(f"[BG-Thread]Error fetching data for {product_url}: {e}")
        return None

def check_product_alerts():
    alerts = PriceAlert.objects.filter(is_active=True, alert_sent=False)
    for alert in alerts:
        current_price = fetch_product_data(alert.product_url)  # Fetch price using POST request
        current_price = convert_price(current_price)
        if current_price is not None and float(current_price) <= float(alert.desired_price):
            # Render email template with context data
            product_name_limited = ' '.join(alert.product_name.split()[:4])
            context = {
                'username': alert.user.username,
                'product_name': alert.product_name,
                'product_image_url': alert.product_image_url,
                'desired_price': alert.desired_price,
                'product_url': alert.product_url,
            }
            email_body = render_to_string('mail_template.html', context)

            # Send the email
            send_mail(
                subject=f"Price Drop Alert for {product_name_limited}",
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[alert.user.email],
                html_message=email_body,
            )

            # Mark the alert as sent
            alert.alert_sent = True
            print(f"[BG-Thread] Sent mail to {alert.user.username}")
            alert.save()

def price_check_loop():
    while True: 
        check_product_alerts()
        time.sleep(60)  # Check every 30 minutes

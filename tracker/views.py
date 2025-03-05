from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import json
import re
from django.contrib import messages
from .models import PriceAlert

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('add_product')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def search_product(search_value):
    # Step 1: Trim and replace parts of the search URL
    search_value = search_value.strip()
    search_value = search_value.replace('http://', ' http://')
    search_value = search_value.replace('https://', ' https://')
    search_value = search_value.replace('https://dl.flipkart.com', ' http://dl.flipkart.com')

    # Step 2: Validate the search value length
    if len(search_value) == 0:
        print("Please search something!")
        return

    # Step 3: Remove trailing '=' from search value
    while len(search_value) > 1 and search_value[-1] == '=':
        search_value = search_value[:-1]

    # Step 4: Extract URLs from the search value using regex
    matches = re.findall(r'\bhttps?:\/\/\S+', search_value)
    if matches:
        # Step 5: Prepare data for POST request
        product_url = matches[0]        
        # Step 6: Send the POST request to the API
        response = requests.post(
            "https://pricehistory.app/api/search",
            headers={'Content-Type': 'application/json'},
            json={'url': product_url}
        )

        # Step 7: Handle response
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                # Redirect logic can be handled based on the response data
                redirect_url = f"https://pricehistory.app/p/{data['code']}"
                return redirect_url
            else:
                return f"Error: {data['message']}"
        else:
            return "Sorry, something went wrong!"
    else:
        # If no URLs are found, handle fallback search
        fallback_search_url = f"https://pricehistory.app/page/search#gsc.tab=0&gsc.q={search_value}"
        print('returned fallbacckk url')
        return fallback_search_url


def convert_price(price_str):
    # Remove currency symbols and commas, then convert to float
    return float(price_str.replace('₹', '').replace(',', '').strip())

@csrf_exempt
@login_required
def create_alert(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_url = data.get('product_url')
            desired_price = data.get('desired_price')
            product_image_url = data.get('product_image_url')
            product_name = data.get('product_name')

            # Create and save the PriceAlert instance
            price_alert = PriceAlert(
                user=request.user,  # Set the current logged-in user
                product_name = product_name,
                product_url=product_url,
                desired_price=desired_price,
                product_image_url=product_image_url
            )
            price_alert.save()

            return JsonResponse({'success': True, 'message': 'Price alert created successfully!'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


@csrf_exempt
def get_product_data(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the POST request
            data = json.loads(request.body)
            product_url = data.get('product_url', '').strip()
            # Clean and process the product URL as in your JavaScript logic
            url = search_product(product_url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text,'html.parser')
            product_name = soup.find('div', class_='col-lg-9 col-md-9 col-sm-8 col-8 ph-title my-0 pl-2 p-1').find('h1', class_='mb-0').get_text(strip=True)
            img_tag = soup.find('div', class_='ph-hero-image').find('img')['src']
            current_price = soup.find('div', class_='ph-pricing-pricing').get_text(strip=True)
            prediction = soup.find('div', class_='rating-scale row')
            highest_price = soup.find('div', class_='all-time-price-overview').find('div',class_='bg-danger').get_text(strip=True).split(':')[-1]
            average_price = soup.find('div', class_='all-time-price-overview').find('div',class_='bg-warning').get_text(strip=True).split(':')[-1]
            lowest_price = soup.find('div', class_='all-time-price-overview').find('div',class_='bg-info').get_text(strip=True).split(':')[-1]
            if prediction is not None:
                prediction = prediction.find('div',class_='active').get_text(strip=True)

            else:
                high_price = convert_price(highest_price)
                avg_price = convert_price(average_price)
                if avg_price < high_price * 0.9:  # 10% lower than highest price
                    prediction = "Buy"
                elif avg_price > high_price * 1.1:  # 10% higher than highest price
                    prediction = "Skip"
                elif avg_price >= high_price * 0.9 and avg_price <= highest_price:
                    prediction = "Wait"
                else:
                    prediction = "Okay"
            product_details = {
                'name' : product_name,
                'image' : img_tag,
                'price' : current_price,
                'highestPrice' : highest_price,
                'averagePrice' : average_price,
                'lowestPrice' : lowest_price,
                'scrape_url' : url,
                'prediction' : {
                    "text" : prediction,
                    "class" : f'prediction-{prediction.lower()}'
                }
            }
            return JsonResponse(product_details)
        except Exception as e:
            print("error : ",e)

def custom_logout(request):
    logout(request)  # Log out the user
    return render(request, 'logout.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add_product')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_product_view(request):
    username = request.user.username
    return render(request, 'add_product.html',{'username':username})

@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        errors = []
        if not username or not email:
            errors.append("Username and Email are required.")
        
        # Additional validation logic can be added here...

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            # Update the user object
            request.user.username = username
            request.user.email = email
            request.user.save()
            return JsonResponse({'success': True})

    return render(request, 'profile.html', {'user': request.user, 'messages': messages.get_messages(request)})

@login_required
def my_alerts_view(request):
    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        if alert_id:
            alert = get_object_or_404(PriceAlert, id=alert_id, user=request.user)
            alert.delete()
            # If you want to respond with a JSON message:
            return JsonResponse({'message': 'Alert deleted successfully.'})
        else:
            return JsonResponse({'error': 'Alert ID not provided.'}, status=400)

    # GET request: Fetch and render alerts
    alerts = PriceAlert.objects.filter(user=request.user)
    return render(request, 'my_alerts.html', {'alerts': alerts})
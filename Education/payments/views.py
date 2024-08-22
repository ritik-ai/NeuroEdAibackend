import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid

# This is your client ID and secret from PayPal
PAYPAL_CLIENT_ID = 'AStA9FjNdpV-w2xLeM3f8sqr1KbbAf3u2krqBsYGPDPpaiXHmdh3qMMoPhJNQD93cUVT8pSgl7q9Pv0O'
PAYPAL_SECRET = 'EM1dsOV846ija0PasyWW9mssi3o_mj9xhi0ogMbO7_5QEI2yxKe6gM4l4TwRTaJ0luJWwLVbe8Vm29yh'


def get_paypal_access_token():
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token',
                             headers={
                                 'Accept': 'application/json',
                                 'Accept-Language': 'en_US',
                             },
                             data={
                                 'grant_type': 'client_credentials'
                             },
                             auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET))
    response_data = response.json()
    return response_data.get('access_token')


@csrf_exempt
def create_paypal_product(request):
    if request.method == "POST":
        access_token = get_paypal_access_token()

        if not access_token:
            return JsonResponse({'error': 'Could not obtain PayPal access token'}, status=500)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'PayPal-Request-Id': str(uuid.uuid4()),
        }

        product_data = {
            "name": "Video Streaming Service",
            "description": "Video Streaming Service basic plan",
            "type": "SERVICE",
            "category": "SOFTWARE",
            "image_url": "https://example.com/streaming.jpg",
            "home_url": "https://example.com/home"
        }

        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/catalogs/products',
            headers=headers,
            json=product_data
        )

        if response.status_code == 201:
            product_id = response.json().get('id')

            if not product_id:
                return JsonResponse({'error': 'No product ID returned from PayPal'}, status=500)

            plan_data = {
                "product_id": product_id,
                "name": "Video Streaming Service Plan",
                "description": "Video Streaming Service basic plan",
                "status": "ACTIVE",
                "billing_cycles": [
                    {
                        "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                        "tenure_type": "REGULAR",
                        "sequence": 1,
                        "total_cycles": 0,  # 0 means infinite billing cycles until canceled
                        "pricing_scheme": {"fixed_price": {"value": "25", "currency_code": "USD"}}
                    }
                ],
                "payment_preferences": {
                    "auto_bill_outstanding": True,
                    "setup_fee": {"value": "0", "currency_code": "USD"},
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 3
                },
                "taxes": {"percentage": "10", "inclusive": False}
            }

            response = requests.post(
                'https://api-m.sandbox.paypal.com/v1/billing/plans',
                headers=headers,
                json=plan_data
            )

            if response.status_code == 201:
                return JsonResponse(response.json(), status=201)
            else:
                print(
                    f"Failed to create plan: {response.status_code}, {response.json()}")
                return JsonResponse(response.json(), status=response.status_code)
        else:
            print(
                f"Failed to create product: {response.status_code}, {response.json()}")
            return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_paypal_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plan_id = data.get('plan_id ')
        subscriber_email = data.get('subscriber_email')
        print("this is plan id",plan_id)

        access_token = get_paypal_access_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        subscription_data = {
            "plan_id": plan_id,
            "start_time": "2018-11-01T00:00:00Z",
            "quantity": "20",
            "shipping_amount": {
                "currency_code": "USD",
                "value": "10.00"
            },
            "subscriber": {
                "name": {
                    "given_name": "John",
                    "surname": "Doe"
                },
                "email_address": subscriber_email,
                "shipping_address": {
                    "name": {
                        "full_name": "John Doe"
                    },
                    "address": {
                        "address_line_1": "2211 N First Street",
                        "address_line_2": "Building 17",
                        "admin_area_2": "San Jose",
                        "admin_area_1": "CA",
                        "postal_code": "95131",
                        "country_code": "US"
                    }
                }
            },
            "application_context": {
                "brand_name": "walmart",
                "locale": "en-US",
                "shipping_preference": "SET_PROVIDED_ADDRESS",
                "user_action": "SUBSCRIBE_NOW",
                "payment_method": {
                    "payer_selected": "PAYPAL",
                    "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                },
                "return_url": "https://example.com/returnUrl",
                "cancel_url": "https://example.com/cancelUrl"
            }
        }

        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/subscriptions',
            headers=headers,
            json=subscription_data
        )

        if response.status_code == 201:
            return JsonResponse(response.json(), status=201)
        else:
            print(
                f"Failed to create subscription: {response.status_code}, {response.json()}")
            return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def paypal_webhook(request):
    if request.method == 'POST':
        webhook_event = json.loads(request.body)
        # Handle the webhook event here
        print(f"Received webhook: {webhook_event}")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_paypal_subscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
        subscriber_email = data.get('subscriber_email')

        access_token = get_paypal_access_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        subscription_data = {
            "plan_id": plan_id,
            "subscriber": {
                "email_address": subscriber_email
            },
            "application_context": {
                "brand_name": "Your Brand",
                "locale": "en-US",
                "shipping_preference": "SET_PROVIDED_ADDRESS",
                "user_action": "SUBSCRIBE_NOW",
                "return_url": "https://example.com/return",
                "cancel_url": "https://example.com/cancel"
            }
        }

        response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/billing/subscriptions',
            headers=headers,
            json=subscription_data
        )

        # if response.status_code == 201:
        #     return JsonResponse(response.json(), status=201)
        # else:
        #     print(
        #         f"Failed to create subscription: {response.status_code}, {response.json()}")
        #     return JsonResponse(response.json(), status=response.status_code)


        if response.status_code == 201:
            subscription_response = response.json()
            approval_url = next(link['href'] for link in subscription_response['links'] if link['rel'] == 'approve')
            return JsonResponse({'approval_url': approval_url}, status=201)
        else:
            print(f"Failed to create subscription: {response.status_code}, {response.json()}")
            return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Invalid request method'}, status=405)















import json
import time
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from Order_Module.models import Order, OrderDetail
from Product_Module.models import Product

# Create your views here.

MERCHANT = 'test'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request: HttpRequest):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))

    if count < 0:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده نادرست میباشد',
            'icon': 'error',
            'confirm_button_text': 'باشه'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_order_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_order_detail.save()

            return JsonResponse({
                'status': 'success',
                'text': 'محصول موردنظر با موفقیت به سبد خرید شما اضافه شد',
                'icon': 'success',
                'confirm_button_text': 'باشه'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول موردنظر یافت نشد',
                'icon': 'error',
                'confirm_button_text': 'باشه'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزپدن به سبد خرید ابتدا باید وارد سایت شوید',
            'icon': 'error',
            'confirm_button_text': 'ورود به سایت'
        })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order_detail: OrderDetail = OrderDetail.objects.filter(
                    order_id=current_order.id, order__is_paid=False, order__user_id=request.user.id).first()
                order_detail.final_price = order_detail.product.price
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                return render(request, 'Order_Module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {str(req.json()["data"]["ref_id"])} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'Order_Module/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'Order_Module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'Order_Module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'Order_Module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from Account_Module.models import User
from Order_Module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePassForm


# Create your views here.


@method_decorator(login_required, 'dispatch')
class UserPanelDashboardView(TemplateView):
    template_name = 'User_Panel_Module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = User.objects.filter(id=request.user.id).first()
            edit_form = EditProfileModelForm(instance=current_user)
            context = {
                'edit_form': edit_form,
                'user': current_user
            }
            return render(request, 'User_Panel_Module/edit_profile_page.html', context)
        else:
            return redirect(reverse('home-page'))

    def post(self, request: HttpRequest):
        if request.user.is_authenticated:
            current_user = User.objects.filter(id=request.user.id).first()
            edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
            if edit_form.is_valid():
                edit_form.save(commit=True)
            context = {
                'edit_form': edit_form,
                'user': current_user
            }
            return render(request, 'User_Panel_Module/edit_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            change_form = ChangePassForm()
            context = {
                'change_pass_form': change_form
            }
            return render(request, 'User_Panel_Module/change_pass_page.html', context)

        else:
            return redirect(reverse('home-page'))

    def post(self, request):
        if request.user.is_authenticated:
            change_form = ChangePassForm(request.POST)
            if change_form.is_valid():
                current_user: User = User.objects.filter(id=request.user.id).first()
                if current_user.check_password(change_form.cleaned_data.get('current_password')):
                    current_user.set_password(change_form.cleaned_data.get('new_password'))
                    current_user.save()
                    logout(request)
                    return redirect(reverse('login_page'))
                else:
                    change_form.add_error('current_password', 'رمز عبور وارد شده اشتباه می باشد')
            context = {
                'change_pass_form': change_form
            }
            return render(request, 'User_Panel_Module/change_pass_page.html', context)
        else:
            return redirect(reverse('home-page'))


@method_decorator(login_required, 'dispatch')
class UserShoppingView(ListView):
    model = Order
    template_name = 'User_Panel_Module/user_shopping.html'
    context_object_name = 'user_shopping'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=self.request.user.id, is_paid=True)
        return queryset


@login_required
def user_panel_component(request):
    return render(request, 'User_Panel_Module/components/user_panel_menu_component.html')


@login_required
def user_basket(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'User_Panel_Module/user_basket.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('User_Panel_Module/user_basket_content.html', context)
    return JsonResponse({
        'status': 'success',
        'body': data
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_id_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                              order__user_id=request.user.id).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('User_Panel_Module/user_basket_content.html', context)
    return JsonResponse({
        'status': 'success',
        'body': data
    })


@login_required
def user_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')

    return render(request, 'User_Panel_Module/user_shopping_detail.html', {
        'order': order
    })

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView , View
from .models import Item, OrderItem , Order
from django.utils import timezone 
from .forms import CheckoutForm
# Create your views here.

def products(request):
    context ={
        'items' : Item.objects.all()
    }
    return render(request,'product.html', context)

@login_required
def pricing(request):
   
    return render(request,'pricing.html')
    
class checkoutView(View):
    def get(self, *args,**kwargs ):

        form =CheckoutForm()
        context ={
            'form':form
        }

        return render(self.request, 'checkout.html',context)

    def post(self, *args ,**kwargs):
        form =CheckoutForm(self.request.POST or None)
        if form.is_valid():
            print('the form is valid')
            return redirect('core:checkout')




class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'home.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user = self.request.user , ordered = False)
            context = {
                'object':order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request , 'you do not have an active order')
            return redirect('/')
        
        
    

class ItemDetailView(DetailView):
    model = Item
    template_name  = 'product.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item , created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This Item quanity was updated')
            return redirect('core:order-summary' )
        else:
            order.items.add(order_item)
            messages.info(request, 'This product is added to your cart')
            return redirect('core:order-summary')
                 
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This product is added to your cart')
        return redirect('core:order-summary' )
    
@login_required
def remove_from_cart(request , slug ):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
         user=request.user,
          ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False,
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'This product is removed from your cart')
            return redirect('core:order-summary')
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('core:product' )

       
    else:
        messages.info(request, 'you do not have a active order')
        return redirect('core:product' )
    




@login_required
def remove_single_item_from_cart(request , slug ):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
         user=request.user,
          ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user = request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)
            messages.info(request, 'This Item quanity was updated')
            return redirect('core:order-summary' )
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('core:product', slug=slug )

       
    else:
        messages.info(request, 'you do not have a active order')
        return redirect('core:product', slug=slug )
    
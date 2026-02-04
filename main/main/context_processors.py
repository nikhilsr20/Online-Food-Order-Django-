from authentication.models import Cart

from authentication.models import CurrAddress

def cart_length(request):
    if request.user.is_authenticated:
        return{
            'cartlength': Cart.objects.filter(user=request.user).count()
        }
    return {'cartlength' : 0}

def curradd(request):
    current = CurrAddress.objects.filter(user_id=request.user.id).first()
    curr_address = ""
    if current:
        curr_address = current.curraddress   # field, not object
        return {'curr': curr_address}
    return {'curr': ""}
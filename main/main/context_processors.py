from authentication.models import Cart



def cart_length(request):
    if request.user.is_authenticated:
        return{
            'cartlength': Cart.objects.filter(user=request.user).count()
        }
    return {'cartlength' : 0}
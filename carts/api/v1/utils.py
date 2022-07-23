from carts.models import Cart


class CartHelper:
    def __init__(self, *args, **kwargs):
        super(CartHelper, self).__init__(*args, **kwargs)

    @classmethod
    def get_current_cart(cls, user):
        """Get user current cart
        :param: user
        :return: cart
        """
        carts = user.carts.filter(step__in=['initial', 'pending'])
        if carts.exists():
            return carts.first()
        return Cart.objects.create(user=user)

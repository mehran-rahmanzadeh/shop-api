class CartHelper:
    def __init__(self, *args, **kwargs):
        super(CartHelper, self).__init__(*args, **kwargs)

    @classmethod
    def get_current_cart(cls, user):
        return user.carts.filter(step__in=['initial', 'pending']).first()

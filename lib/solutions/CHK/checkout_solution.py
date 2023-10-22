

# noinspection PyUnusedLocal
# skus = unicode string

"""
Our price table and offers:
+------+-------+----------------+
| Item | Price | Special offers |
+------+-------+----------------+
| A    | 50    | 3A for 130     |
| B    | 30    | 2B for 45      |
| C    | 20    |                |
| D    | 15    |                |
+------+-------+----------------+
"""

prices = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

specials = {
    "A": (3, 130),
    "B": (2, 45),
}


def apply_discounts(basket):
    """
    Return a reduced count of items in the basket, and the cost of what offers were applied
    :param basket:
    :return:
    """
    cost_of_discounted = []
    for code, count in basket.items():
        if code not in specials:
            continue
        required_items = specials[code][0]
        if count >= required_items:
            fits = count // required_items
            basket[code] = basket[code] - fits*required_items
            cost_of_discounted.append(fits*specials[code][1])
    return basket, cost_of_discounted


def checkout(skus):
    basket = {}
    # Remap to count
    for item in skus:
        basket[item] = basket.get(item, 0) + 1

    print(basket)
    # We have a count of the items, we need some way to define the special offers to apply the discord
    new_basket, discount_costs = apply_discounts(basket)
    print(new_basket, discount_costs)


print(checkout(["A", "A", "A", "B", "D", "B"]))
print(checkout(["A", "A", "A", "A", "A", "A", "A", "B", "D"]))







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
    for code, count in basket.items():
        if code in specials and count >= specials[code][0]:
            print(count // specials[code][0])

def checkout(skus):
    basket = {}
    # Remap to count
    for item in skus:
        basket[item] = basket.get(item, 0) + 1

    # We have a count of the items, we need some way to define the special offers to apply the discord
    apply_discounts(basket)

    return basket

print(checkout(["A", "A", "A", "B", "D"]))
print(checkout(["A", "A", "A", "A", "A", "A", "A", "B", "D"]))




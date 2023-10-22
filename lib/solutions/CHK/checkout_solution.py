

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    basket = {}
    for item in skus:
        basket[item] = basket.get(item, 0) + 1
    return basket

print(checkout(["A", "A", "A", "B", "D"]))


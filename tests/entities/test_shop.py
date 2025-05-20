from cardwise.entities.Shop import Shop


def test_shop_creation():
    shop = Shop(name="Test Shop", category="Retail")
    assert shop.name == "Test Shop"
    assert shop.category == "Retail"


def test_shop_id_generation():
    shop = Shop(name="Test Shop")
    assert shop.id == "test_shop"


def test_shop_equality():
    shop1 = Shop(name="Test Shop")
    shop2 = Shop(name="Test Shop")
    shop3 = Shop(name="Another Shop")
    assert shop1 == shop2
    assert shop1 != shop3

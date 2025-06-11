from cardwise.domain.models.bank import Bank


def test_bank_info_creation():
    bank_info = Bank(name="Test Bank")
    assert bank_info.name == "Test Bank"
    assert bank_info.id == "test_bank"

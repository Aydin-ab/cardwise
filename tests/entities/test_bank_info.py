from cardwise.entities.BankInfo import BankInfo


def test_bank_info_creation():
    bank_info = BankInfo(name="Test Bank", bank_id="123", website="https://testbank.com")
    assert bank_info.name == "Test Bank"
    assert bank_info.bank_id == "123"
    assert bank_info.website == "https://testbank.com"


def test_bank_info_optional_fields():
    bank_info = BankInfo(name="Test Bank")
    assert bank_info.name == "Test Bank"
    assert bank_info.bank_id is None
    assert bank_info.website is None

class Shop {
  final String id;
  final String name;

  Shop({required this.id, required this.name});

  factory Shop.fromJson(Map<String, dynamic> json) {
    return Shop(
      id: json['id'],
      name: json['name'],
    );
  }
}

class Bank {
  final String id;
  final String name;

  Bank({required this.id, required this.name});

  factory Bank.fromJson(Map<String, dynamic> json) {
    return Bank(
      id: json['id'],
      name: json['name'],
    );
  }
}

class Offer {
  final String id;
  final Shop shop;
  final Bank bank;
  final String offerType;
  final String description;
  final String? expiryDate;

  Offer({
    required this.id,
    required this.shop,
    required this.bank,
    required this.offerType,
    required this.description,
    required this.expiryDate,
  });

  factory Offer.fromJson(Map<String, dynamic> json) {
    return Offer(
      id: json['id'],
      shop: Shop.fromJson(json['shop']),
      bank: Bank.fromJson(json['bank']),
      offerType: json['offer_type'],
      description: json['description'],
      expiryDate: json['expiry_date'], // may be null
    );
  }
}

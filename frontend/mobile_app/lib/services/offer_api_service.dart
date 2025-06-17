import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/offer.dart';

class OfferApiService {
  // Use emulator-friendly localhost address
  final String baseUrl = "https://cardwise-backend-api.onrender.com";

  Future<List<Offer>> searchOffers(String shopName) async {
    final response = await http.get(
      Uri.parse("$baseUrl/offers/search/?shops=${Uri.encodeQueryComponent(shopName)}"),
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList.map((e) => Offer.fromJson(e)).toList();
    } else {
      throw Exception("Failed to load offers: ${response.statusCode}");
    }
  }

  Future<List<Offer>> searchMultipleOffers(List<String> shopNames) async {
    final allOffers = <Offer>[];

    for (final name in shopNames) {
      try {
        final response = await http.get(
          Uri.parse("$baseUrl/offers/search?shops=${Uri.encodeQueryComponent(name)}"),
        );
        if (response.statusCode == 200) {
          final List<dynamic> jsonList = jsonDecode(response.body);
          final offers = jsonList.map((e) => Offer.fromJson(e)).toList();
          allOffers.addAll(offers);
        }
      } catch (e) {
        // Optional: log error per shop
      }
    }

    return allOffers;
  }


  Future<List<Offer>> getAllOffers() async {
    final response = await http.get(Uri.parse("$baseUrl/offers/all"));

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);
      return jsonList.map((e) => Offer.fromJson(e)).toList();
    } else {
      throw Exception("Failed to load all offers: ${response.statusCode}");
    }
  }
}

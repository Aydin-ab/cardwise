import 'package:flutter/material.dart';
import '../models/offer.dart';
import '../services/offer_api_service.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _textController = TextEditingController();
  final OfferApiService _apiService = OfferApiService();

  List<String> _shopNames = [];
  Future<List<Offer>>? _futureOffers;

  void _addShopName(String name) {
    final trimmed = name.trim();
    if (trimmed.isNotEmpty && !_shopNames.contains(trimmed)) {
      setState(() {
        _shopNames.add(trimmed);
      });
    }
    _textController.clear();
  }

  void _removeShopName(String name) {
    setState(() {
      _shopNames.remove(name);
    });
  }

  void _searchOffers() {
    if (_shopNames.isEmpty) return;

    setState(() {
      _futureOffers = _apiService.searchMultipleOffers(_shopNames);
    });
  }

void _showAllOffers() {
  setState(() {
    _futureOffers = _apiService.getAllOffers();
  });
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Search your credit cards offers")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Chips display
            Wrap(
              spacing: 8,
              runSpacing: 4,
              children: _shopNames.map((name) {
                return InputChip(
                  label: Text(name),
                  onDeleted: () => _removeShopName(name),
                );
              }).toList(),
            ),
            const SizedBox(height: 12),
            // Text input to add more
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: const InputDecoration(
                      labelText: "Add shop name",
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: _addShopName,
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: () => _addShopName(_textController.text),
                  child: const Text("Add"),
                ),
              ],
            ),
            const SizedBox(height: 16),
            // 🆕 Search & All Offers buttons
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _searchOffers,
                    icon: const Icon(Icons.search),
                    label: const Text("Search Offers"),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _showAllOffers,
                    icon: const Icon(Icons.list),
                    label: const Text("Show All Offers"),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: _futureOffers == null
                  ? const Center(child: Text("Add shop names to start searching"))
                  : FutureBuilder<List<Offer>>(
                      future: _futureOffers,
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return const Center(child: CircularProgressIndicator());
                        } else if (snapshot.hasError) {
                          return Center(
                            child: Text("Error: ${snapshot.error}",
                                style: const TextStyle(color: Colors.red)),
                          );
                        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                          return const Center(child: Text("No offers found."));
                        }

                        final offers = snapshot.data!;
                        return ListView.builder(
                          itemCount: offers.length,
                          itemBuilder: (context, index) {
                            final offer = offers[index];
                            return ListTile(
                              title: Text(offer.shop.name),
                              subtitle: Text("${offer.bank.name} • ${offer.description}"),
                              trailing: Text(offer.offerType),
                            );
                          },
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

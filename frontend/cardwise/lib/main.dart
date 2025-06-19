import 'package:flutter/material.dart';
import 'screens/search_screen.dart';

void main() {
  runApp(const CardwiseApp());
}

class CardwiseApp extends StatelessWidget {
  const CardwiseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cardwise',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const SearchScreen(),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cardwise/screens/search_screen.dart';

void main() {
  testWidgets('SearchScreen chip input behavior test', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(home: SearchScreen()));

    // Check initial state
    expect(find.text("Add shop name"), findsOneWidget);
    expect(find.text("Search Offers"), findsOneWidget);
    expect(find.byType(InputChip), findsNothing);

    // Enter "adidas" and tap "Add"
    await tester.enterText(find.byType(TextField), 'adidas');
    await tester.tap(find.text("Add"));
    await tester.pump();

    // Chip should appear
    expect(find.byType(InputChip), findsOneWidget);
    expect(find.text('adidas'), findsOneWidget);

    // Enter "shake shack" and tap "Add"
    await tester.enterText(find.byType(TextField), 'shake shack');
    await tester.tap(find.text("Add"));
    await tester.pump();

    expect(find.text('shake shack'), findsOneWidget);
    expect(find.byType(InputChip), findsNWidgets(2));

    // Remove the "adidas" chip
    final adidasDeleteIcon = find.byIcon(Icons.clear).first;
    await tester.tap(adidasDeleteIcon);
    await tester.pump();

    // Only one chip should remain
    expect(find.text('adidas'), findsNothing);
    expect(find.byType(InputChip), findsOneWidget);
  });
}

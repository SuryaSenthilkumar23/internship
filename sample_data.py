#!/usr/bin/env python3
"""
Sample Data Script for SML Isuzu Inventory Management System
This script adds sample inventory items and transactions for testing.
"""

import inventory
import transactions

def add_sample_data():
    """Add sample inventory items and transactions"""
    
    # Initialize databases
    inventory.init_db()
    transactions.init_transactions_db()
    
    # Sample inventory items
    sample_items = [
        {
            'name': 'Engine Oil 15W-40',
            'category': 'Lubricants',
            'quantity': 150,
            'reorder_level': 50,
            'cost_per_unit': 450.00
        },
        {
            'name': 'Brake Pad Set',
            'category': 'Brake System',
            'quantity': 25,
            'reorder_level': 10,
            'cost_per_unit': 2500.00
        },
        {
            'name': 'Air Filter',
            'category': 'Filters',
            'quantity': 8,
            'reorder_level': 15,
            'cost_per_unit': 850.00
        },
        {
            'name': 'Spark Plug Set',
            'category': 'Ignition',
            'quantity': 40,
            'reorder_level': 20,
            'cost_per_unit': 320.00
        },
        {
            'name': 'Clutch Plate',
            'category': 'Transmission',
            'quantity': 12,
            'reorder_level': 8,
            'cost_per_unit': 3200.00
        },
        {
            'name': 'Radiator Coolant',
            'category': 'Cooling System',
            'quantity': 75,
            'reorder_level': 30,
            'cost_per_unit': 180.00
        },
        {
            'name': 'Battery 12V',
            'category': 'Electrical',
            'quantity': 18,
            'reorder_level': 12,
            'cost_per_unit': 4500.00
        },
        {
            'name': 'Tire 195/65R15',
            'category': 'Tires',
            'quantity': 32,
            'reorder_level': 16,
            'cost_per_unit': 3800.00
        },
        {
            'name': 'Fuel Filter',
            'category': 'Filters',
            'quantity': 22,
            'reorder_level': 15,
            'cost_per_unit': 650.00
        },
        {
            'name': 'Headlight Bulb H4',
            'category': 'Lighting',
            'quantity': 60,
            'reorder_level': 25,
            'cost_per_unit': 450.00
        },
        {
            'name': 'Windshield Wipers',
            'category': 'Accessories',
            'quantity': 35,
            'reorder_level': 20,
            'cost_per_unit': 280.00
        },
        {
            'name': 'Seat Cover Set',
            'category': 'Interior',
            'quantity': 15,
            'reorder_level': 10,
            'cost_per_unit': 1200.00
        }
    ]
    
    print("Adding sample inventory items...")
    item_ids = []
    
    for item in sample_items:
        try:
            item_id = inventory.add_inventory_item(
                item['name'],
                item['category'],
                item['quantity'],
                item['reorder_level'],
                item['cost_per_unit']
            )
            item_ids.append(item_id)
            print(f"✓ Added: {item['name']}")
        except Exception as e:
            print(f"✗ Error adding {item['name']}: {e}")
    
    # Sample transactions
    sample_transactions = [
        {
            'item_id': 1,  # Engine Oil
            'transaction_type': 'incoming',
            'quantity': 50,
            'remarks': 'New stock received from supplier'
        },
        {
            'item_id': 2,  # Brake Pad Set
            'transaction_type': 'outgoing',
            'quantity': 5,
            'remarks': 'Sold to customer - Invoice #001'
        },
        {
            'item_id': 3,  # Air Filter
            'transaction_type': 'outgoing',
            'quantity': 12,
            'remarks': 'Service department usage'
        },
        {
            'item_id': 4,  # Spark Plug Set
            'transaction_type': 'incoming',
            'quantity': 20,
            'remarks': 'Emergency restock'
        },
        {
            'item_id': 5,  # Clutch Plate
            'transaction_type': 'outgoing',
            'quantity': 3,
            'remarks': 'Workshop repair job'
        },
        {
            'item_id': 6,  # Radiator Coolant
            'transaction_type': 'outgoing',
            'quantity': 25,
            'remarks': 'Bulk sale to dealer'
        },
        {
            'item_id': 7,  # Battery
            'transaction_type': 'incoming',
            'quantity': 10,
            'remarks': 'Monthly stock replenishment'
        },
        {
            'item_id': 8,  # Tire
            'transaction_type': 'outgoing',
            'quantity': 8,
            'remarks': 'Customer tire replacement'
        }
    ]
    
    print("\nAdding sample transactions...")
    
    for transaction in sample_transactions:
        try:
            transactions.add_transaction(
                transaction['item_id'],
                transaction['transaction_type'],
                transaction['quantity'],
                transaction['remarks']
            )
            print(f"✓ Added transaction: {transaction['transaction_type']} - {transaction['quantity']} units")
        except Exception as e:
            print(f"✗ Error adding transaction: {e}")
    
    print("\n" + "="*60)
    print("SAMPLE DATA ADDED SUCCESSFULLY!")
    print("="*60)
    
    # Show summary
    all_items = inventory.get_all_inventory()
    low_stock_items = inventory.get_low_stock_items()
    total_value = inventory.get_inventory_value()
    
    print(f"Total Items: {len(all_items)}")
    print(f"Low Stock Items: {len(low_stock_items)}")
    print(f"Total Inventory Value: ₹{total_value:,.2f}")
    
    if low_stock_items:
        print("\nLow Stock Alerts:")
        for item in low_stock_items:
            print(f"  - {item[0]} ({item[1]}): {item[2]} units (reorder at {item[3]})")
    
    print("\nYou can now run the application with: python app.py")
    print("Access the dashboard at: http://localhost:5000")

if __name__ == "__main__":
    add_sample_data()
import sqlite3
import os
from datetime import datetime

# Database configuration
DB_NAME = 'inventory.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            reorder_level INTEGER NOT NULL DEFAULT 0,
            cost_per_unit REAL NOT NULL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_inventory():
    """Get all inventory items with calculated values"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, category, quantity, reorder_level, cost_per_unit,
               (quantity * cost_per_unit) as total_value,
               CASE 
                   WHEN quantity <= reorder_level THEN 'low'
                   WHEN quantity <= reorder_level * 1.5 THEN 'medium'
                   ELSE 'high'
               END as stock_status
        FROM inventory
        ORDER BY name
    ''')
    
    items = cursor.fetchall()
    conn.close()
    
    return items

def get_inventory_by_id(item_id):
    """Get a specific inventory item by ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    
    return item

def add_inventory_item(name, category, quantity, reorder_level, cost_per_unit):
    """Add a new inventory item"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO inventory (name, category, quantity, reorder_level, cost_per_unit)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, quantity, reorder_level, cost_per_unit))
        
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("Item with this name already exists")

def update_inventory_item(item_id, name, category, quantity, reorder_level, cost_per_unit):
    """Update an existing inventory item"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE inventory 
        SET name = ?, category = ?, quantity = ?, reorder_level = ?, cost_per_unit = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (name, category, quantity, reorder_level, cost_per_unit, item_id))
    
    conn.commit()
    conn.close()

def update_stock(item_id, new_quantity):
    """Update stock quantity for an item"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE inventory 
        SET quantity = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_quantity, item_id))
    
    conn.commit()
    conn.close()

def get_low_stock_items():
    """Get items with low stock (quantity <= reorder_level)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, category, quantity, reorder_level
        FROM inventory
        WHERE quantity <= reorder_level
        ORDER BY quantity ASC
    ''')
    
    items = cursor.fetchall()
    conn.close()
    
    return items

def get_inventory_value():
    """Calculate total inventory value"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(quantity * cost_per_unit) FROM inventory')
    total = cursor.fetchone()[0]
    conn.close()
    
    return total if total else 0

def search_inventory(query):
    """Search inventory by name or category"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, category, quantity, reorder_level, cost_per_unit,
               (quantity * cost_per_unit) as total_value,
               CASE 
                   WHEN quantity <= reorder_level THEN 'low'
                   WHEN quantity <= reorder_level * 1.5 THEN 'medium'
                   ELSE 'high'
               END as stock_status
        FROM inventory
        WHERE name LIKE ? OR category LIKE ?
        ORDER BY name
    ''', (f'%{query}%', f'%{query}%'))
    
    items = cursor.fetchall()
    conn.close()
    
    return items

def get_categories():
    """Get all unique categories"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT category FROM inventory ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return categories
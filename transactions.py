import sqlite3
from datetime import datetime
from inventory import update_stock, get_inventory_by_id, DB_NAME

def init_transactions_db():
    """Initialize the transactions table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES inventory (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_transaction(item_id, transaction_type, quantity, remarks=""):
    """Add a new transaction and update inventory"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Get current inventory item
        item = get_inventory_by_id(item_id)
        if not item:
            raise ValueError("Item not found")
        
        current_quantity = item[3]  # quantity is at index 3
        
        # Calculate new quantity based on transaction type
        if transaction_type == 'incoming':
            new_quantity = current_quantity + quantity
        elif transaction_type == 'outgoing':
            new_quantity = current_quantity - quantity
            if new_quantity < 0:
                raise ValueError("Insufficient stock")
        else:
            raise ValueError("Invalid transaction type")
        
        # Add transaction record
        cursor.execute('''
            INSERT INTO transactions (item_id, transaction_type, quantity, remarks)
            VALUES (?, ?, ?, ?)
        ''', (item_id, transaction_type, quantity, remarks))
        
        conn.commit()
        
        # Update inventory quantity
        update_stock(item_id, new_quantity)
        
        transaction_id = cursor.lastrowid
        conn.close()
        
        return transaction_id
        
    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

def get_all_transactions():
    """Get all transactions with item details"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.id, i.name, i.category, t.transaction_type, t.quantity, 
               t.remarks, t.created_at
        FROM transactions t
        JOIN inventory i ON t.item_id = i.id
        ORDER BY t.created_at DESC
    ''')
    
    transactions = cursor.fetchall()
    conn.close()
    
    return transactions

def get_transactions_by_item(item_id):
    """Get all transactions for a specific item"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.id, t.transaction_type, t.quantity, t.remarks, t.created_at
        FROM transactions t
        WHERE t.item_id = ?
        ORDER BY t.created_at DESC
    ''', (item_id,))
    
    transactions = cursor.fetchall()
    conn.close()
    
    return transactions

def get_recent_transactions(limit=10):
    """Get recent transactions"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.id, i.name, i.category, t.transaction_type, t.quantity, 
               t.remarks, t.created_at
        FROM transactions t
        JOIN inventory i ON t.item_id = i.id
        ORDER BY t.created_at DESC
        LIMIT ?
    ''', (limit,))
    
    transactions = cursor.fetchall()
    conn.close()
    
    return transactions

def get_transaction_summary():
    """Get transaction summary statistics"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Get total incoming and outgoing quantities
    cursor.execute('''
        SELECT 
            SUM(CASE WHEN transaction_type = 'incoming' THEN quantity ELSE 0 END) as total_incoming,
            SUM(CASE WHEN transaction_type = 'outgoing' THEN quantity ELSE 0 END) as total_outgoing,
            COUNT(*) as total_transactions
        FROM transactions
    ''')
    
    summary = cursor.fetchone()
    conn.close()
    
    return {
        'total_incoming': summary[0] if summary[0] else 0,
        'total_outgoing': summary[1] if summary[1] else 0,
        'total_transactions': summary[2] if summary[2] else 0
    }

def delete_transaction(transaction_id):
    """Delete a transaction (for admin purposes)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
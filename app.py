from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import inventory
import transactions
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize databases
inventory.init_db()
transactions.init_transactions_db()

@app.route('/')
def dashboard():
    """Main dashboard showing overview"""
    items = inventory.get_all_inventory()
    low_stock_items = inventory.get_low_stock_items()
    total_value = inventory.get_inventory_value()
    recent_transactions = transactions.get_recent_transactions(5)
    transaction_summary = transactions.get_transaction_summary()
    
    stats = {
        'total_items': len(items),
        'low_stock_count': len(low_stock_items),
        'total_value': total_value,
        'recent_transactions': recent_transactions,
        'transaction_summary': transaction_summary
    }
    
    return render_template('dashboard.html', stats=stats, low_stock_items=low_stock_items)

@app.route('/inventory')
def view_inventory():
    """View all inventory items"""
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    if search_query:
        items = inventory.search_inventory(search_query)
    else:
        items = inventory.get_all_inventory()
    
    if category_filter:
        items = [item for item in items if item[2] == category_filter]
    
    categories = inventory.get_categories()
    
    return render_template('inventory.html', 
                         items=items, 
                         categories=categories,
                         search_query=search_query,
                         category_filter=category_filter)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
    """Add new inventory item"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            quantity = int(request.form['quantity'])
            reorder_level = int(request.form['reorder_level'])
            cost_per_unit = float(request.form['cost_per_unit'])
            
            inventory.add_inventory_item(name, category, quantity, reorder_level, cost_per_unit)
            flash('Item added successfully!', 'success')
            return redirect(url_for('view_inventory'))
            
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Error adding item: ' + str(e), 'error')
    
    return render_template('add_inventory.html')

@app.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_inventory(item_id):
    """Edit existing inventory item"""
    item = inventory.get_inventory_by_id(item_id)
    
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('view_inventory'))
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            quantity = int(request.form['quantity'])
            reorder_level = int(request.form['reorder_level'])
            cost_per_unit = float(request.form['cost_per_unit'])
            
            inventory.update_inventory_item(item_id, name, category, quantity, reorder_level, cost_per_unit)
            flash('Item updated successfully!', 'success')
            return redirect(url_for('view_inventory'))
            
        except Exception as e:
            flash('Error updating item: ' + str(e), 'error')
    
    return render_template('edit_inventory.html', item=item)

@app.route('/transactions')
def view_transactions():
    """View all transactions"""
    all_transactions = transactions.get_all_transactions()
    transaction_summary = transactions.get_transaction_summary()
    
    return render_template('transactions.html', 
                         transactions=all_transactions,
                         summary=transaction_summary)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    """Add new transaction"""
    if request.method == 'POST':
        try:
            item_id = int(request.form['item_id'])
            transaction_type = request.form['transaction_type']
            quantity = int(request.form['quantity'])
            remarks = request.form.get('remarks', '')
            
            transactions.add_transaction(item_id, transaction_type, quantity, remarks)
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('view_transactions'))
            
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Error adding transaction: ' + str(e), 'error')
    
    items = inventory.get_all_inventory()
    return render_template('add_transaction.html', items=items)

@app.route('/api/inventory/search')
def api_search_inventory():
    """API endpoint for searching inventory"""
    query = request.args.get('q', '')
    items = inventory.search_inventory(query)
    
    result = []
    for item in items:
        result.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'quantity': item[3],
            'reorder_level': item[4],
            'cost_per_unit': item[5],
            'total_value': item[6],
            'stock_status': item[7]
        })
    
    return jsonify(result)

@app.route('/api/inventory/<int:item_id>')
def api_get_inventory(item_id):
    """API endpoint for getting specific inventory item"""
    item = inventory.get_inventory_by_id(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({
        'id': item[0],
        'name': item[1],
        'category': item[2],
        'quantity': item[3],
        'reorder_level': item[4],
        'cost_per_unit': item[5]
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    items = inventory.get_all_inventory()
    low_stock_items = inventory.get_low_stock_items()
    total_value = inventory.get_inventory_value()
    transaction_summary = transactions.get_transaction_summary()
    
    return jsonify({
        'total_items': len(items),
        'low_stock_count': len(low_stock_items),
        'total_value': total_value,
        'transaction_summary': transaction_summary
    })

@app.template_filter('datetime')
def datetime_filter(value):
    """Format datetime for templates"""
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return value
    return value

@app.template_filter('currency')
def currency_filter(value):
    """Format currency for templates"""
    try:
        return f"₹{float(value):,.2f}"
    except:
        return value

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
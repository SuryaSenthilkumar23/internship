# SML Isuzu Inventory Management System

A lightweight, modern inventory management dashboard built for SML Isuzu internship project. This system provides comprehensive inventory tracking, transaction management, and real-time alerts for low stock items.

## 🚀 Features

### Core Functionality
- **Inventory Management**: Add, edit, and track inventory items with detailed information
- **Transaction Recording**: Track incoming and outgoing stock with timestamps and remarks
- **Low Stock Alerts**: Automatic alerts when items reach reorder levels
- **Search & Filter**: Real-time search by name or category with filtering options
- **Dashboard Analytics**: Visual overview with key metrics and statistics

### Advanced Features
- **Color-coded Stock Levels**: Visual indicators for stock status (low, medium, high)
- **Total Inventory Value**: Calculate and display total worth of inventory
- **Transaction History**: Complete audit trail of all stock movements
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Quick Actions**: Fast transaction entry from inventory view

## 🛠️ Tech Stack

- **Backend**: Python Flask (lightweight web framework)
- **Database**: SQLite (embedded database, no setup required)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Icons**: Font Awesome 6.0
- **Styling**: Modern CSS with CSS Grid and Flexbox

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🔧 Installation & Setup

### 1. Clone or Download the Project
```bash
# If you have git installed
git clone <repository-url>
cd inventory-management

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
The database will be automatically created when you first run the application.

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Dashboard
Open your web browser and go to:
```
http://localhost:5000
```

## 🎯 Usage Guide

### Dashboard
- View key metrics: total items, low stock alerts, inventory value
- Quick access to recent transactions
- Color-coded low stock warnings

### Inventory Management
- **Add Items**: Click "Add New Item" to create inventory entries
- **Edit Items**: Click the edit icon next to any item
- **Search**: Use the search bar to find items by name or category
- **Filter**: Use category dropdown to filter items
- **Quick Transactions**: Click transaction icon for fast stock updates

### Transaction Management
- **Add Transactions**: Record incoming/outgoing stock movements
- **View History**: Complete transaction log with timestamps
- **Transaction Types**:
  - **Incoming**: Stock received, purchases, returns
  - **Outgoing**: Stock sold, issued, damaged, lost

### Search & Filter
- Real-time search as you type
- Filter by category
- Clear filters to view all items

## 📊 Database Schema

### Inventory Table
- `id`: Primary key
- `name`: Item name (unique)
- `category`: Item category
- `quantity`: Current stock quantity
- `reorder_level`: Minimum stock level
- `cost_per_unit`: Cost per unit in ₹
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Transactions Table
- `id`: Primary key
- `item_id`: Foreign key to inventory
- `transaction_type`: 'incoming' or 'outgoing'
- `quantity`: Transaction quantity
- `remarks`: Optional notes
- `created_at`: Transaction timestamp

## 🎨 Features Showcase

### Visual Indicators
- **🟢 Green**: Good stock levels
- **🟡 Yellow**: Medium stock (approaching reorder level)
- **🔴 Red**: Low stock (at or below reorder level)

### Smart Alerts
- Automatic low stock detection
- Visual dashboard warnings
- Color-coded inventory table

### Modern UI
- Clean, professional design
- Responsive layout for all devices
- Intuitive navigation
- Interactive elements

## 🔒 Security Notes

- Change the `app.secret_key` in `app.py` for production use
- The current setup is for development/demo purposes
- For production, consider using a more robust database (PostgreSQL, MySQL)

## 🚀 Deployment Options

### Local Development
Already configured for local development with Flask's built-in server.

### Production Deployment
For production deployment, consider:
- **Gunicorn**: `pip install gunicorn`
- **uWSGI**: `pip install uwsgi`
- **Docker**: Containerization for easy deployment
- **Cloud Platforms**: Heroku, AWS, Google Cloud, Azure

## 📱 Mobile Responsiveness

The application is fully responsive and works well on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔧 Customization

### Adding New Features
1. **Backend**: Add new routes in `app.py`
2. **Database**: Modify `inventory.py` or `transactions.py`
3. **Frontend**: Update templates in `templates/`
4. **Styling**: Modify `static/css/style.css`

### Changing Company Branding
1. Update navigation logo in `templates/base.html`
2. Modify colors in CSS variables in `static/css/style.css`
3. Update footer information

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in app.py or kill process using port 5000
   python app.py
   ```

2. **Database Not Created**
   ```bash
   # Delete any existing database file and restart
   rm inventory.db
   python app.py
   ```

3. **CSS/JS Not Loading**
   - Check if files exist in `static/` directory
   - Clear browser cache
   - Ensure Flask is serving static files correctly

### Reset Database
```bash
# Stop the application
# Delete database file
rm inventory.db
# Restart application
python app.py
```

## 📄 File Structure

```
inventory-management/
├── app.py                 # Main Flask application
├── inventory.py           # Inventory management functions
├── transactions.py        # Transaction management functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── inventory.db          # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── inventory.html
│   ├── add_inventory.html
│   ├── edit_inventory.html
│   ├── transactions.html
│   └── add_transaction.html
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        └── main.js       # JavaScript functionality
```

## 🤝 Contributing

This project was created for educational purposes as part of an internship project. Feel free to:
- Report issues
- Suggest improvements
- Add new features
- Improve documentation

## 📝 License

This project is created for educational purposes as part of an internship at SML Isuzu. 

## 👨‍💻 Author

Created as part of internship project at SML Isuzu.

## 🔄 Version History

- **v1.0**: Initial release with core inventory management features
- **v1.1**: Added transaction management and search functionality
- **v1.2**: Enhanced UI/UX with modern design and responsiveness

## 📞 Support

For support or questions about this project, please refer to the documentation or create an issue in the project repository.

---

**Happy Inventory Management! 📦**
# 🏠 UrbanHome - Real Estate Marketplace

A full-stack Django web application for buying, selling, and renting properties. Built with modern web technologies and a focus on user experience.

## ✨ Features

### 🏘️ Property Management
- **Property Listings**: Create, edit, and manage property listings
- **Image Upload**: Multiple images per property with main image support
- **Property Details**: BHK, area, amenities, furnished status, parking, etc.
- **Location Hierarchy**: Country → State → City → Town → Village system

### 🔍 Advanced Search & Filtering
- **Search by Location**: City, area, pincode
- **Price Range**: Min/Max price filtering
- **Property Type**: Rent/Sale filtering
- **BHK & Amenities**: Filter by bedrooms and amenities
- **Sorting Options**: Price, date, rating

### 👥 User Features
- **User Authentication**: Register, login, profile management
- **Favorites System**: Save and manage favorite properties
- **Messaging System**: Direct communication between users
- **Reviews & Ratings**: Rate and review properties
- **Dashboard**: Personal property and message management

### 🎨 Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Theme**: Modern dark color scheme
- **Interactive Elements**: Hover effects, smooth transitions
- **Bootstrap 5**: Professional styling framework

## 🛠️ Technology Stack

### Backend
- **Django 4.x**: Python web framework
- **SQLite**: Database (can be easily migrated to PostgreSQL/MySQL)
- **Django Admin**: Content management interface

### Frontend
- **HTML5/CSS3**: Semantic markup and modern styling
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive UI components
- **Font Awesome**: Icons

### Features
- **File Upload**: Image handling with Django
- **AJAX**: Dynamic content loading
- **Form Validation**: Client and server-side validation
- **Search & Filter**: Advanced query system

## 🌐 Live Demo

**Coming Soon!** This project will be deployed to a live server for demonstration.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/urbanhome.git
cd urbanhome
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the application.

## 🖼️ Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Property Listings
![Property Listings](screenshots/listings.png)

### Property Details
![Property Details](screenshots/property-detail.png)

### User Dashboard
![Dashboard](screenshots/dashboard.png)

*Note: Screenshots will be added after deployment*

## 📁 Project Structure

```
urbanhome/
├── homefinder/          # Main app for home page, about, contact
├── listings/           # Property listings and management
├── users/             # User authentication and profiles
├── urbanhome/         # Project settings and configuration
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # User uploaded files
└── requirements.txt  # Python dependencies
```

## 🎯 Key Features Explained

### Property Management System
- **CRUD Operations**: Create, Read, Update, Delete properties
- **Owner Verification**: Only property owners can edit their listings
- **Image Management**: Multiple images with main image selection
- **Status Management**: Active/Inactive property status

### Search & Filter System
- **Dynamic Filtering**: Real-time search results
- **Location-based**: Multi-level location hierarchy
- **Price Range**: Flexible price filtering
- **Advanced Queries**: Complex search combinations

### User Interaction
- **Messaging**: Direct communication between buyers and sellers
- **Favorites**: Save interesting properties
- **Reviews**: Rate and comment on properties
- **Notifications**: Message read status

## 🔧 Customization

### Adding New Features
1. Create new Django app: `python manage.py startapp newapp`
2. Add to INSTALLED_APPS in settings.py
3. Create models, views, and templates
4. Update URLs and navigation

### Styling Changes
- Modify `static/css/style.css` for custom styles
- Update Bootstrap classes in templates
- Add custom JavaScript in `static/js/main.js`

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop**: Full feature set with advanced layouts
- **Tablet**: Optimized layouts for medium screens
- **Mobile**: Touch-friendly interface with simplified navigation

## 🔒 Security Features

- **User Authentication**: Secure login/logout system
- **CSRF Protection**: Built-in Django security
- **File Upload Validation**: Secure image uploads
- **SQL Injection Protection**: Django ORM security
- **XSS Protection**: Template auto-escaping

## 🚀 Deployment

### For Production
1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Deploy to your preferred hosting service

### Recommended Hosting
- **Heroku**: Easy Django deployment
- **DigitalOcean**: VPS hosting
- **AWS**: Scalable cloud hosting
- **PythonAnywhere**: Django-specific hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**BUDIREDDY ATCHUTH KUMAR**
- GitHub: [@8331088013](https://github.com/8331088013)
- Location: Chittoor, India
- Email: budireddyatchuthkumar@gmail.com

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome
- Stack Overflow Community

---

⭐ **Star this repository if you found it helpful!** 
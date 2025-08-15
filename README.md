# Mexican Trout Biodiversity Project

A modern web-based system for managing and displaying Mexican trout biodiversity data, replacing the discontinued Drupal-based system from the British Museum of Natural History.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/varundataquest/Texas-Fishes-Lab.git
   cd Texas-Fishes-Lab
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Features

### 🗺️ Interactive Map
- Visualize all 350+ Mexican trout occurrence records
- Filter by species, basin, state, and year
- Export filtered data
- Mobile-responsive design

### 🐟 Species Directory
- Complete taxonomy and conservation status
- IUCN Red List assessments
- Search and filter functionality
- Detailed species information

### 📊 Data Explorer
- Advanced filtering and search
- Export data in CSV, JSON, and Excel formats
- Statistical summaries and charts
- Pagination for large datasets

### ⚙️ Admin Panel
- Excel data import functionality
- Data validation and quality checks
- System monitoring and logs
- Configuration management

## Data Import

To import your existing Excel data:

```bash
python import_data.py
```

This will:
- Load data from the Excel file
- Clean and validate the data
- Import occurrence records, species taxonomy, and genetic data
- Create the database schema

## API Endpoints

- `GET /api/occurrences` - Get occurrence records with filtering
- `GET /api/species` - Get species taxonomy information
- `GET /api/statistics` - Get database statistics
- `GET /api/map-data` - Get GeoJSON for mapping
- `POST /api/import-excel` - Import Excel data
- `GET /api/export-data` - Export data in various formats

## Configuration

Copy the environment template and customize:

```bash
cp env_example.txt .env
# Edit .env with your settings
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in app.py or kill existing process
   lsof -ti:5000 | xargs kill -9
   ```

2. **Database errors**
   ```bash
   # Remove existing database and recreate
   rm instance/mexican_trout.db
   python app.py
   ```

3. **Import errors**
   - Ensure Excel file is in the project directory
   - Check file permissions
   - Verify Excel file format

### Testing

Run the test suite:

```bash
python test_app.py
```

## Development

### Project Structure
```
Texas-Fishes-Lab/
├── app.py                 # Main Flask application
├── import_data.py         # Data import script
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
├── static/               # CSS, JS, and images
└── README.md             # This file
```

### Adding Features
1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Submit pull request

## Deployment

### Production Setup
1. Use PostgreSQL with PostGIS
2. Set production environment variables
3. Use Gunicorn behind Nginx
4. Configure SSL with Let's Encrypt

### Docker Deployment
```bash
docker build -t mexican-trout .
docker run -p 5000:5000 mexican-trout
```

## Support

- **Documentation**: See README.md and inline code comments
- **Issues**: Report bugs on GitHub
- **Contact**: [Your Email] for technical support

## License

This project is licensed under the MIT License.

---

**Repository**: https://github.com/varundataquest/Texas-Fishes-Lab  
**Status**: Complete and Ready for Deployment 
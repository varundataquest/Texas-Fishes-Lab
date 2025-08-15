# Mexican Trout Biodiversity Project

A modern web-based system for managing and displaying Mexican trout biodiversity data, replacing the discontinued Drupal-based system from the British Museum of Natural History.

## Project Overview

This project addresses the need for a modern, maintainable platform to manage Mexican trout biodiversity data. The original system was hosted on the British Museum's Scratchpads platform, which was discontinued in 2019. This new system provides:

- **Interactive mapping** of trout occurrences across the Sierra Madre Occidental
- **Comprehensive data management** with version control and quality validation
- **Public access** to biodiversity information and conservation status
- **GIS integration** for hydrographic data comparison
- **API access** for research and integration purposes

## Features

### Core Functionality
- **Interactive Map**: Explore trout occurrences with filtering and visualization
- **Species Directory**: Browse detailed information about Mexican trout species
- **Data Explorer**: Advanced filtering, searching, and export capabilities
- **Admin Panel**: Data import, validation, and management tools

### Data Management
- **Excel Import**: Import data from the existing Excel database
- **Data Validation**: Automated quality checks and error detection
- **Version Control**: Track changes and maintain data integrity
- **Export Options**: CSV, JSON, and Excel export formats

### GIS Integration
- **Multiple Hydrographic Datasets**: SIATL, Hydrosheds, GIRES, INEGI DEM
- **Spatial Analysis**: Watershed delineation and environmental variables
- **Comparison Tools**: Side-by-side analysis of different datasets

## Technology Stack

- **Backend**: Python Flask with SQLAlchemy ORM
- **Database**: SQLite (development) / PostgreSQL with PostGIS (production)
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Mapping**: Leaflet.js for interactive maps
- **Charts**: Chart.js for data visualization
- **Data Processing**: Pandas, GeoPandas, NumPy

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mexican-trout-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize the database**
   ```bash
   python import_data.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## Data Import

The application includes a data import script that loads the existing Excel database:

```bash
python import_data.py
```

This script will:
- Load data from the Excel file (`Mex_trout_records_merge_2011_12_ver11+Abadia_DAH2024-05-10 (version 1).xlsx`)
- Clean and validate the data
- Import occurrence records, species taxonomy, and genetic data
- Create the database schema and populate it with initial data

## Project Structure

```
mexican-trout-project/
├── app.py                 # Main Flask application
├── import_data.py         # Data import script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── map.html          # Interactive map
│   ├── species.html      # Species directory
│   ├── data.html         # Data explorer
│   └── admin.html        # Admin panel
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   └── images/           # Images and icons
└── data/                 # Data files
    └── *.xlsx            # Excel database files
```

## API Endpoints

### Occurrence Data
- `GET /api/occurrences` - Get occurrence records with filtering
- `GET /api/map-data` - Get GeoJSON data for mapping
- `POST /api/import-excel` - Import Excel data
- `GET /api/export-data` - Export data in various formats

### Species Data
- `GET /api/species` - Get species taxonomy information

### Statistics
- `GET /api/statistics` - Get database statistics and metadata

## Usage

### For Researchers
1. **Browse Species**: Visit the Species page to explore Mexican trout taxonomy
2. **Interactive Mapping**: Use the Map page to visualize distributions
3. **Data Export**: Download occurrence data in your preferred format
4. **API Access**: Use the REST API for programmatic access

### For Administrators
1. **Data Import**: Use the Admin panel to import new data
2. **Quality Control**: Run validation checks on the database
3. **System Monitoring**: View system statistics and activity logs
4. **User Management**: Configure access and permissions

### For the Public
1. **Educational Content**: Learn about Mexican trout biodiversity
2. **Conservation Information**: Access IUCN assessments and status
3. **Interactive Features**: Explore maps and species information

## Data Sources

### Primary Data
- **Occurrence Records**: 350+ collection records from 1903-2014
- **Species Taxonomy**: Mexican trout species classifications
- **Genetic Data**: Abadia et al. (2015) population structure analysis

### External Sources
- **IUCN Red List**: Conservation status assessments
- **SIATL**: Mexican National Hydrography System
- **Hydrosheds**: Global hydrographic datasets
- **GIRES**: Intermittent rivers and ephemeral streams
- **INEGI DEM**: Digital elevation models

## Development

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Add tests if applicable
4. Submit pull request

### Database Migrations
```bash
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

### Testing
```bash
python -m pytest tests/
```

## Deployment

### Production Setup
1. **Database**: Use PostgreSQL with PostGIS extension
2. **Web Server**: Deploy with Gunicorn behind Nginx
3. **Environment**: Set production environment variables
4. **SSL**: Configure HTTPS with Let's Encrypt

### Docker Deployment
```bash
docker build -t mexican-trout .
docker run -p 5000:5000 mexican-trout
```

## Contributing

We welcome contributions from the scientific community:

1. **Data Contributions**: Submit new occurrence records or corrections
2. **Code Contributions**: Improve the web application
3. **Documentation**: Help improve documentation and user guides
4. **Testing**: Report bugs and suggest improvements

## Contact

- **Project Lead**: Dean A. Hendrickson (deanhend@austin.utexas.edu)
- **Technical Support**: Contact the development team
- **Data Inquiries**: For data access and collaboration opportunities

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Cool Texas Fishes Biodiversity Lab** at the University of Texas at Austin
- **British Museum of Natural History** for the original Scratchpads system
- **IUCN** for conservation status assessments
- **INEGI** for Mexican hydrographic data
- **Research Collaborators** who contributed to the original data collection

## Future Development

### Planned Features
- **Advanced GIS Analysis**: Watershed modeling and environmental variables
- **Genetic Data Integration**: Enhanced genetic analysis tools
- **Mobile Application**: Native mobile app for field data collection
- **Machine Learning**: Species distribution modeling and prediction
- **Collaborative Features**: Multi-user editing and annotation

### Integration Goals
- **GBIF**: Integration with Global Biodiversity Information Facility
- **iNaturalist**: Citizen science data integration
- **Research Repositories**: Links to genetic and morphological data
- **Conservation Organizations**: Real-time status updates

---

*This project represents a modern approach to biodiversity data management, providing researchers, conservationists, and the public with comprehensive access to Mexican trout biodiversity information.* 
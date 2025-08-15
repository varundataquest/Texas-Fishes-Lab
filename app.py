from flask import Flask, render_template, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json
import os
from datetime import datetime
import folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mexican_trout.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Database Models
class OccurrenceRecord(db.Model):
    """Model for Mexican trout occurrence records"""
    __tablename__ = 'occurrence_records'
    
    id = db.Column(db.Integer, primary_key=True)
    unique_record_id = db.Column(db.String(50), unique=True, nullable=False)
    collection_date = db.Column(db.Date)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    locality_description = db.Column(db.Text)
    state = db.Column(db.String(100))
    municipality = db.Column(db.String(100))
    river_basin = db.Column(db.String(100))
    sub_basin = db.Column(db.String(100))
    species = db.Column(db.String(100))
    genus = db.Column(db.String(100))
    collectors = db.Column(db.String(200))
    field_number = db.Column(db.String(50))
    institution = db.Column(db.String(100))
    catalog_number = db.Column(db.String(50))
    specimen_count = db.Column(db.Integer)
    habitat_notes = db.Column(db.Text)
    conservation_status = db.Column(db.String(50))
    data_source = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Species(db.Model):
    """Model for Mexican trout species taxonomy"""
    __tablename__ = 'species'
    
    id = db.Column(db.Integer, primary_key=True)
    scientific_name = db.Column(db.String(100), unique=True, nullable=False)
    common_name = db.Column(db.String(100))
    taxon_code = db.Column(db.String(10))
    conservation_status = db.Column(db.String(50))
    iucn_assessment = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GeneticData(db.Model):
    """Model for genetic data from Abadia et al. (2015)"""
    __tablename__ = 'genetic_data'
    
    id = db.Column(db.Integer, primary_key=True)
    occurrence_record_id = db.Column(db.Integer, db.ForeignKey('occurrence_records.id'))
    sample_code = db.Column(db.String(50))
    population_number = db.Column(db.String(20))
    genetic_group = db.Column(db.String(50))
    haplotype = db.Column(db.String(50))
    sequence_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HydrographicData(db.Model):
    """Model for hydrographic dataset comparisons"""
    __tablename__ = 'hydrographic_data'
    
    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(100), nullable=False)  # SIATL, Hydrosheds, GIRES, etc.
    stream_id = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    stream_order = db.Column(db.Integer)
    flow_accumulation = db.Column(db.Float)
    elevation = db.Column(db.Float)
    basin_name = db.Column(db.String(100))
    sub_basin_name = db.Column(db.String(100))
    data_quality = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/species')
def species_list():
    """Species listing page"""
    species = Species.query.all()
    return render_template('species.html', species=species)

@app.route('/species/<int:species_id>')
def species_detail(species_id):
    """Individual species detail page"""
    species = Species.query.get_or_404(species_id)
    occurrences = OccurrenceRecord.query.filter_by(species=species.scientific_name).all()
    return render_template('species_detail.html', species=species, occurrences=occurrences)

@app.route('/map')
def map_view():
    """Interactive map page"""
    return render_template('map.html')

@app.route('/data')
def data_explorer():
    """Data exploration page"""
    return render_template('data.html')

@app.route('/api/occurrences')
def api_occurrences():
    """API endpoint for occurrence data"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    species = request.args.get('species')
    basin = request.args.get('basin')
    state = request.args.get('state')
    
    query = OccurrenceRecord.query
    
    if species:
        query = query.filter(OccurrenceRecord.species.contains(species))
    if basin:
        query = query.filter(OccurrenceRecord.river_basin.contains(basin))
    if state:
        query = query.filter(OccurrenceRecord.state.contains(state))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    records = pagination.items
    
    return jsonify({
        'records': [{
            'id': record.id,
            'unique_record_id': record.unique_record_id,
            'collection_date': record.collection_date.isoformat() if record.collection_date else None,
            'latitude': record.latitude,
            'longitude': record.longitude,
            'locality_description': record.locality_description,
            'state': record.state,
            'municipality': record.municipality,
            'river_basin': record.river_basin,
            'species': record.species,
            'collectors': record.collectors,
            'field_number': record.field_number,
            'institution': record.institution,
            'catalog_number': record.catalog_number,
            'specimen_count': record.specimen_count,
            'conservation_status': record.conservation_status
        } for record in records],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })

@app.route('/api/species')
def api_species():
    """API endpoint for species data"""
    species = Species.query.all()
    return jsonify([{
        'id': s.id,
        'scientific_name': s.scientific_name,
        'common_name': s.common_name,
        'taxon_code': s.taxon_code,
        'conservation_status': s.conservation_status,
        'iucn_assessment': s.iucn_assessment
    } for s in species])

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for data statistics"""
    total_records = OccurrenceRecord.query.count()
    records_with_coords = OccurrenceRecord.query.filter(
        OccurrenceRecord.latitude.isnot(None),
        OccurrenceRecord.longitude.isnot(None)
    ).count()
    
    # Get unique values for filters
    states = db.session.query(OccurrenceRecord.state).distinct().filter(
        OccurrenceRecord.state.isnot(None)
    ).all()
    basins = db.session.query(OccurrenceRecord.river_basin).distinct().filter(
        OccurrenceRecord.river_basin.isnot(None)
    ).all()
    species_list = db.session.query(OccurrenceRecord.species).distinct().filter(
        OccurrenceRecord.species.isnot(None)
    ).all()
    
    return jsonify({
        'total_records': total_records,
        'records_with_coordinates': records_with_coords,
        'coordinate_percentage': round((records_with_coords / total_records * 100), 1) if total_records > 0 else 0,
        'states': [s[0] for s in states if s[0]],
        'basins': [b[0] for b in basins if b[0]],
        'species': [sp[0] for sp in species_list if sp[0]]
    })

@app.route('/api/map-data')
def api_map_data():
    """API endpoint for map visualization data"""
    records = OccurrenceRecord.query.filter(
        OccurrenceRecord.latitude.isnot(None),
        OccurrenceRecord.longitude.isnot(None)
    ).all()
    
    features = []
    for record in records:
        if record.latitude and record.longitude:
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [record.longitude, record.latitude]
                },
                'properties': {
                    'id': record.id,
                    'unique_record_id': record.unique_record_id,
                    'species': record.species,
                    'collection_date': record.collection_date.isoformat() if record.collection_date else None,
                    'locality': record.locality_description,
                    'state': record.state,
                    'basin': record.river_basin,
                    'collectors': record.collectors,
                    'field_number': record.field_number,
                    'institution': record.institution,
                    'catalog_number': record.catalog_number
                }
            }
            features.append(feature)
    
    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })

@app.route('/admin')
def admin_panel():
    """Admin panel for data management"""
    return render_template('admin.html')

@app.route('/api/import-excel', methods=['POST'])
def import_excel():
    """Import data from Excel file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read Excel file
        df = pd.read_excel(file, sheet_name='Mex_trout_core')
        
        # Process and import data
        imported_count = 0
        for _, row in df.iterrows():
            # Create occurrence record
            record = OccurrenceRecord(
                unique_record_id=str(row.get('Final_database_unique_record_ID', '')),
                collection_date=pd.to_datetime(row.get('data__yyyy', ''), errors='coerce').date() if pd.notna(row.get('data__yyyy')) else None,
                latitude=row.get('lat_dec') if pd.notna(row.get('lat_dec')) else None,
                longitude=row.get('long_dec') if pd.notna(row.get('long_dec')) else None,
                locality_description=row.get('locality', ''),
                state=row.get('state', ''),
                municipality=row.get('municipio', ''),
                river_basin=row.get('basin', ''),
                sub_basin=row.get('subbasin', ''),
                species=row.get('species', ''),
                genus=row.get('genus', ''),
                collectors=row.get('collectors', ''),
                field_number=row.get('field_num', ''),
                institution=row.get('institution', ''),
                catalog_number=row.get('catalog_num', ''),
                specimen_count=row.get('N_specimens') if pd.notna(row.get('N_specimens')) else None,
                habitat_notes=row.get('habitat_notes', ''),
                data_source='Excel Import'
            )
            
            db.session.add(record)
            imported_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Successfully imported {imported_count} records'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Import failed: {str(e)}'}), 500

@app.route('/api/export-data')
def export_data():
    """Export data as CSV"""
    records = OccurrenceRecord.query.all()
    
    data = []
    for record in records:
        data.append({
            'Unique Record ID': record.unique_record_id,
            'Collection Date': record.collection_date.isoformat() if record.collection_date else '',
            'Latitude': record.latitude,
            'Longitude': record.longitude,
            'Locality Description': record.locality_description,
            'State': record.state,
            'Municipality': record.municipality,
            'River Basin': record.river_basin,
            'Sub Basin': record.sub_basin,
            'Species': record.species,
            'Genus': record.genus,
            'Collectors': record.collectors,
            'Field Number': record.field_number,
            'Institution': record.institution,
            'Catalog Number': record.catalog_number,
            'Specimen Count': record.specimen_count,
            'Habitat Notes': record.habitat_notes,
            'Conservation Status': record.conservation_status
        })
    
    df = pd.DataFrame(data)
    csv_path = 'exported_data.csv'
    df.to_csv(csv_path, index=False)
    
    return send_file(csv_path, as_attachment=True, download_name='mexican_trout_data.csv')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 
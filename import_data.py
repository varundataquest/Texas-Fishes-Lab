#!/usr/bin/env python3
"""
Data import script for Mexican Trout Biodiversity Project
Loads Excel data into the database and populates initial species information
"""

import pandas as pd
import sys
import os
from datetime import datetime
from app import app, db, OccurrenceRecord, Species, GeneticData

def load_excel_data(file_path):
    """Load data from Excel file"""
    print(f"Loading data from {file_path}...")
    
    try:
        # Read the main data sheet
        df = pd.read_excel(file_path, sheet_name='Mex_trout_core')
        print(f"Loaded {len(df)} records from Mex_trout_core sheet")
        
        # Read species taxonomy sheet
        species_df = pd.read_excel(file_path, sheet_name='taxa_names')
        print(f"Loaded {len(species_df)} species from taxa_names sheet")
        
        # Read genetic data sheet
        genetic_df = pd.read_excel(file_path, sheet_name='Abadia_S1')
        print(f"Loaded {len(genetic_df)} genetic records from Abadia_S1 sheet")
        
        return df, species_df, genetic_df
        
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None, None, None

def clean_data(df):
    """Clean and normalize the data"""
    print("Cleaning data...")
    
    # Remove rows with no unique record ID
    df = df.dropna(subset=['Final_database_unique_record_ID'])
    
    # Clean coordinate data
    df['lat_dec'] = pd.to_numeric(df['lat_dec'], errors='coerce')
    df['long_dec'] = pd.to_numeric(df['long_dec'], errors='coerce')
    
    # Clean date data
    df['data__yyyy'] = pd.to_datetime(df['data__yyyy'], errors='coerce')
    
    # Clean specimen count
    df['N_specimens'] = pd.to_numeric(df['N_specimens'], errors='coerce')
    
    # Fill missing values
    df = df.fillna('')
    
    print(f"Cleaned data: {len(df)} records")
    return df

def import_species_data(species_df):
    """Import species taxonomy data"""
    print("Importing species data...")
    
    imported_count = 0
    for _, row in species_df.iterrows():
        try:
            # Check if species already exists
            existing = Species.query.filter_by(scientific_name=row.get('scientific_name', '')).first()
            if existing:
                continue
                
            species = Species(
                scientific_name=row.get('scientific_name', ''),
                common_name=row.get('common_name', ''),
                taxon_code=row.get('taxon_code', ''),
                conservation_status=row.get('conservation_status', ''),
                iucn_assessment=row.get('iucn_assessment', ''),
                description=row.get('description', '')
            )
            
            db.session.add(species)
            imported_count += 1
            
        except Exception as e:
            print(f"Error importing species {row.get('scientific_name', '')}: {e}")
            continue
    
    db.session.commit()
    print(f"Imported {imported_count} species")
    return imported_count

def import_occurrence_data(df):
    """Import occurrence records"""
    print("Importing occurrence data...")
    
    imported_count = 0
    errors = 0
    
    for _, row in df.iterrows():
        try:
            # Check if record already exists
            existing = OccurrenceRecord.query.filter_by(
                unique_record_id=str(row.get('Final_database_unique_record_ID', ''))
            ).first()
            
            if existing:
                continue
            
            # Parse date
            collection_date = None
            if pd.notna(row.get('data__yyyy')):
                if isinstance(row['data__yyyy'], str):
                    try:
                        collection_date = datetime.strptime(row['data__yyyy'], '%Y%m%d').date()
                    except:
                        try:
                            collection_date = pd.to_datetime(row['data__yyyy']).date()
                        except:
                            collection_date = None
                else:
                    collection_date = row['data__yyyy'].date()
            
            record = OccurrenceRecord(
                unique_record_id=str(row.get('Final_database_unique_record_ID', '')),
                collection_date=collection_date,
                latitude=row.get('lat_dec') if pd.notna(row.get('lat_dec')) else None,
                longitude=row.get('long_dec') if pd.notna(row.get('long_dec')) else None,
                locality_description=str(row.get('locality', '')),
                state=str(row.get('state', '')),
                municipality=str(row.get('municipio', '')),
                river_basin=str(row.get('basin', '')),
                sub_basin=str(row.get('subbasin', '')),
                species=str(row.get('species', '')),
                genus=str(row.get('genus', '')),
                collectors=str(row.get('collectors', '')),
                field_number=str(row.get('field_num', '')),
                institution=str(row.get('institution', '')),
                catalog_number=str(row.get('catalog_num', '')),
                specimen_count=int(row.get('N_specimens')) if pd.notna(row.get('N_specimens')) else None,
                habitat_notes=str(row.get('habitat_notes', '')),
                conservation_status=str(row.get('conservation_status', '')),
                data_source='Excel Import'
            )
            
            db.session.add(record)
            imported_count += 1
            
            # Commit every 100 records to avoid memory issues
            if imported_count % 100 == 0:
                db.session.commit()
                print(f"Imported {imported_count} records...")
                
        except Exception as e:
            errors += 1
            print(f"Error importing record {row.get('Final_database_unique_record_ID', '')}: {e}")
            continue
    
    db.session.commit()
    print(f"Imported {imported_count} occurrence records with {errors} errors")
    return imported_count, errors

def import_genetic_data(genetic_df):
    """Import genetic data from Abadia et al. (2015)"""
    print("Importing genetic data...")
    
    imported_count = 0
    
    for _, row in genetic_df.iterrows():
        try:
            # Link to occurrence record if possible
            occurrence_record_id = None
            if pd.notna(row.get('Final_database_unique_record_ID')):
                occurrence_record = OccurrenceRecord.query.filter_by(
                    unique_record_id=str(row.get('Final_database_unique_record_ID'))
                ).first()
                if occurrence_record:
                    occurrence_record_id = occurrence_record.id
            
            genetic_record = GeneticData(
                occurrence_record_id=occurrence_record_id,
                sample_code=str(row.get('Sample_Code', '')),
                population_number=str(row.get('Population_No', '')),
                genetic_group=str(row.get('Genetic_Gr', '')),
                haplotype=str(row.get('Haplotype', '')),
                sequence_data=str(row.get('Sequence_Data', ''))
            )
            
            db.session.add(genetic_record)
            imported_count += 1
            
        except Exception as e:
            print(f"Error importing genetic record: {e}")
            continue
    
    db.session.commit()
    print(f"Imported {imported_count} genetic records")
    return imported_count

def create_sample_species():
    """Create sample species data if none exists"""
    print("Creating sample species data...")
    
    sample_species = [
        {
            'scientific_name': 'Oncorhynchus mykiss nelsoni',
            'common_name': 'Baja California Rainbow Trout',
            'taxon_code': 'A',
            'conservation_status': 'Endangered',
            'iucn_assessment': 'https://www.iucnredlist.org/species/142674143/145641616',
            'description': 'Native rainbow trout subspecies found in Baja California streams'
        },
        {
            'scientific_name': 'Oncorhynchus chrysogaster',
            'common_name': 'Mexican Golden Trout',
            'taxon_code': 'B',
            'conservation_status': 'Endangered',
            'iucn_assessment': 'https://www.iucnredlist.org/species/142674185/145641626',
            'description': 'Golden trout species endemic to the Sierra Madre Occidental'
        },
        {
            'scientific_name': 'Oncorhynchus sp. nov. "Yaqui"',
            'common_name': 'Yaqui Trout',
            'taxon_code': 'C',
            'conservation_status': 'Vulnerable',
            'iucn_assessment': 'https://www.iucnredlist.org/species/145641073/145641656',
            'description': 'Undescribed trout species from the Yaqui River basin'
        },
        {
            'scientific_name': 'Oncorhynchus sp. nov. "Fuerte"',
            'common_name': 'Fuerte Trout',
            'taxon_code': 'D',
            'conservation_status': 'Near Threatened',
            'description': 'Undescribed trout species from the Fuerte River basin'
        },
        {
            'scientific_name': 'Oncorhynchus sp. nov. "Santo Domingo"',
            'common_name': 'Santo Domingo Trout',
            'taxon_code': 'E',
            'conservation_status': 'Data Deficient',
            'description': 'Undescribed trout species from the Santo Domingo River basin'
        }
    ]
    
    imported_count = 0
    for species_data in sample_species:
        try:
            existing = Species.query.filter_by(scientific_name=species_data['scientific_name']).first()
            if not existing:
                species = Species(**species_data)
                db.session.add(species)
                imported_count += 1
        except Exception as e:
            print(f"Error creating species {species_data['scientific_name']}: {e}")
    
    db.session.commit()
    print(f"Created {imported_count} sample species")
    return imported_count

def main():
    """Main import function"""
    print("=== Mexican Trout Data Import ===")
    
    # Check if database exists and create tables
    with app.app_context():
        db.create_all()
        print("Database tables created")
        
        # Check if data already exists
        existing_records = OccurrenceRecord.query.count()
        if existing_records > 0:
            print(f"Database already contains {existing_records} records")
            response = input("Do you want to continue and add more data? (y/n): ")
            if response.lower() != 'y':
                print("Import cancelled")
                return
        
        # Load Excel data
        excel_file = 'Mex_trout_records_merge_2011_12_ver11+Abadia_DAH2024-05-10 (version 1).xlsx'
        
        if not os.path.exists(excel_file):
            print(f"Excel file not found: {excel_file}")
            print("Please ensure the Excel file is in the current directory")
            return
        
        df, species_df, genetic_df = load_excel_data(excel_file)
        
        if df is None:
            print("Failed to load Excel data")
            return
        
        # Clean data
        df = clean_data(df)
        
        # Import species data
        if species_df is not None:
            import_species_data(species_df)
        else:
            create_sample_species()
        
        # Import occurrence data
        imported_count, errors = import_occurrence_data(df)
        
        # Import genetic data
        if genetic_df is not None:
            import_genetic_data(genetic_df)
        
        # Print summary
        print("\n=== Import Summary ===")
        print(f"Occurrence records imported: {imported_count}")
        print(f"Import errors: {errors}")
        print(f"Species in database: {Species.query.count()}")
        print(f"Genetic records in database: {GeneticData.query.count()}")
        
        # Print some statistics
        total_records = OccurrenceRecord.query.count()
        records_with_coords = OccurrenceRecord.query.filter(
            OccurrenceRecord.latitude.isnot(None),
            OccurrenceRecord.longitude.isnot(None)
        ).count()
        
        print(f"\n=== Database Statistics ===")
        print(f"Total records: {total_records}")
        print(f"Records with coordinates: {records_with_coords}")
        print(f"Coordinate completeness: {records_with_coords/total_records*100:.1f}%")
        
        # Show unique values
        states = db.session.query(OccurrenceRecord.state).distinct().filter(
            OccurrenceRecord.state != ''
        ).all()
        basins = db.session.query(OccurrenceRecord.river_basin).distinct().filter(
            OccurrenceRecord.river_basin != ''
        ).all()
        species_list = db.session.query(OccurrenceRecord.species).distinct().filter(
            OccurrenceRecord.species != ''
        ).all()
        
        print(f"States covered: {len(states)}")
        print(f"River basins: {len(basins)}")
        print(f"Species: {len(species_list)}")
        
        print("\nImport completed successfully!")

if __name__ == '__main__':
    main() 
#!/usr/bin/env python3
"""
Mexican Trout Biodiversity Data Analysis and Web System Planning
Based on requirements from Dean Hendrickson, Cool Texas Fishes Biodiversity Lab

This script analyzes the existing Excel data and provides insights for building
a modern web-based system to replace the discontinued Drupal platform.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium import plugins
import os
import json
from datetime import datetime

class MexicanTroutAnalyzer:
    def __init__(self, excel_file_path):
        """Initialize the analyzer with the Excel file path."""
        self.excel_file_path = excel_file_path
        self.data = {}
        self.analysis_results = {}
        
    def load_data(self):
        """Load all sheets from the Excel file."""
        print("Loading Mexican Trout data...")
        
        excel_file = pd.ExcelFile(self.excel_file_path)
        print(f"Found {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names}")
        
        for sheet_name in excel_file.sheet_names:
            print(f"Loading sheet: {sheet_name}")
            self.data[sheet_name] = pd.read_excel(self.excel_file_path, sheet_name=sheet_name)
            
        print("Data loading complete!")
        
    def analyze_core_data(self):
        """Analyze the core Mexican trout records."""
        print("\n=== CORE DATA ANALYSIS ===")
        
        if 'Mex_trout_core' not in self.data:
            print("Core data not found!")
            return
            
        df = self.data['Mex_trout_core']
        
        # Basic statistics
        self.analysis_results['core_stats'] = {
            'total_records': len(df),
            'records_with_coordinates': len(df[df['Lat_dec'].notna() & df['Long_dec'].notna()]),
            'unique_states': df['State'].nunique(),
            'unique_basins': df['Maj_Basin'].nunique(),
        }
        
        # Handle date analysis carefully
        date_col = 'Date (yyyymmdd)'
        if date_col in df.columns:
            # Convert to numeric where possible
            numeric_dates = pd.to_numeric(df[date_col], errors='coerce')
            valid_dates = numeric_dates.dropna()
            if len(valid_dates) > 0:
                self.analysis_results['core_stats']['date_range'] = {
                    'earliest': int(valid_dates.min()),
                    'latest': int(valid_dates.max()),
                    'valid_dates': len(valid_dates)
                }
        
        print(f"Total records: {self.analysis_results['core_stats']['total_records']}")
        print(f"Records with coordinates: {self.analysis_results['core_stats']['records_with_coordinates']}")
        print(f"States covered: {self.analysis_results['core_stats']['unique_states']}")
        print(f"Major basins: {self.analysis_results['core_stats']['unique_basins']}")
        
        if 'date_range' in self.analysis_results['core_stats']:
            date_range = self.analysis_results['core_stats']['date_range']
            print(f"Date range: {date_range['earliest']} to {date_range['latest']} ({date_range['valid_dates']} valid dates)")
        
        # Geographic distribution
        state_counts = df['State'].value_counts()
        basin_counts = df['Maj_Basin'].value_counts()
        
        self.analysis_results['geographic_distribution'] = {
            'states': state_counts.to_dict(),
            'basins': basin_counts.to_dict()
        }
        
        print("\nTop 5 States:")
        print(state_counts.head())
        
        print("\nTop 5 Basins:")
        print(basin_counts.head())
        
    def analyze_taxonomic_data(self):
        """Analyze taxonomic classifications."""
        print("\n=== TAXONOMIC ANALYSIS ===")
        
        if 'taxa_names' not in self.data:
            print("Taxonomic data not found!")
            return
            
        df = self.data['taxa_names']
        
        print("Species Classifications:")
        for _, row in df.iterrows():
            if pd.notna(row['Genus']) and pd.notna(row['species']):
                species_name = f"{row['Genus']} {row['species']}"
                if pd.notna(row['subspecies']):
                    species_name += f" {row['subspecies']}"
                print(f"  {row['TM_taxon_code']}: {species_name} - {row['common_name']}")
                
        self.analysis_results['taxonomy'] = {
            'total_taxa': len(df),
            'species_list': df.to_dict('records')
        }
        
    def create_geographic_visualizations(self):
        """Create geographic visualizations of the data."""
        print("\n=== CREATING GEOGRAPHIC VISUALIZATIONS ===")
        
        if 'Mex_trout_core' not in self.data:
            print("Core data not available for mapping!")
            return
            
        df = self.data['Mex_trout_core']
        
        # Filter records with coordinates
        geo_df = df[df['Lat_dec'].notna() & df['Long_dec'].notna()].copy()
        
        if len(geo_df) == 0:
            print("No geographic data available!")
            return
            
        # Create output directory
        os.makedirs('visualizations', exist_ok=True)
        
        # 1. Interactive map with Folium
        print("Creating interactive map...")
        m = folium.Map(
            location=[geo_df['Lat_dec'].mean(), geo_df['Long_dec'].mean()],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add markers for each record
        for idx, row in geo_df.iterrows():
            popup_text = f"""
            <b>Location:</b> {row['Locality']}<br>
            <b>State:</b> {row['State']}<br>
            <b>Basin:</b> {row['Maj_Basin']}<br>
            <b>Species:</b> {row['cataloged genus']} {row['cataloged species']}<br>
            <b>Date:</b> {row['Date (yyyymmdd)']}<br>
            <b>Collectors:</b> {row['Collectors']}
            """
            
            folium.Marker(
                [row['Lat_dec'], row['Long_dec']],
                popup=popup_text,
                tooltip=f"{row['cataloged genus']} {row['cataloged species']}"
            ).add_to(m)
            
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save the map
        m.save('visualizations/mexican_trout_distribution.html')
        print("Interactive map saved to visualizations/mexican_trout_distribution.html")
        
        # 2. Basin distribution chart
        print("Creating basin distribution chart...")
        basin_counts = geo_df['Maj_Basin'].value_counts()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        basin_counts.plot(kind='bar', ax=ax)
        ax.set_title('Mexican Trout Distribution by Major Basin')
        ax.set_xlabel('Major Basin')
        ax.set_ylabel('Number of Records')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/basin_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. State distribution chart
        print("Creating state distribution chart...")
        state_counts = geo_df['State'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        state_counts.plot(kind='bar', ax=ax)
        ax.set_title('Mexican Trout Distribution by State')
        ax.set_xlabel('State')
        ax.set_ylabel('Number of Records')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.savefig('visualizations/state_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def analyze_data_quality(self):
        """Analyze data quality and completeness."""
        print("\n=== DATA QUALITY ANALYSIS ===")
        
        if 'Mex_trout_core' not in self.data:
            print("Core data not available for quality analysis!")
            return
            
        df = self.data['Mex_trout_core']
        
        # Check for missing data
        missing_data = {}
        for column in df.columns:
            missing_count = df[column].isna().sum()
            missing_percent = (missing_count / len(df)) * 100
            missing_data[column] = {
                'missing_count': missing_count,
                'missing_percent': missing_percent
            }
            
        # Focus on key fields
        key_fields = ['Lat_dec', 'Long_dec', 'Date (yyyymmdd)', 'Collectors', 
                     'cataloged genus', 'cataloged species', 'State', 'Maj_Basin']
        
        print("Missing data analysis for key fields:")
        for field in key_fields:
            if field in missing_data:
                info = missing_data[field]
                print(f"  {field}: {info['missing_count']} missing ({info['missing_percent']:.1f}%)")
                
        self.analysis_results['data_quality'] = {
            'missing_data': missing_data,
            'key_fields_analysis': {field: missing_data.get(field, {}) for field in key_fields}
        }
        
    def generate_web_system_recommendations(self):
        """Generate recommendations for the web system based on data analysis."""
        print("\n=== WEB SYSTEM RECOMMENDATIONS ===")
        
        recommendations = {
            'database_schema': {
                'core_tables': [
                    'occurrences',
                    'specimens', 
                    'taxa',
                    'localities',
                    'collectors',
                    'institutions'
                ],
                'spatial_features': 'PostGIS extension for geographic data',
                'version_control': 'Implement data versioning and change tracking'
            },
            'web_application': {
                'framework': 'Python Flask/Django with PostgreSQL/PostGIS',
                'frontend': 'React.js with Leaflet/Mapbox for mapping',
                'api': 'RESTful API for data access and updates',
                'admin_interface': 'Django Admin or custom admin panel'
            },
            'gis_integration': {
                'hydrographic_data': [
                    'SIATL (Mexican National System)',
                    'Hydrosheds',
                    'GIRES Database',
                    'INEGI DEM (100m elevation)'
                ],
                'comparison_tools': 'Side-by-side dataset comparison interface',
                'spatial_analysis': 'Buffer analysis, watershed delineation'
            },
            'data_management': {
                'cleaning_pipeline': 'Automated data validation and cleaning',
                'update_workflow': 'Version-controlled data updates',
                'backup_strategy': 'Regular automated backups',
                'access_control': 'Role-based permissions for data editing'
            },
            'public_features': {
                'species_pages': 'Detailed information for each trout species',
                'interactive_maps': 'Geographic distribution with multiple layers',
                'conservation_status': 'IUCN Red List integration',
                'data_download': 'API and bulk download options',
                'search_functionality': 'Advanced search and filtering'
            }
        }
        
        self.analysis_results['recommendations'] = recommendations
        
        print("Key recommendations:")
        print("1. Use PostgreSQL/PostGIS for spatial data management")
        print("2. Implement version control for all data changes")
        print("3. Create interactive mapping interface with multiple hydrographic layers")
        print("4. Build API for data access and integration")
        print("5. Develop admin interface for data management")
        print("6. Integrate conservation status from IUCN")
        
    def generate_implementation_plan(self):
        """Generate a detailed implementation plan."""
        print("\n=== IMPLEMENTATION PLAN ===")
        
        plan = {
            'phase_1': {
                'duration': '2 weeks',
                'tasks': [
                    'Data cleaning and normalization',
                    'Database schema design',
                    'Development environment setup',
                    'Basic data import scripts'
                ]
            },
            'phase_2': {
                'duration': '3 weeks', 
                'tasks': [
                    'Core database implementation',
                    'Basic web application framework',
                    'Data visualization components',
                    'API development'
                ]
            },
            'phase_3': {
                'duration': '3 weeks',
                'tasks': [
                    'GIS integration and mapping',
                    'Hydrographic data comparison tools',
                    'Species information pages',
                    'Admin interface development'
                ]
            },
            'phase_4': {
                'duration': '2 weeks',
                'tasks': [
                    'Conservation status integration',
                    'Advanced search and filtering',
                    'Performance optimization',
                    'Testing and documentation'
                ]
            },
            'phase_5': {
                'duration': '1 week',
                'tasks': [
                    'Production deployment',
                    'User training',
                    'Data migration from Excel',
                    'Go-live and monitoring'
                ]
            }
        }
        
        self.analysis_results['implementation_plan'] = plan
        
        print("Implementation timeline: 11 weeks total")
        for phase, details in plan.items():
            print(f"\n{phase.replace('_', ' ').title()}: {details['duration']}")
            for task in details['tasks']:
                print(f"  - {task}")
                
    def save_analysis_report(self):
        """Save the complete analysis report."""
        print("\n=== SAVING ANALYSIS REPORT ===")
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'data_summary': self.analysis_results,
            'file_info': {
                'excel_file': self.excel_file_path,
                'sheets_analyzed': list(self.data.keys())
            }
        }
        
        # Save as JSON
        with open('analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        # Save as markdown
        with open('analysis_report.md', 'w') as f:
            f.write("# Mexican Trout Data Analysis Report\n\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Data Summary\n\n")
            if 'core_stats' in self.analysis_results:
                stats = self.analysis_results['core_stats']
                f.write(f"- Total records: {stats['total_records']}\n")
                f.write(f"- Records with coordinates: {stats['records_with_coordinates']}\n")
                f.write(f"- States covered: {stats['unique_states']}\n")
                f.write(f"- Major basins: {stats['unique_basins']}\n")
                if 'date_range' in stats:
                    date_range = stats['date_range']
                    f.write(f"- Date range: {date_range['earliest']} to {date_range['latest']}\n")
                f.write("\n")
                
            f.write("## Geographic Distribution\n\n")
            if 'geographic_distribution' in self.analysis_results:
                geo = self.analysis_results['geographic_distribution']
                f.write("### Top States:\n")
                for state, count in list(geo['states'].items())[:5]:
                    f.write(f"- {state}: {count} records\n")
                f.write("\n### Top Basins:\n")
                for basin, count in list(geo['basins'].items())[:5]:
                    f.write(f"- {basin}: {count} records\n")
                    
        print("Analysis report saved to analysis_report.json and analysis_report.md")
        
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        print("=== MEXICAN TROUT BIODIVERSITY DATA ANALYSIS ===")
        print("Based on requirements from Dean Hendrickson, Cool Texas Fishes Biodiversity Lab\n")
        
        # Load data
        self.load_data()
        
        # Run analyses
        self.analyze_core_data()
        self.analyze_taxonomic_data()
        self.analyze_data_quality()
        
        # Create visualizations
        self.create_geographic_visualizations()
        
        # Generate recommendations
        self.generate_web_system_recommendations()
        self.generate_implementation_plan()
        
        # Save report
        self.save_analysis_report()
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("Check the following files:")
        print("- analysis_report.json: Complete analysis data")
        print("- analysis_report.md: Human-readable report")
        print("- visualizations/: Geographic visualizations")
        print("- project_plan.md: Implementation plan")

def main():
    """Main function to run the analysis."""
    excel_file = "Mex_trout_records_merge_2011_12_ver11+Abadia_DAH2024-05-10 (version 1).xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Error: Excel file '{excel_file}' not found!")
        return
        
    analyzer = MexicanTroutAnalyzer(excel_file)
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()

# Mexican Trout Biodiversity Project - Technical Implementation Plan

## Project Overview
Based on the email from Dean Hendrickson at the Cool Texas Fishes Biodiversity Lab, this project aims to create a modern web-based system for managing and displaying Mexican trout biodiversity data, replacing the discontinued Drupal-based system from the British Museum of Natural History.

## Current State Analysis

### Existing Data Sources
1. **Excel Database**: `Mex_trout_records_merge_2011_12_ver11+Abadia_DAH2024-05-10 (version 1).xlsx`
   - 350 core records with geographic coordinates
   - 10 sheets containing different data views and joins
   - Multiple species of Mexican trout with taxonomic classifications
   - Geographic coverage across major Mexican river basins

2. **Legacy System**: https://truchasmexicanas.myspecies.info/
   - Currently archived but still accessible
   - Contains occurrence data and specimen information
   - No longer updatable

3. **External Data Sources**:
   - IUCN Red List assessments for conservation status
   - Mexican national hydrography system (SIATL)
   - Alternative hydrographic datasets (Hydrosheds, GIRES, etc.)

## Key Requirements from Email

### Primary Objectives
1. **Replace the discontinued Drupal system** with a modern, maintainable web platform
2. **Enable continuous data updates** for occurrence records, specimen data, and metadata
3. **Integrate multiple data types**:
   - Occurrence data and specimen records
   - Geographic coverages (topography, meteorology, vegetation, hydrography)
   - Field notes and genetic data
   - Morphological analysis results
   - Conservation status assessments

### Technical Requirements
1. **Version-controlled data management** system
2. **Web publishing platform** for public access
3. **GIS integration** for hydrographic data comparison
4. **Database tools** for data cleaning and linking
5. **Comparison tools** for different hydrographic datasets

## Proposed Technical Solution

### 1. Data Architecture
```
├── Core Database (PostgreSQL/PostGIS)
│   ├── Occurrence Records
│   ├── Specimen Data
│   ├── Geographic Data
│   ├── Taxonomic Classifications
│   └── Metadata
├── Web Application (Python/Flask or Django)
│   ├── Public-facing website
│   ├── Data visualization tools
│   ├── GIS mapping interface
│   └── Admin interface for data management
└── Data Processing Pipeline
    ├── ETL scripts for data cleaning
    ├── GIS data integration
    └── Automated updates
```

### 2. Technology Stack
- **Backend**: Python (Flask/Django) with PostgreSQL/PostGIS
- **Frontend**: React.js with Leaflet/Mapbox for mapping
- **GIS**: GeoPandas, Shapely for spatial analysis
- **Data Processing**: Pandas, NumPy for data manipulation
- **Deployment**: Docker containers with cloud hosting

### 3. Key Features
- **Interactive Maps**: Display trout occurrences with hydrographic overlays
- **Data Comparison Tools**: Compare different hydrographic datasets
- **Species Pages**: Detailed information for each trout species
- **Conservation Status**: Integration with IUCN assessments
- **Data Export**: APIs for data access and download
- **Admin Interface**: Tools for data management and updates

## Implementation Phases

### Phase 1: Data Analysis and Cleaning (Week 1-2)
- [x] Analyze existing Excel data structure
- [ ] Clean and normalize data
- [ ] Design database schema
- [ ] Create data migration scripts

### Phase 2: Core Database Development (Week 3-4)
- [ ] Set up PostgreSQL/PostGIS database
- [ ] Implement data models
- [ ] Create data import scripts
- [ ] Develop basic API endpoints

### Phase 3: Web Application Development (Week 5-8)
- [ ] Build web application framework
- [ ] Implement mapping interface
- [ ] Create species information pages
- [ ] Develop admin interface

### Phase 4: GIS Integration (Week 9-10)
- [ ] Integrate Mexican hydrography data (SIATL)
- [ ] Implement alternative dataset comparison tools
- [ ] Create spatial analysis features
- [ ] Develop hydrographic data visualization

### Phase 5: Advanced Features (Week 11-12)
- [ ] Conservation status integration
- [ ] Genetic data linking
- [ ] Morphological analysis integration
- [ ] Field notes and metadata management

### Phase 6: Testing and Deployment (Week 13-14)
- [ ] Comprehensive testing
- [ ] Performance optimization
- [ ] Documentation
- [ ] Production deployment

## Data Sources Integration

### Hydrographic Datasets
1. **SIATL (Mexican National System)**: https://antares.inegi.org.mx/analisis/red_hidro/siatl/
2. **Hydrosheds**: https://www.hydrosheds.org/
3. **GIRES Database**: For intermittent rivers and ephemeral streams
4. **INEGI DEM**: 100m digital elevation models

### Conservation Data
- IUCN Red List assessments for each species
- Conservation status tracking
- Population trend analysis

### Genetic and Morphological Data
- Link to Abadia et al. (2015) genetic structure data
- Integration with Casey Dillman's morphometric data
- Field notes and collection metadata

## Success Metrics
1. **Data Completeness**: All 350+ records properly integrated
2. **Geographic Coverage**: Full mapping of Mexican trout distributions
3. **Data Quality**: Clean, normalized, and linked datasets
4. **User Access**: Public website with interactive features
5. **Maintainability**: Version-controlled, documented system
6. **Extensibility**: Framework for future data additions

## Next Steps
1. **Immediate**: Begin data cleaning and schema design
2. **Short-term**: Set up development environment and core database
3. **Medium-term**: Develop web application and GIS integration
4. **Long-term**: Deploy production system and begin data updates

## Contact Information
- **Project Lead**: Dean A. Hendrickson (Cool Texas Fishes Biodiversity Lab)
- **Technical Implementation**: Varun (AI Assistant)
- **Collaborators**: Casey Dillman, Joe Tomelleri, Dave Propst

---
*This plan addresses the key requirements from Dean's email and provides a roadmap for creating a modern, maintainable system for Mexican trout biodiversity data management and public outreach.*

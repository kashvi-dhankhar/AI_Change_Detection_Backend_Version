# AI Satellite Change Detection Backend

A production-ready backend system for automated satellite change detection using Google Earth Engine, Sentinel-1 (SAR), and Sentinel-2 imagery.

This backend analyzes satellite data across two time periods for a user-defined Area of Interest (AOI) and detects land cover changes including vegetation variation, water body changes, and urban expansion.

Built using Flask (Python), the system integrates directly with Google Earth Engine to perform large-scale geospatial analysis efficiently and reliably.

---

## Overview

This backend service allows users to:

- Upload an Area of Interest (KML file)
- Provide a start date and end date
- Automatically fetch Sentinel-2 optical imagery
- Automatically fetch Sentinel-1 SAR imagery (VV, VH polarizations)
- Compute spectral and radar-based indices
- Detect land cover changes using rule-based logic
- Receive output as a GeoJSON FeatureCollection

The output is GIS-compatible and can be integrated into mapping systems, dashboards, or analytical tools.

---

## Satellite Data Sources

Sentinel-2 (Optical Imagery)
- Used for vegetation, water, and urban detection
- Cloud-filtered imagery
- Used to compute:
  - NDVI (Vegetation Index)
  - NDWI (Water Index)
  - NDBI (Built-up Index)

Sentinel-1 (SAR Imagery)
- Uses VV and VH polarizations
- Useful in cloudy conditions
- Enhances detection reliability
- Supports structural and surface change identification

The combination of optical and SAR imagery improves robustness across different environmental conditions.

---

## Change Categories Detected

The system detects the following change types:

- Vegetation Loss
- Vegetation Gain
- Water Expansion
- Water Shrinkage
- Urban Expansion

Each detected change polygon includes:

- Change Type
- Area in square meters
- GeoJSON geometry

---

## Core Features

Automated Multi-Satellite Data Retrieval  
Fetches Sentinel-1 and Sentinel-2 imagery directly from Google Earth Engine.

Spectral and Radar-Based Processing  
Computes NDVI, NDWI, NDBI and incorporates VV/VH radar information.

Rule-Based Change Detection  
Applies interpretable threshold-based difference logic for classification.

GeoJSON Output  
Returns vectorized change polygons compatible with GIS platforms.

Threaded Execution  
Runs processing in a separate thread to prevent API blocking.

Live Status Streaming  
Uses Server-Sent Events (SSE) to stream real-time progress updates.

Single Task Execution Control  
Prevents simultaneous executions to maintain system stability.

---

## Technology Stack

Backend: Python (Flask)  
Geospatial Processing: Google Earth Engine  
Optical Data: Sentinel-2  
SAR Data: Sentinel-1 (VV, VH)  
Indices: NDVI, NDWI, NDBI  
Concurrency: Python Threading  
Output Format: GeoJSON  

---

## Installation & Setup

### 1. Clone Repository
### 2. Create Virtual Environment
### 3. Install Dependencies

---

## Google Earth Engine Setup (Important)

This project requires authentication with Google Earth Engine.

### Initial Authentication

Run the following command in your terminal:

Follow the browser login process and paste the verification code back into the terminal.

---

### Session Expiry & Re-Authentication (Important)

Google Earth Engine authentication tokens expire periodically (typically within 12–24 hours).

If you restart the project after some time and encounter authentication errors, you must re-authenticate manually by running:

This must be executed from the terminal before starting the Flask server again.

This behavior is expected and is due to session/token expiration in Google Earth Engine.

---

### Earth Engine Initialization

Ensure the correct project ID is configured inside the backend initialization:

Replace with the appropriate Google Earth Engine project ID.

---

## Processing Workflow

1. AOI is extracted from the uploaded KML file.
2. The date range is divided into two temporal periods.
3. Sentinel-2 imagery is retrieved for both periods.
4. Sentinel-1 VV/VH SAR imagery is retrieved.
5. Spectral and radar indices are calculated.
6. Difference layers are computed between time periods.
7. Threshold-based classification rules detect land cover changes.
8. Raster masks are converted to vector polygons.
9. Change polygons and area metrics are returned as GeoJSON.

---

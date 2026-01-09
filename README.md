# Image Retrieval System

A content-based image retrieval (CBIR) system that extracts objects from images and finds similar objects based on visual features using Local Binary Patterns (LBP) and histogram analysis.

## Overview

This project implements an intelligent image retrieval system that:
- Automatically detects and extracts objects from uploaded images
- Computes visual features using grayscale histograms and Local Binary Patterns (LBP)
- Searches for similar objects in a pre-indexed image database
- Supports multiple similarity metrics (Histogram Intersection and Cosine Distance)

## Features

### Image Processing
- **Object Detection & Extraction**: Uses contour detection to automatically identify and extract objects from images
- **Mask-based Segmentation**: Applies binary masks to isolate objects from backgrounds
- **Feature Extraction**: Combines grayscale histograms with LBP for robust feature representation

### Similarity Search
- **Histogram Intersection**: Measures the overlap between image histograms
- **Cosine Distance**: Computes similarity using cosine similarity between feature vectors

### Web Interface
- User-friendly web interface for uploading images
- Real-time visualization of search results
- Side-by-side comparison of input and matched objects

## Technologies

### Backend
- **Node.js** - Server-side JavaScript runtime
- **Express.js** - Web application framework
- **Multer** - File upload handling
- **Handlebars** - Template engine for dynamic views

### Image Processing
- **Python 3** - Image processing scripts
- **OpenCV (cv2)** - Computer vision operations
- **NumPy** - Numerical computations
- **Matplotlib** - Visualization and histogram generation

### Computer Vision Techniques
- **Local Binary Patterns (LBP)** - Texture descriptor for feature extraction
- **Contour Detection** - Object boundary detection
- **Canny Edge Detection** - Edge detection algorithm
- **Morphological Operations** - Image processing transformations
- **GrabCut** - Foreground/background segmentation (experimental)

## Project Structure

```
Image-Retrieval/
├── bin/                          # Python scripts for image processing
│   ├── processImages.py          # Main image processing pipeline
│   ├── grabcut.py                # GrabCut segmentation implementation
│   ├── histogram.py              # Histogram visualization
│   ├── intensity.py              # Intensity analysis
│   ├── RCNN.py                   # RCNN related code
│   └── www                       # Server startup script
├── routes/                       # Express route handlers
│   └── index.js                  # Main application routes
├── middleware/                   # Express middleware
│   └── processImage.js           # Image processing middleware
├── views/                        # Handlebars templates
│   ├── index.hbs                 # Main search page
│   └── searchResults.hbs         # Results display page
├── public/                       # Static assets
│   ├── images/
│   │   ├── indexed/              # Pre-indexed reference images
│   │   ├── imageObjects/         # Extracted object images
│   │   ├── binary/               # Binary masks for segmentation
│   │   ├── histograms/           # Generated histogram images
│   │   └── grayscale/            # LBP grayscale representations
│   ├── data/
│   │   └── data.json             # Feature database
│   ├── javascripts/              # Client-side JavaScript
│   └── stylesheets/              # CSS files
└── helpers/                      # Utility functions
    └── runPy.js                  # Python script execution helper

```

## Installation

### Prerequisites
- **Node.js** (v12 or higher)
- **Python 3.6+**
- **npm** (Node Package Manager)

### Required Python Packages
```bash
pip install opencv-python numpy matplotlib
```

### Required Node Packages
```bash
npm install
```

## Usage

### Starting the Server

1. Navigate to the project directory:
```bash
cd Image-Retrieval
```

2. Start the server:
```bash
npm start
```
or
```bash
node bin/www
```

3. Open your browser and navigate to:
```
http://localhost:3000
```

### Searching for Similar Images

1. **Select Similarity Method**:
   - Choose either "Histogram Intersection" or "Cosine Distance"

2. **Upload an Image**:
   - Click "Select Image" and choose an image file (PNG, JPEG, or GIF)

3. **View Results**:
   - The system will automatically extract objects from your image
   - Similar objects from the database will be displayed
   - Results are ranked by similarity score

## How It Works

### 1. Image Upload & Object Extraction
When an image is uploaded:
- A binary mask is applied to isolate foreground objects
- Canny edge detection identifies object boundaries
- Contour detection finds connected components
- Bounding boxes are computed and objects are extracted

### 2. Feature Extraction
For each extracted object:
- Image is converted to grayscale
- Local Binary Patterns (LBP) are computed for texture analysis
- Grayscale histogram is calculated
- Features are concatenated into a feature vector

### 3. Similarity Search
The system compares the input object's features against the database:
- **Histogram Intersection**: `min(a, b) / sum(b)`
- **Cosine Distance**: `dot(a, b) / (||a|| * ||b||)`

### 4. Results Display
- Top K most similar objects are returned
- Results include the original indexed image reference
- Visualizations show histograms and LBP representations

## API Endpoints

### `GET /`
Main search page with upload form

### `POST /search`
- **Description**: Upload and search for similar images
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameters**:
  - `image_file`: Image file to search (required)
  - `method`: Similarity method - "intersection" or "cosine" (required)
- **Response**: Renders search results page

### `GET /data`
- **Description**: Retrieve the feature database
- **Response**: JSON array of image features

## Database Structure

The feature database (`public/data/data.json`) stores:
```json
{
  "id": "A1_0",
  "image_path": "../public/images/imageObjects/A1_0.png",
  "parent_path": "../public/images/indexed/A1.png",
  "feature": [/* 512-dimensional feature vector */]
}
```

## Development Notes

### Pre-processing Images
To index new images:
1. Place images in `public/images/indexed/`
2. Create corresponding masks in `public/images/binary/`
3. Run the extraction script:
```python
python bin/processImages.py
```

### Generating Visualizations
Uncomment the relevant sections in `processImages.py`:
- `make_hist(images)` - Generate histogram images
- `make_gray(images)` - Generate LBP grayscale images

## Future Enhancements
- Support for additional similarity metrics (Chi-square, Bhattacharyya distance)
- Deep learning-based feature extraction (CNN features)
- Real-time RCNN object detection integration
- Improved GrabCut segmentation interface
- Database support for larger image collections
- Batch image upload and processing

## License
This project is available for educational and research purposes.

## Contributors
- Eddie Fu
- Cristobal Padilla

## Acknowledgments
Built as a term project for CSC 664 - Computer Vision.

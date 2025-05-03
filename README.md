# Image Color Analysis Application

This application analyzes images from an Excel file to determine if they are single-colored images. It processes image URLs from an Excel file and provides detailed analysis of each image.

## Features

- Upload Excel files containing image URLs
- Process multiple images in batch
- Detect if images are single-colored
- Display RGB color values
- Show processing time for each image
- Progress tracking with visual feedback
- Robust error handling and file management

## Requirements

- Python 3.7+
- Required Python packages (install using `pip install -r requirements.txt`):
  - streamlit
  - pandas
  - openpyxl
  - Pillow
  - numpy
  - opencv-python
  - requests

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage or Workflow

1. Prepare your Excel file:
   - Create an Excel file with a column named 'upload_links'
   - Add image URLs in one of these formats:
     - Direct URL: `https://example.com/image.jpg`
     - JSON array: `["https://example.com/image.jpg"]`
     - JSON object: `{"url": "https://example.com/image.jpg"}`

2. Run the application:
```bash
streamlit run streamlit_app.py
```

3. In the web interface:
   - Upload your Excel file using the file uploader
    **new data set that we got upload that
   - Click "Analyze Images" to start processing
   - View results for each image:
     - The image itself
     - Whether it's a single color
     - The RGB color value
     - Processing time

## Output

For each image, the application displays:
- The image preview
- Analysis results:
  - Single color status (Yes/No)
  - RGB color values
  - Processing time in seconds

## Error Handling

The application includes robust error handling for:
- Invalid Excel files
- Missing or malformed URLs
- Failed image downloads
- File access issues
- Processing errors

## Notes

- The application automatically filters out empty cells in the Excel file
- Temporary files are automatically cleaned up after processing
- Progress is tracked and displayed during batch processing
- The application supports various URL formats and JSON structures

## Troubleshooting

If you encounter any issues:
1. Ensure your Excel file has the correct column name ('upload_links')
2. Verify that your URLs are accessible
3. Check that all required dependencies are installed
4. Ensure you have write permissions in the temporary directory

## License

This project is open source and available under the MIT License. 
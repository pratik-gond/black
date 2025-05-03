import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io
import os
from black_image_detector import is_single_color_image
import tempfile
import json
import time

def get_image_url(row):
    try:
        if 'upload_links' not in row or pd.isna(row['upload_links']) or not row['upload_links']:
            return None
        
        # Handle different representations of the URL
        url_data = row['upload_links']
        
        # If it's already a string, process it
        if isinstance(url_data, str):
            # Remove any surrounding quotes that might be present
            cleaned_url = url_data.strip('"\'')
            
            # Try parsing as JSON if it looks like JSON
            if (cleaned_url.startswith('[') and cleaned_url.endswith(']')) or (cleaned_url.startswith('{') and cleaned_url.endswith('}')):
                try:
                    parsed_data = json.loads(cleaned_url)
                    if isinstance(parsed_data, list) and parsed_data:
                        return parsed_data[0]
                    elif isinstance(parsed_data, dict) and 'url' in parsed_data:
                        return parsed_data['url']
                except json.JSONDecodeError:
                    # Not valid JSON, treat as direct URL
                    pass
            
            # Direct URL (clean it)
            return cleaned_url
            
    except Exception as e:
        st.error(f"Error parsing upload_links: {e}")
        return None

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        return None
    except Exception as e:
        st.error(f"Error downloading image: {str(e)}")
        return None

def safe_delete_file(file_path, max_retries=3, delay=0.5):
    """Safely delete a file with retries and delay"""
    for attempt in range(max_retries):
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                st.warning(f"Could not delete temporary file {file_path}: {str(e)}")
                return False

def main():
    st.title("Image Color Analysis")
    st.write("Upload an Excel file containing image URLs to analyze them.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Filter out empty cells and get valid image URLs
            filtered_df = df[~df['upload_links'].isna() & (df['upload_links'] != '')]
            total_rows = len(df)
            
            st.write(f"\nFound {len(filtered_df)} entries with images to analyze out of {total_rows} total entries")
            
            if len(filtered_df) == 0:
                st.warning("No valid image URLs found in the upload_links column.")
                return
            
            if st.button("Analyze Images"):
                # Create a progress bar
                progress_bar = st.progress(0)
                
                # Process each image
                for idx, row in filtered_df.iterrows():
                    st.write(f"\nProcessing image {idx + 1} of {len(filtered_df)}")
                    
                    # Get image URL using the parsing function
                    url = get_image_url(row)
                    if url is None:
                        st.error(f"Failed to parse URL from row {idx + 1}")
                        continue
                    
                    # Download image
                    img = download_image(url)
                    if img is None:
                        st.error(f"Failed to download image from URL: {url}")
                        continue
                    
                    # Create temporary file
                    tmp_file = None
                    try:
                        # Save image temporarily
                        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                        tmp_file.close()  # Close the file handle
                        
                        # Save the image
                        img.save(tmp_file.name)
                        
                        # Analyze image
                        is_single_color, color, execution_time = is_single_color_image(tmp_file.name)
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.image(img, caption=f"Image {idx + 1}")
                        
                        with col2:
                            st.write("Analysis Results:")
                            st.write(f"Single Color: {'Yes' if is_single_color else 'No'}")
                            st.write(f"Color (RGB): {color}")
                            st.write(f"Processing Time: {execution_time:.3f} seconds")
                        
                    finally:
                        # Clean up temporary file
                        if tmp_file and os.path.exists(tmp_file.name):
                            safe_delete_file(tmp_file.name)
                    
                    # Update progress bar
                    progress_bar.progress((idx + 1) / len(filtered_df))
                
                st.success("Analysis complete!")
                
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")

if __name__ == "__main__":
    main() 
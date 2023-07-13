import base64
import os
import shutil
import zipfile
import sys
def create_installer(input_path, output_path):
    # Convert input to zip
    temp_zip_path = 'temp.zip'
    if os.path.isfile(input_path):
        with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
            zipf.write(input_path, os.path.basename(input_path))
    elif os.path.isdir(input_path):
        shutil.make_archive(temp_zip_path, 'zip', input_path)
    else:
        print('Invalid input path.')
        return
    # Convert zip to base64
    with open(temp_zip_path, 'rb') as zip_file:
        base64_data = base64.b64encode(zip_file.read()).decode('utf-8')
    # Write base64 data to output file
    with open(output_path, 'w') as output_file:
        output_file.write(base64_data)
    # Clean up temporary zip file
    os.remove(temp_zip_path)
def extract_installer(input_path, output_path):
    # Read base64 data from input file
    with open(input_path, 'r') as input_file:
        base64_data = input_file.read()
    # Convert base64 to zip
    temp_zip_path = 'temp.zip'
    with open(temp_zip_path, 'wb') as zip_file:
        zip_file.write(base64.b64decode(base64_data))
    # Extract zip to output path
    if output_path.endswith('.zip'):
        shutil.move(temp_zip_path, output_path)
    else:
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_path)
    # Clean up temporary zip file
    os.remove(temp_zip_path)
if len(sys.argv) == 2:
    if sys.argv[1].endswith(".ins"):
        extract_installer(sys.argv[1], os.path.dirname(sys.argv[1]))
    else:
        create_installer(sys.argv[1], os.path.splitext(sys.argv[1])[0] + ".ins")
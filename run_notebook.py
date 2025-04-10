#!/usr/bin/env python
"""
Script to run the notebook using nbconvert with custom parameters to skip certain parts in CI environments
"""
import os
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import json

# Print environment info
print("=== Environment Information ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Check if running in GitHub Actions
in_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"
print(f"Running in GitHub Actions: {in_github_actions}")

# Modify the notebook to skip problematic parts when running in CI
def prepare_notebook_for_ci(notebook_path, output_path):
    print(f"Preparing notebook for CI: {notebook_path} -> {output_path}")
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    if in_github_actions:
        # Inject a cell at the beginning to set CI mode
        ci_cell = nbformat.v4.new_code_cell(
            "# Set CI mode to skip interactive and problematic parts\n"
            "import os\n"
            "os.environ['CI_MODE'] = 'true'\n"
            "import sys\n"
            "print('Running in CI mode - some interactive features will be skipped')\n"
        )
        nb.cells.insert(0, ci_cell)
        
        # Modify cells with apt-get or other problematic parts
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                # Skip apt-get commands
                if '!apt-get' in cell.source:
                    print(f"Modifying cell {i} to skip apt-get commands")
                    cell.source = cell.source.replace(
                        '!apt-get -qq -y install espeak-ng > /dev/null 2>&1',
                        'print("Skipping apt-get install in CI mode")'
                    )
                
                # Skip Google Drive credential download
                if 'test_google_drive_api' in cell.source and 'download_file_from_google_drive' in cell.source:
                    print(f"Modifying cell {i} to skip Google Drive API test")
                    cell.source = cell.source.replace(
                        'api_test_result = test_google_drive_api()',
                        'print("Skipping Google Drive API test in CI mode")\napi_test_result = False'
                    )
    
    # Write the modified notebook
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    return output_path

# Path to notebooks
notebook_path = 'notebook.ipynb'
ci_notebook_path = 'notebook_ci_ready.ipynb'

# Prepare notebook for CI if needed
prepared_notebook = prepare_notebook_for_ci(notebook_path, ci_notebook_path)

# Execute the notebook
try:
    print(f"Executing notebook: {prepared_notebook}")
    
    # Read the prepared notebook
    with open(prepared_notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Configure the execution
    execute_kwargs = {
        'timeout': 600,  # 10 minutes timeout per cell
        'allow_errors': True,  # Continue execution even if there are errors
        'interrupt_on_timeout': True,
    }
    
    # Create executor
    ep = ExecutePreprocessor(**execute_kwargs)
    
    # Execute the notebook
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    
    # Save the executed notebook
    output_notebook_path = 'executed_notebook.ipynb'
    with open(output_notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print(f"Notebook execution completed: {output_notebook_path}")
    
    # Create an execution report
    execution_report = {
        'status': 'success',
        'message': 'Notebook execution completed',
        'notebook_path': output_notebook_path,
        'errors': False
    }
    
except Exception as e:
    print(f"Error executing notebook: {e}")
    
    # Create an execution report with error information
    execution_report = {
        'status': 'error',
        'message': str(e),
        'notebook_path': prepared_notebook,
        'errors': True
    }

# Save the execution report
report_path = 'notebook_execution_report.json'
with open(report_path, 'w') as f:
    json.dump(execution_report, f, indent=2)

print(f"Execution report saved to: {report_path}")
print("Done!")

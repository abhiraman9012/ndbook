# Running Jupyter Notebook with GitHub Actions

This repository contains a Jupyter notebook that can be automatically executed via GitHub Actions.

## Workflow Setup

The GitHub Actions workflow is configured to run the notebook whenever code is pushed to the `main` branch, a pull request is made to the `main` branch, or when manually triggered from the Actions tab.

## Required Secrets

To run the notebook successfully, you need to set up the following secret in your GitHub repository:

- `GEMINI_API_KEY`: Your Google Gemini API key

### How to Add Secrets to Your GitHub Repository

1. Go to your GitHub repository
2. Click on "Settings" 
3. In the left sidebar, click on "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Enter the name `GEMINI_API_KEY` and paste your API key as the value
6. Click "Add secret"

## Google Drive Integration

The notebook contains code that interacts with Google Drive. For this to work in GitHub Actions, you'll need to:

1. Store your Google Drive service account credentials as a GitHub secret, or
2. Modify the notebook to skip Google Drive operations when running in GitHub Actions

## Running the Workflow Manually

To run the notebook manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Run Jupyter Notebook" workflow
3. Click "Run workflow"
4. Choose the branch to run from and click "Run workflow"

## Viewing Results

After the workflow completes, you can download the executed notebook from the "Artifacts" section of the workflow run page.

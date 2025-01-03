# Financial Analysis Project

## Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Create .env file with required API keys
5. Run the project: `python src/main.py`

## Project Structure
- src/
  - data_collection/ - Data collection modules
  - analysis/ - Analysis modules
  - report/ - Report generation modules
  - config.py - Configuration settings
  - main.py - Main entry point

## Configuration
Set the following environment variables in .env:
- NEWS_API_KEY
- ALPHA_VANTAGE_KEY 
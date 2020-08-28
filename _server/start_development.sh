# Create venv if not exits.
python3 -m venv venv

# Activate venv.
source venv/bin/activate

# Install requirements.txt
pip install -r requirements.txt

# Run as development server.
python3 main.py


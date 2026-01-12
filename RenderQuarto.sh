
ECHO Creating virtual environment: .venv/,
python3 -m venv .venv

ECHO Activating .venv
source .venv/bin/activate

ECHO Installing necessary dependencies
pip install quarto jupyter numpy matplotlib plotly pandas

ECHO Rendering
quarto render


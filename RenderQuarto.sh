
echo Creating virtual environment: .venv/ using Python 3.11
python3.11 -m venv .venv

echo Activating .venv
source .venv/bin/activate

echo Installing necessary dependencies
pip install pyyaml jupyter numpy matplotlib plotly pandas

echo Setting QUARTO_PYTHON to the venv Python
export QUARTO_PYTHON=$(which python)

echo Rendering
quarto render


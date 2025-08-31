## Setup Environment - Anaconda
```
conda create --name main-ds python=3.13
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir dashboard
cd dashboard
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app local
```
streamlit run dashboard.py
```
## Run app online 
```
https://dashboardterlaris.streamlit.app/
```
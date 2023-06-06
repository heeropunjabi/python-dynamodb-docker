# Prerequiesites ( for mac users only )

    brew install python3
    brew install pyenv
    pyenv install 3.9
    pyenv global <version-number>

# Run Project Locally

    python -m venv venv # create virtual envt
    pip install -r requirements.txt

# Run Docker container for dynamodb

    docker pull amazon/dynamodb-local
    docker run -p 8000:8000 amazon/dynamodb-local

# Create Table, Write into table and get data from table

    python main.py

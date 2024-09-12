# Virtual Environment

## Setup

Creating a virtual environment is different depending on the OS:

<details><summary>macOS</summary>

#### Creating the Virtual Environment:

````
python3 -m venv "project_path/.venv"
````

#### Activating the Virtual Environment:

````
source .venv/bin/activate
````

</details>

<details><summary>Windows</summary>

#### Creating the Virtual Environment:

````
python3 -m venv "project_path\.venv"
````

#### Activating the Virtual Environment:

````
.venv\Scripts\activate
````

</details>

#### Deactivating the Virtual Environment:

````
deactivate
````

## Resources

* [Creation of Virtual Environments](https://docs.python.org/3/library/venv.html)

* [Using pip in a Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

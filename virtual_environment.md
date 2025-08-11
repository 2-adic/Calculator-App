## Virtual Environment

A virtual environment isolates project-specific dependencies from the global Python installation.

## Setup

*All commands shown below are run from the project's root directory.*

### Creating the Virtual Environment:

````
python -m venv .venv
````

### Activating the Virtual Environment:

*This step is a bit different depending on the OS.*

<details><summary>macOS</summary>

````
source .venv/bin/activate
````

</details>

<details><summary>Windows</summary>

````
.venv\Scripts\activate
````

</details>

### Deactivating the Virtual Environment:

````
deactivate
````

## Resources

* [Creation of Virtual Environments](https://docs.python.org/3/library/venv.html)

* [Using pip in a Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

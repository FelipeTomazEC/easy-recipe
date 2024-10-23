# Easy Recipe

Easy Recipe is a web application built with [Django](https://www.djangoproject.com/start/) that allows users to manage ingredients and recipes in an easy manner.

You can access Easy Recipe at https://easy-recipe-w3cg.onrender.com

### Features

- Register ingredients;
- Edit ingredients;
- Visualization of all ingredients registered in the system;
- Search for ingredients based on EAN or name;
- Register recipes;
- Edit recipes;
- View all recipes registered in the system;
- See the details of a given recipe (ingredients that are used, cost by ingredient and total cost).

### Getting Started

Following the instructions down below you'll get a copy of the project, so you can run it from your local machine.

#### Requirements
Before running this project locally, make sure you have installed:

- **Docker/Docker Compose**: You can check how to install following the [docs](https://docs.docker.com/engine/install/).
- **Git**: Ensure Git is installed and accessible from the command line.
- **Python 3.10** or later: You can download it from [here](https://www.python.org/downloads/) or use your preferred package manager.
- **Poetry 1.8.** or later: You can install by following the instructions [here](https://python-poetry.org/docs/#installation).

To verify your installations, run the following commands:

```bash
git --version
poetry --version
python --version
docker --version
```

### Running this project locally

1. Clone the repository to your local machine:
   `$ git clone https://github.com/FelipeTomazEC/easy-recipe.git`

2. Enter the directory of the project:
   `$ cd easy-recipe`

3. Install project's dependencies:
   `$ poetry install`

4. Make a copy of the `example.env` file, and name it as `.env`:
   `$ cp .env.example .env`

5. Start a local database (via docker):
    `$ docker compose up`

6. Run database migrations:
    `$ python manage.py migrate`

7. Start the application:
    `$ python manage.py runserver`

5. That's all. Easy Recipe home page will be available at http://localhost:8000/;
# Mini Project for System Engineer Class - PokeAPI

This project is developed as part of the Mini Project for the System Engineer class. It aims to provide practical experience with a variety of technologies and tools relevant in the field of system engineering and software development.

## Topics Covered

The project encompasses a wide range of topics and technologies including:

- **Python - Flask**: Used for backend development, creating RESTful APIs that serve data.
- **ReactJS**: Employed for the frontend development to create a dynamic and responsive user interface.
- **SQL**: Utilized for database management, ensuring data is stored, retrieved, and manipulated efficiently.
- **Docker**: Containers are used to package the application and its dependencies, ensuring consistency across different development and deployment environments.
- **Monitoring Tools and Logging (NewRelic)**: NewRelic is integrated for monitoring application performance and logging, offering insights into the application's operational aspects.
- **CI/CD in Github**: Continuous Integration and Continuous Deployment processes are implemented using GitHub Actions, ensuring automated testing and deployment.
- **Kubernetes with GKE (Google Kubernetes Engine)**: Kubernetes is used for orchestrating the containerized applications, managing deployment, scaling, and operations of application containers across clusters of hosts.
- **API Integration**: The project integrates with the [PokeAPI](https://pokeapi.co) to fetch data about Pokémon for various functionalities within the application.
- **And other knowledge**: Includes other essential knowledge areas such as security best practices, API rate limiting, and efficient resource management.

## Getting Started

### Prerequisites

Before you begin, ensure you have installed all of the following prerequisites on your development machine:

- Git - [Download & Install Git](https://git-scm.com/downloads).
- Docker - [Download & Install Docker](https://www.docker.com/get-started).
- Kubernetes - [Install and Set Up kubectl](https://kubernetes.io/docs/tasks/tools/).
- Google Cloud SDK - For GKE, [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

### Clone The Project

To get started with the project, clone the repository to your local machine:

```bash
git clone https://github.com/fawwaz26/Mini-Project-Syseng-PokeAPI
cd Mini-Project-Syseng-PokeAPI

### Backend Setup

'''bash
cd flask
pip install -r requirements.txt
flask run

### Frontend Setup

'''bash
cd pokedex
npm install
npm start




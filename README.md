# Containerized application BearingPoint Hackathon
This GitHup repository will take you through how to deploy an application in the cloud using a Docker Image for your application. The application is a Python web application using the visualization library Dash.

## Competency prerequisites
There are no required prerequisites to complete the tasks in the hackathon, but some previous knowledge is benefitial:
- Familiar with Python, managing libraries and virtual environments
- Basic command line experience
- Familiar with what Docker is used for
- Familiar with cloud services such as AWS/Azure

## Step 0. Getting set ut before the hackathon
Before the hackathon you should have the following installed on your computer. How to install each component is described below.
- Python 3 (recommended, not mandatory) 
- Git
- Docker  ([Guide](https://docs.docker.com/get-docker/))
- Have an [AWS account.](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc)
- Have the [AWS Command Line Interface (CLI) installed](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). Version 2 is the newest version and recommended, if you already have Version 1 installed then that's fine.
### Installing Python 3 (optional but recommended)
It is recommended to have Python 3 installed on your computer before the hackathon. This will allow you to test the application on your own computer before we deploy it to the cloud.

You can install Python 3 by following [this guide for Windows](https://phoenixnap.com/kb/how-to-install-python-3-windows) or [this guide for Mac](https://docs.python-guide.org/starting/install3/osx/). Make sure that you also install pip, a package installer for Python (this is included in both guides).

You can verify that your Python and pip installation worked by running the below commands in a terminal/command prompt window

    # Verify python
    $ python --version

    # Verify pip
    $ pip --version
### Installing git
Git can be installed [here](https://git-scm.com/downloads). In this lab we will be cloning a repository from GitHub, you do not need a GitHub account in order to do this. If you do however want to start using GitHub as well, check out [this introduction to git and GitHub](https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners).

You can verify that the git installation worked running the below command in your terminal.
    
    # Check git installation
    $ git --version

### Installing Docker
Instructions on how to install Docker can be found [here](https://docs.docker.com/get-docker/).

You can verify the installation by running the below command in your terminal.

    # Verify docker installation
    $ docker --version

### Creating an AWS account
Creatnig an AWS account is free and can be done [here](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc).

### Installing the AWS Command Line Interface (CLI)
The AWS CLI is a way to programatically interact with AWS. The CLI allows for users to create and manage resources though a command prompt/terminal instead of through the AWS Console.

Instructions for installing the AWS CLI can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html). We recommend using version 2 of the CLI, if you already have version 1 installed instructions will be provided with both version 1 and 2 in this hackathon (there are some breaking differences).

You now have everything set up and are ready to start!

## Step 1: Cloning the GitHub repository 
In the hackathon we will deploy a Dash application on AWS. If you already have a Python Dash application on your computer you can use this as your base application, if not you can clone this GitHub repository.

To clone the repository, use the command prompt to navigate to the directory (folder) on your local computer where you want the repository to be stored and run the below command.

    $ git clone https://github.com/mattimoller/ContainerizedApps-Cloud-hackathon.git

You should now see that a folder has been created with the code for the dash application.

## Step 2 (Optional): Running the application locally on your computer
Before we deploy the application using Docker in AWS we can try running the application locally first. To do this we first need to create a virtual environment and install the required Python packages.

To create a virtual environment named 'venv', you first need to have the package `virtualenv` installed. See the below commands to check if virtualenv is installed, and install it if it is not.

    # Check if virtualenv is installed
    $ virtualenv --version
    # Install virtualenv using pip
    $ pip install virtualenv

Once the library is installed we can create the virtual environment and activate it as shown below. The environment will be created in your current directory in a folder we name "venv". In the .gitignore file that is a part of the repository you will notice that it is explicitly stated that we do not want to include the virtual environment as a part of our repository. This is best practice.

    # Create the environment
    $ virtualenv venv
    # Activate the environment
    $ /venv/Scripts/activate.bat

Now that the environment is created we can install the required packages by installing the packages needed. They are listed in the requirements.txt-file that was downloaded when the repository was cloned from GitHub and pip allows us to we install the packages using this file.

    $ pip install -r requirements.txt

Once the installation is complete the packages required to ron the application should be installed. The application is run from the index.py-file, before being run you however need to make one small change on the last lines of this file. The file should be modified so that the server and app.run_Server-line reads as below. This is also specified in the file.

    app.run_Server(debug=True)

You can now view the dashboard at by opening a web browser and entering the address [http://127.0.0.1:8050/](http://127.0.0.1:8050/). Stop the application by entering ctrl+C in your command line.

At this stage you can play around with the application code as desired and modify it as you want, as long as it is still running. Remember to add any new packages you install to the requirements.txt file.

If you have run the application locally, also remember to change the last line of the index.py-file so that it can be deployed with Docker on AWS.

## Step 3: Creating our Docker image
Now that we have the application on our local computer we can create a Docker image of the application. This image will in turn be uploaded to AWS and create the basis for running our application on cloud infrastructure.

A Docker image is created from a Dockerfile, this Dockerfile is what we will now create. The Dockerfile will be created from the base image continuumio/miniconda3. For a more thorough explanation of Dockerfile syntax [this article](https://betterprogramming.pub/what-goes-into-a-dockerfile-ff0ace591060) explains the commands we use.

The complete Dockerfile specification is given below.

    FROM continuumio/miniconda3
    WORKDIR "/app"
    COPY . .
    RUN conda install pip
    RUN pip install -r requirements.txt
    EXPOSE 8050
    ENTRYPOINT [ "python3" ]
    CMD [ "index.py" ]

The commands are shortly explained below:
- FROM: Copies the base image
- WORKDIR: sets /app as the workind directory, since this directory does not exist it is first created then set as the working directory
- COPY: Copies the files in our current local directory to the Docker image, except for the ones specified in our .dockerignore file
- RUN: Used to run commands on our server, here we first install pip and then use pip to install the required packages from requirements.txt
- EXPOSE 8050: Exposes port 8050 on the applicaion server, this is the port our application uses
- ENTRYPOINT: default command to execute at runtime (when the container starts)
- CMD: Command to run the application

Now that you have the Dockerfile ready our Docker image can be created. This is done by running one simple command in your terminal. Note that the command must be run from the directory where your Dockerfile is stored (the " . " tells Docker to look for a Dockerfile in the current directory)

    docker build -t hackathon_dashboard .

Docker will now line-by-line execute your Dockerfile commands, you can follow the progress in your terminal. When the build is complete you can try running the image on a Docker container on your local computer before we upload it to AWS. This can again be done with one command and if no errors occur your build was successful.

    docker run hackathon_dashboard

Accessing the application can be quite tricky due to the port mappings used in Docker. As long as you know your application is running successfully you are OK to move on th the next stage.

To stop the running container you first need to find its name. This can be done by running `docker ps` which lists all running containers. You can then run the command `docker stop <container_name>` to stop the container. Verify that the container stopped succesfully by running `docker ps` again, which should now be empty.

## Step 4: Uploading our image to AWS



## Installation
Download the necessary packages (pip install requirements.txt)
then `python index.py` and then look at the beautiful dashboard at [http://127.0.0.1:8050/](http://127.0.0.1:8050/)



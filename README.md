# Containerized application BearingPoint Hackathon
This GitHub repository will take you through how to deploy an application on AWS using a Docker Image for your application. The application is a Python web application using the visualization library Dash.

## Competency prerequisites
There are no required prerequisites to complete the tasks in the hackathon, but some previous knowledge is benefitial.
- Familiar with Python, managing libraries and virtual environments
- Basic command line experience
- Familiar with what Docker is used for
- Familiar with cloud services such as AWS/Azure

## Step 0. Getting set up before the hackathon
Before the hackathon you should have the following installed on your computer. How to install each component is described below.
- Python 3 (recommended, not mandatory. [Windows guide](https://phoenixnap.com/kb/how-to-install-python-3-windows), [Mac guide](https://docs.python-guide.org/starting/install3/osx/)) 
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
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
Before we deploy the application using Docker on AWS we can try running the application locally first. To do this we first need to create a virtual environment and install the required Python packages.

To create a virtual environment named 'venv' you first need to have the package `virtualenv` installed. See the below commands to check if virtualenv is installed, and install it if it is not.

    # Check if virtualenv is installed
    $ virtualenv --version
    # Install virtualenv using pip
    $ pip install virtualenv

Once 'venv' is installed we can create the virtual environment and activate it as shown below. The environment will be created in your current directory in a folder we name "venv". In the .gitignore file that is a part of the repository you will notice that it is explicitly stated that we do not want to include the virtual environment as a part of our repository. This is best practice.

    # Create the environment
    $ virtualenv venv
    # Activate the environment
    $ /venv/Scripts/activate.bat

Now that the environment is created we need to install the required packages to our environment. They are listed in the requirements.txt file that was downloaded when the repository was cloned from GitHub and pip allows us to install the packages using this file.

    $ pip install -r requirements.txt

Once the installation is complete the packages required to run the application should be installed. The application is run from the index.py file, before being run you however need to make one small change on the last lines of this file. The file should be modified so that the last line reads `app.run_Server(debug=True)`, instead of `app.run_server(host='0.0.0.0', port=8050, debug=True)`. This is also specified in the file.

To run the application simply enter the command `$ python index.py` in the terminal. You can now view the dashboard by opening a web browser and entering the address [http://127.0.0.1:8050/](http://127.0.0.1:8050/). Stop the application by pressing Ctrl+C while in your terminal.

At this stage you can play around with the application code as desired and modify it as you want, as long as it is still running. Remember to add any new packages you install to the requirements.txt file.

If you have run the application locally, also remember to change the last line of the index.py file so that the last line reads  `app.run_server(host='0.0.0.0', port=8050, debug=True)`. This will ensure our deployment using Docker works as expected.

## Step 3: Creating our Docker image
Now that we have the application on our local computer we can create a Docker image of the application. This image will in turn be uploaded to AWS and create the basis for running our application on cloud infrastructure.

A Docker image is created using a Dockerfile, this file provides instructions on which packages the application needs and how the application is run. For our use case we will create our image from another base image *continuumio/miniconda3*. For a more thorough explanation of Dockerfile syntax [this article](https://betterprogramming.pub/what-goes-into-a-dockerfile-ff0ace591060) explains the commands we use.

The complete Dockerfile specification is given below, the file can be stored in the same location as your application code. The Dockerfile should be stored without a file type ending, i.e it's name should just be "Dockerfile", not "Dockerfile.txt".

    FROM continuumio/miniconda3
    WORKDIR "/app"
    COPY . .
    RUN conda install pip
    RUN pip install -r requirements.txt
    EXPOSE 8050
    ENTRYPOINT [ "python3" ]
    CMD [ "index.py" ]

The commands are shortly explained below:
- **FROM**: Copies the base image
- **WORKDIR**: sets /app as the working directory, since this directory does not exist it is first created then set as the working directory.
- **COPY**: Copies the files in our current local directory to the Docker image, except for the ones specified in our .dockerignore file.
- **RUN**: Used to run commands on our container, here we first install pip and then use pip to install the required packages from requirements.txt.
- **EXPOSE**: Exposes port 8050 on the applicaion server, this is the port our Dash application uses.
- **ENTRYPOINT**: default command to execute at runtime (when the container starts).
- **CMD**: Command to run the application.

Once you have stored your Dockerfile the Docker image can be created. This is done by running one simple command in your terminal. Note that the command must be run from the directory where your Dockerfile is stored (the " . " tells Docker to look for a Dockerfile in the current directory). The name of the image is set to hackathon_dashboard, you can change this if you want.

    $ docker build -t hackathon_dashboard .

Docker will now execute the Dockerfile commands line by line and you can follow the progress in your terminal. The build should finish without any error messages but may take a minute or two due to the Python package installation. 

When the build is complete you can try running the image on a Docker container on your local computer before we upload it to AWS. This can again be done with one command and if no errors occur your build was successful.

    $ docker run hackathon_dashboard

Your terminal should now say that your application is running (see below screenshot). Accessing the application can however be quite tricky due to the networking configuration used in Docker. I have not been able to figure out exactly why the application can't be accessed at the given address but will update with new information if i find any. As long as you know your application is running successfully you are OK to move on to the next stage.

![Terminal message when app is running sucessfully on your local Docker Container](/assets/ReadMe/DockerAppRunSuccess.PNG)


To stop the application press Ctrl+C in your terminal. To stop the running container you first need to find its name, this can be done by running `docker ps` which lists all running containers. You can then run the command `docker stop container_name` to stop the container. Verify that the container stopped succesfully by running `docker ps` again, which should now be empty.

## Step 4: Uploading our image to AWS
In this part we will upload our image to the Elastic Container Repository (ECR) in AWS. We will do this using the AWS CLI.

There are several ways to interact with AWS. One is via the [AWS Management Console](https://aws.amazon.com/console/), another is via the AWS CLI. Today we will use both ways of interacting with AWS. We will start by logging in to the [AWS Management Console](https://aws.amazon.com/console/). If you have not previously used AWS and have no IAM users you can use the root account, you should however be aware that your root account has unrestricted access to all AWS resources and AWS best practice is to create IAM Users with only the required access (if you are curious you can read more about [AWS Security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)). 

Once logged in to the console, check which region you are in (top right) and make sure that you remain in the same region for the remainder of the hackathon. The standard AWS region is N. Virginia, also named us-east-1. In us-east-1 the newest AWS features will always be available, new features are typially launched there first.

![Current AWS Region](/assets/ReadMe/MyRegion.png)


### Step 4a: Creating an access key
There are several ways to interact with AWS. One is via the [AWS Management Console](https://aws.amazon.com/console/), another is via the AWS CLI. Today we will use both ways of interacting with AWS.

To use the AWS CLI we need an access key pair which needs to be generated in the AWS Management Console. To create an access key go to *My Seurity Credentials* by clicking on your account name in the top right hand corner once you are logged in to the console.

![My security credentials](/assets/ReadMe/MySecurityCredentials.PNG)

From this page, click on *Access keys (access key ID and secret access key)* and *Create New Access Key*. The key will be downloaded on your computer, make sure to save it somewhere. You will nor be able to download it again and if it is lost you will need to generate a new key pair.

### Step 4b: Create an Elastic Container Repository (ECR)
The AWS service which manages container orchestration is called Elastic Compute Service (ECS). You can navigate to ECS by searching for it in the search bar, or by pressing services in the top left window (ECS can be found under *Containers*).

Once on the ECS landing page, navigate to *Repositories* in the menu on the left side. Once in the repositories page, press *Create repository*. Create the repository as a pricate repository and give it a fitting name, leave everything else as default.

![Repository creation](/assets/ReadMe/Createrepository.png)

Now that we have ceated our repository we are ready to upload our Docker image.

### Step 4c: Uploading our Docker Image to AWS
We will now use the AWS CLI to upload our Docker image to AWS. This assumes you have the AWS CLI installed on your compute (see [Step 0. Getting set up before the hackathon](#step-0-getting-set-up-before-the-hackathon)).

Before uploading our image we need to configure our AWS access in the CLI. This is done in the terminal with the below commands and your previously downloaded access key pair.

    $ aws configure set aws_access_key_id YOUR_ACCESS_KEY
    $ aws configure set aws_secret_access_key YOUR_SECRET_KEY

We can also set the region as the same region we created our repository (if N. Virginia then he region name is us-east-1), and set JSON as the default output format.

    $ aws configure set default.region <YOUR_REGION>
    $ aws configure set default.output json

We can now log in to ECR. There is a ctually a breaking change in how you log in to ECR in the CLI Version 2 compared to version 1. Both login commands are provided below, [here](https://docs.aws.amazon.com/cli/latest/userguide/cliv2-migration.html) you can see the full list of breaking changs between the versions.

    # CLI Version 1 login
    $ (aws ecr get-login --no-include-email --region <YOUR REGION>)

    # CLI Version 2 login
    $ aws ecr get-login-password | docker login --username AWS --password-stdin MY-REGISTRY-URL

The registry URL id for the registry you widh to access, in our case this is the registry we jusy created in AWS. The URL (or URI as ECR calls it) can be found in the repository overview, see image below.

![Find your registry URI](/assets/ReadMe/MyRegistryURI.png)

If the terminal responds with a *Login Succeeded* message you know you have successfully logged in to ECR and are ready to upload your Docker image.

To upload the image to aws we first se the `docker tag` command and then the `docker push` command. For a more complete description on what these commands do check out the [Docker documentation](https://docs.docker.com/engine/reference/commandline/push/).

    $ docker tag <EXISTING_IMAGE_NAME> <AWS_REPOSITORY_URI>
    $ docker push <AWS_REPOSITORY_URI>

An example of the commands and the reuslt is shown below.

![Push Docker image to the AWS repository](/assets/ReadMe/DockerPushImage.png)

You can verify tat the push was successful by clicking on your repository in AWS, you should see that a *latest* version of your image is now available in the repository. Copy the URI and store it somewhere temporarily, you will need it when creating the container to deploy the image.

![Latest version of the Docker image in the ECR repository](/assets/ReadMe/AWSRepoLatest.png)

## Step 5: Running our Docker container on AWS
Now that the Docker image is available on AWS we can run a container on AWS to make the application available to anyone in the world. We will do this using the AWS Console.

To start, navigate to *Clusters* on the left hand side of the ECS landing page. Click *Get started*. 

For the cotainer definition, click *Configure* on the custom image.

![Custom container definition](/assets/ReadMe/ECSGetStarted_CustomDef.png)

Give your container an apppropriate name. For the Image URI, paste the URI from the *latest* version of the image that you copied previously. The port mapping is 8050, this tells the container which port the application is running on within the application server. Leave everything else as default.

![Edit container](/assets/ReadMe/ECSEditContainer.png)

Click on *Next* at the bottom to move on to the Service definition. For the Load balancer type, select *Application Load balancer, leave everythin else as default and press *Next*

![Service Definition](/assets/ReadMe/ECSServiceDef.png)

On the *Cluster* page, give yout cluster an appropriate name, no other changes are required. 

You are now ready to create your cluster.

![Cluster review](/assets/ReadMe/ECSReview.png)

AWS will now create the resources required by your cluster. This includes a Virtual Private Cloud (VPC, a "network" in the cloud) and a load balancer. 

Once the launch is complete click *View service*. If the status of the service is *PENDING*, wait until it says *ACTIVE* (should only take a minute or two). 

To view the dasboard, press *Tasks*. You should see that you have one running task, click on it. This will take you to a page similar to the one shown below.

![Service task information](/assets/ReadMe/ECS_Service_TaskInfo.png)

You can now view your application by opening a new tab in your web browser and entering the public IP address of the task followed by :8050. For the public IP above this would read `3.81.86.88:8050`.

Congratulations, you have now successfully launched a Docker application on AWS! 


### Step 5b (Optional): Accessing your application through the Application Load Balancer
At this point, you may be wondering why we have to enter the port number after the public IP when we already provided the Application Load Balancer (ALB) with the port mapping 8050. This is because, when accessing the application from the IP address directly, we are not actually using the ALB.

To access the application though the Application Load Balancer, first we navigate to EC2 by searching for it in the AWS console. If you scroll down on the left menu you will find *Load Balancers* under the *Load Balancing* category, click on it. You should have one Load Balancer showing, assuming you do not have any Load Balancers running already.

![Elastic Load Balancer](/assets/ReadMe/ElasticLoadBalancer.png)

You can try to access the application by pasting the Load Balancer DNS Name into a browser and hitting enter, it will however not work. If you add *:8050* at the end of the DNS name and press enter again it should work. This is because, when the Load Balancer was created, AWS assumed you would access the application from the same port as it runs on the container. To fix this so that we do not have to add *:8050* at the end of the DNS name we need to do two things.

- Change the Load Balancer to listen on port 80 instead of 8050
- Allow inbound traffic from port 80 (HTTP) to our load balancer

Changing the listener can be done by clicking on listners, selecting the listener (there should only be one) and clicking *edit*. Change the pot protocol from 8050 to 80 and click update.

![Change listener port](/assets/ReadMe/ALB_ChangePort.png)

To update the security group, go back to the Loab Balancer Description and scroll down to Security. Click on the security group ID, which will take you to the VPC section of the AWS Console.

![Security group ALB info](/assets/ReadMe/ALB_SecurityGroup.png) 

Once on the VPC Secutity group page, select the one being used by your ALB (even though you have filtered on a secutiry group two secutiry groups may still show, the console is a little buggy). Click on the Inbound rules tab and *Edit inbound rules*

![Security group ALB info](/assets/ReadMe/SecurityGroup_EditInbound.png)

Now add an inbound rule for port 80 as shown below and clisk *Save rules*

![Security group ALB info](/assets/ReadMe/SecurityGroup_AddPort80.png)

You can now try to accessing the application with the ALB DNS name *without* the port number at the end, it should work.

The point of including this as a part of the demo was that, in a real life situation whee you have users who wish to access the dashboard, adding *:8050* at the end of a website name is not user-friendly. Knowing how to create a load balancer which correctly maps to the correct ports and allows the necessary access is therefore useful in real life situations.

## Step 6: Deleting everything
Running an ECS cluster on AWS is unfortunately not included in the AWS free tier usage, we should therefore delete the resources we have created to avoid paying for the resources in the future. To do this simpply navigate to your ECS Cluster and click *Delete cluster*. AWS will delete all the resources that were provisioned when the cluster was created.



# Computer Vision Annotation Tool (CVAT) for Animal Crossing

## What this README covers
- About Animal Crossing Project
- Deployment of CVAT on EC2 instance from scratch
- Making Modifications to CVAT for Animal Crossing

## About Animal Crossing Project by WSP Digital Data Science

Objective:
- To help the WSP Environment Team easily annotate and maintain their images.

Components for the Project:
- **CVAT hosted on EC2 instance**, source code can be found [here](https://github.com/benedictasherrie27/cvat).
- **AWS Lambda functions**, scripts can be found on the [animal-crossing Bitbucket](https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/).
- **AWS S3 buckets**, for storing the images.

Contacts:
- David Rawlinson (david.rawlinson@wsp.com), Supervisor and Lead Data Scientist
- Christine Seeliger (christine.seeliger@wsp.com), Senior Data Scientist
- Benedicta Sherrie (benedicta.sherrie@wsp.com), Data Science IBL Intern Jan-Jun 2022
- Zijin Chen (zijin.chen@wsp.com), Data Science IBL Intern Jan-Jun 2022

## Deployment of CVAT on EC2 instance from scratch

Requirements:
- You will need an AWS account. Contact Christine Seeliger (christine.seeliger@wsp.com) to help you get one.

### A. EC2 Instance Creation

1. Log into your AWS account and go into the EC2 console. Go to _Instances_ and click '_Launch instance from template_' on the top right corner of the screen.

2. Select **AC_CVAT** as a Source template. In the _Key pair (login)_ section, select your own key pair name, or click _Create new key pair_. Make sure to save this key pair so you can connect to your instance later on. Click '_Launch template_'.

3. Connect to your EC2 instance by entering the following command on your terminal:
```
    $ ssh -i /path/my-key-pair.pem my-instance-user-name@my-instance-public-ipv4-dns-name
```
For example, to connect to the current Animal Crossing EC2 instance, use the following:
```
    $ ssh -i /path/my-key-pair.pem ubuntu@ec2-54-252-18-255.ap-southeast-2.compute.amazonaws.com
```
To find out your instance's Public IPv4 DNS, you can look at your instance summary in the AWS EC2 console.

4. Once you're connected to the instance, create a virtual environment and activate it.
```
    $ pip install virtualenv
    $ virtualenv your-venv-name
    $ source path/to/your-venv-name/bin/activate
```

### B. CVAT Installation on EC2

1. To start, please have the terminal for the EC2 instance open.

2. Type the commands below into the terminal to install Docker.
```
    $ sudo apt-get update
    $ sudo apt-get --no-install-recommends install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    $ sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"
    $ sudo apt-get update
    $ sudo apt-get --no-install-recommends install -y docker-ce docker-ce-cli containerd.io
```

3. Enter the following to run docker without root permissions.
```
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
```
Log out and log back in so that your group membership is re-evaluated. You can type in `groups` command in the terminal and check if `docker` is in its output.

4. Next, use the following commands to install docker-compose. This is used for defining and running multi-container docker applications.
```
    $ sudo apt-get --no-install-recommends install -y python3-pip python3-setuptools
    $ sudo python3 -m pip install setuptools docker-compose
```

5. Clone the CVAT source code from this [GitHub repository](https://github.com/benedictasherrie27/cvat).
```
    $ sudo apt-get --no-install-recommends install -y git
    $ git clone https://github.com/benedictasherrie27/cvat.git
    $ cd cvat
```

6. To access CVAT using the IPv4 address that the EC2 instance has, export the `CVAT_HOST` environment variable.
```
    $ export CVAT_HOST=your-ipv4-address
```

7. To run the docker containers with the changes made to the CVAT source code, use the following command:
```
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
    $ docker-compose up -d
```
To run the docker containers according to the latest CVAT release from [openvinotoolkit](https://github.com/openvinotoolkit/cvat), run the following command instead:
```
    $ docker-compose build
    $ docker-compose up -d
```

8. To access your EC2-hosted CVAT by going to the following: http://your-ipv4-address:8080/.

## Making Modifications to CVAT for Animal Crossing

For any of the following changes to take effect, you should always bring Docker down first, and then rebuild it.
    $ docker-compose down
    $ docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
    $ docker-compose up -d

### To make changes to the CVAT User Interface

In the source code, there is a folder `cvat-ui` which contains all the different files for the user interface. To _hide specific buttons_ from the UI, find the specific section of the code that's for the button you want to hide, comment out that section of the code and save the file. Once you have done this, please rebuild the Docker stack in the instance.

### To edit the Export Format (Animal Crossing 1.0)

1. Go to `cvat/apps/dataset_manager/formats/metadata.py` to edit the code according to any changes needed to be made to the exported output file.
2. Save the changes in the file.
3. Bring Docker down with `docker-compose down` and rebuild the Docker with the `docker-compose ... build` and `docker-compose up -d` commands.

### To create a new Export Format

1. Make a new python script under `cvat/apps/dataset_manager/formats` directory. This can consist of functions or classes decorated with `importer` or `exporter` from `registry.py`.
2. Add an import statement to the end of `cvat/apps/dataset_manager/formats/registry.py`.
Read more on [how to add a new annotation format support](https://openvinotoolkit.github.io/cvat/docs/contributing/new-annotation-format/).
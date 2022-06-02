# Computer Vision Annotation Tool (CVAT) for Animal Crossing

## What this README covers
- About Animal Crossing Project
- Deployment of CVAT on EC2 instance from scratch
- Making Modifications to CVAT for Animal Crossing
- AWS S3 Bucket Setup
- AWS Lambda Setup

## About Animal Crossing Project by WSP Digital Data Science

Objective:
- To help the WSP Environment Team easily annotate and maintain their images.

Components for the Project:
- **CVAT hosted on EC2 instance**, source code can be found [here](https://github.com/benedictasherrie27/cvat).
- **AWS Lambda functions**, scripts can be found on the [animal-crossing Bitbucket](https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/).
- **AWS S3 buckets**, for storing the images.

To access the CVAT used for Animal Crossing, go to http://54.252.18.255:8080/.

Please contact any of the following for any queries:
- David Rawlinson (david.rawlinson@wsp.com), Supervisor and Lead Data Scientist
- Christine Seeliger (christine.seeliger@wsp.com), Senior Data Scientist
- Benedicta Sherrie (benedicta.sherrie@wsp.com), Data Science IBL Intern Jan-Jun 2022
- Zijin Chen (zijin.chen@wsp.com), Data Science IBL Intern Jan-Jun 2022

## Deployment of CVAT on EC2 instance from scratch

Requirements:
- You will need an AWS account. Contact Christine Seeliger (christine.seeliger@wsp.com) to help you get one.

### A. EC2 Instance Creation

1. Log into your AWS account and go into the [EC2 console](https://ap-southeast-2.console.aws.amazon.com/ec2/v2/home?region=ap-southeast-2#Home:). Go to _Instances_ and click '_Launch instance from template_' on the top right corner of the screen.

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

## AWS S3 Bucket Setup

1. Go to the [AWS S3 console](https://s3.console.aws.amazon.com/s3/buckets?region=ap-southeast-2). Click '_Create bucket_'.

2. In the '_Copy settings from existing bucket_' option, choose the **animal-crossing** bucket.

3. Click '_Create bucket_'.

## AWS Lambdas Setup

3 separate Lambda functions were created for the Animal Crossing annotation Pipeline. In the order of the workflow, these are the following:

1. **Onedrive-S3**, Lambda script can be found [here](https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/Onedrive-S3/).

2. **Day-night-sorting**, Lambda script can be found [here](https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/Day-night-sorting/Lambda/).

3. **CVAT-taskhandling**, Lambda scripts can be found [here](https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/CVAT-taskhandling/lambda/).

### Onedrive-S3 Lambda

Aim: to process the email received from Microsoft Onedrive once an image has been uploaded there, and put this image into AWS S3.

AWS Region where it was set up: `us-east-1`

#### How to setup

Source code: https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/Onedrive-S3/

1. Create a Lambda function from scratch, with a runtime of Python 3.9, and architecture of x86_64. Select '_Use an existing role_' for the Execution role section, and choose 'AC_SEStoS3'.

2. Copy the files found in the source code link into the lambda function code. Click 'Deploy' once the code has been added.

3. To set the trigger for this lambda, go to [Amazon Workmail](https://us-east-1.console.aws.amazon.com/workmail/v2/home?region=us-east-1#/). Click the `da-team` organization.

4. Click 'Organization settings' in the navigation pane, and click 'Inbound rules'.

5. Click 'Create' to create a new inbound rule.
    - Choose 'Run Lambda' under the 'Action' settings.
    - Make sure to specify the 'Sender domains or addresses' and 'Destination domains or addresses' sections.

### Day-night-sorting Lambda

Aim: To sort incoming images from `/inbox` directory into `/day` or `/night` directories every 20 minutes in AWS S3 `animal-crossing` bucket, with the addition of backing up those images to `animal-crossing-backup`.

AWS Region where it was set up: `ap-southeast-2`

#### How to setup

Source code: https://bitbucket.org/wspdigital/animal_crossing/src/master/Pipeline/Day-night-sorting/Lambda/

1. Create a Lambda function from scratch, with a runtime of Python 3.9, and architecture of x86_64. Select '_Use an existing role_' for the Execution role section, and choose '_lambda-role_'.

2. Next, we want to deploy package with dependencies for the Lambda script. Refer to this [link](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency) for more information.

    - In your local computer terminal, create a project directory named whatever you like. For example for macOS:
    ```
        $ mkdir directory-name
    ```
    - Navigate to the recently made directory.
    ```
        $ cd directory-name
    ```
    - Copy the contents found in the source code link and save it in a new file named `lambda_function.py`
    ```
        $ nano lambda_function.py
    ```
    Paste the code into this newly created file, and save it.
    - Install the required libraries to a new package directory.
    ```
        $ pip install --target ./package exif
        $ pip install --target ./package suntime
        $ pip install --target ./package datetime
    ```
    - Create a deployment package with the installed library at the root.
    ```
        $ cd package
        $ zip -r ../my-deployment-package.zip .
    ```
    - Add the `lambda_function.py` file to the root of the zip file.
    ```
        $ cd ..
        $ zip -g my-deployment-package.zip lambda_function.py
    ```

3. On the AWS Lambda console for the function you created earlier, click '_Upload from_' and select '_.zip file_'. Upload the file named my-deployment-package.zip, which you created in the previous step.

4. Edit the timeout settings to **15 minutes** under the **General Configuration** section.

5. Next, create a rule to run the Lambda function on a schedule.
    - Go to https://console.aws.amazon.com/cloudwatch/
    - In the navigation pane, choose '_Events_' --> '_Rule_' and click '_Back to CloudWatch Events_'.
    - Click '_Create rule_'
    - Select '_Schedule_' and set '_Fixed rate of_' to **20 minutes**.
    - For the '_Targets_' section, select '_Lambda function_' and choose the name of the function you just created so that it is triggered by this rule.
    - NOTE: an existing rule called 'schedule_classify_images' was already created to trigger the current lambda function.

6. You can see the rule once you created it. You can disable it by clicking '_Actions_' and select '_Disable_'.

### CVAT-taskhandling Lambda

Aim: To update the manifest files of each `/night` folders in the S3 bucket, and to (re-)create CVAT tasks with an expanded number of images. This is set to be done every day at 8 am AEST.

AWS Region where it was set up: `ap-southeast-2`

#### How to setup

1. Create a Lambda function from scratch, with a runtime of Python 3.8, and architecture of x86_64. Select 'Use an existing role' for the Execution role section, and choose 'AC_CVATTasks'.

2. Copy the files found in the source code link into the lambda function code. Note that there are 3 separate files, please keep each file's name the same as the ones found in the source code. Click 'Deploy' once all code is added.

3. Next, we want to add 2 layers to the Lambda function. This will provide the external Python libraries required for the lambda to run.
    - To add a layer, go to the 'Layers' section of the lambda, and click 'Add layer'. Choose 'Specify an ARN' and input the following ARNs:
        - Python Pillow module: `arn:aws:lambda:ap-southeast-2:770693421928:layer:Klayers-python38-Pillow:15`
        - Python requests module: `arn:aws:lambda:ap-southeast-2:770693421928:layer:Klayers-python38-requests:28`
        - Note: these may not be the latest ARN for the modules above. Please check [here](https://github.com/keithrozario/Klayers/blob/master/deployments/python3.8/arns/ap-southeast-2.csv) for the latest ones.

4. Edit the timeout settings to **15 minutes** under the **General Configuration** section.

5. Add an EventBridge trigger rule.
    - Click 'Add trigger'
    - Choose 'EventBridge (CloudWatch Events)' for the trigger.
    - You can either:
        - Create a new rule. Please refer to this [link](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html) if you want to write your own schedule expression.
        - Use an existing rule called `cvat_task_creation`, which is set to trigger the lambda everyday at 8 am AEST.

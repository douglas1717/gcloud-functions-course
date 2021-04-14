#Google cloud function course
##Startin a project
To start a new project in Google Cloud, we can go to the [Firebase Console](https://console.firebase.google.com) 
or create it from [Google Cloud Platform Console](https://console.cloud.google.com).
##Create a virtual enviroment
First we have to install `python3-venv` with the following command.
```
    sudo apt install python3-venv
```
Then we execute following command
```
    python3 -m venv venv
```
To activate venv
```
source venv/bin/ativate
```

Now, create the file requirements.txt to automate install all necessary  packages to the project.
```
    pip install -r requirements.txt
```

To run test in test enviroment 
```
functions-framework --target hello_world
http://127.0.0.1:8081/?name=douglas
```

To login gcloud
```
./google-cloud-sdk/bin/gcloud init
gcloud config set project paratyai
```
To install gcloud function
```
gcloud functions deploy hello_world --runtime python38 --trigger-http
```
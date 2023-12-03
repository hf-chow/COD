# COD
Download the gcloud CLI install script
```
https://cloud.google.com/sdk/docs/install
```

Install the gcloud CLI
```
./google-cloud-sdk/install.sh
```

Enabling the API by providing the authentication
```
export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"
```

Init glcoud with 
```
./google-cloud-sdk/bin/gcloud init
```

Test authentication with the following, it should print out the token
```
gcloud auth application-default print-access-token
```

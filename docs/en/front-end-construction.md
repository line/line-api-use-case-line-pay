# Building a front-end environment

## Fix index.js

In front > js > index.js, there is a value that needs to be changed for each environment, so modify that value.
Change the URL in the following description to the URL of the APIGateway that you took a note of when deploying the app.
1. request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/reserve/', true);

## Modify confirm.js

In front > js > confirm.js, there is a value that needs to be changed for each environment, so modify that value.
Change the URL in the following description to the URL of the APIGateway that you took a note of when deploying the app.
1. request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/confirm/', true);

## Deploy front-end modules in S3

 Place all the files in the front folder into the target S3 bucket created in the backend construction procedure.


[Next page](validation.md)

[Back to Table of Contents](README_en.md)

# Steps to build the backend

## Deploy peripheral resources

These peripheral resources need to be deployed for this app:

- Common processing layer (Layer)
### Common processing layer (Layer)

In AWS Lambda, you can describe the process you want to use in common with multiple Lambda functions as a layer.
Since this app uses layers, first deploy the layers by following these steps:

- Change template.yaml
  Open template.yaml in the backend > Layer folder and change this parameter item in the EnvironmentMap dev:

  - `LayerName` any layer name

- Run this command:

```
cd [backend > Layer folder]
sam build --use-container
sam deploy --guided
*Must be specified when using profile information that's not the default (`sam deploy --guided --profile xxx`)
    Stack Name: any stack name
    AWS Region: ap-northeast-1
    Parameter Environment: dev
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy Confirm changes before deploy [Y/n]: Y
    #SAM needs permission to be able to create roles to connect to the resources in your template Allow SAM CLI IAM role creation[Y/n]: Y
    Save arguments to samconfig.toml [Y/n]: Y

    SAM configuration file [samconfig.toml]: Press Enter only
    SAM configuration environment [default]: Press Enter only

    Deploy this changeset? [y/N]: y
```

- Note the layer version
  After deployment, the layer ARN and layer version will be displayed in the Output section of the terminal, so make sure to note the layer version.
  The layer version is the part with the numbers at the end
  *The version is updated every time you deploy, so the correct version for your first deployment is version 1.
  ![Output section of the command prompt](../images/en/out-put-description-en.png)

- [Confirmation] Open the Lambda console in the AWS Management Console, select "Layers" from the left tab, and confirm that the layer you deployed this time exists.

## Deploy the application (APP)

Follow these steps to deploy the app:

- Change template.yaml
  Open template.yaml in the backend > APP folder, and modify these parameter items of dev in EnvironmentMap:
  *If you need the S3 access log, uncomment the part that says ACCESS LOG SETTING.


  - `LinePayChannelId` The channel ID of the LINE Pay channel created in [Creating a LINE channel]
  - `LinePayChannelSecret` Channel secret for the LINE Pay channel created in [Creating a LINE channel]
  - `LinePayIsSandbox` True or False
    *Specify the basic True
    True: Uses a sandbox environment. You will not be charged by LINE Pay.
    False: LINE Pay "test merchant environment" will be used. The user's LINE Pay balance will be temporarily debited and the amount spent will be refunded after a certain period of time.
  - `LINEPayOrderInfoDBName` Any table name (table to register payment information)
  - `FrontS3BucketName` Any bucket name *This will be the S3 bucket name to place the front-side module.
  - `LayerVersion` The version number of the layer deployed in the [1. Common processing layer] procedure
    Example: LayerVersion: 1
  - `LoggerLevel` INFO or Debug
  - `LambdaMemorySize` Lambda memory size
    Example) LambdaMemorySize: 128 *If you don't need to change it, specify the minimum size of 128
  - `TTL` True or False (whether to delete order information automatically)
  - `TTLDay` Any number (If TTL is True, specify how many days after registration the reservation information will be deleted; if TTL is False, enter 0)
  - `LogS3Bucket` Any bucket name (the name of the S3 where the access log is stored)
  *Cancel the comment and record it only if you need an access log. Also, if you've already built another Use Case app, specify its access log bucket name and alias.
  - `LogFilePrefix` Any name (log file prefix)
  *Cancel the comment and record it only if you need an access log.

- Run this command:

```
cd [backend > APP folder]
sam build --use-container
sam deploy --guided
*Must be specified when using profile information that's not the default (`sam deploy --guided --profile xxx`)
    Stack Name: any stack name
    AWS Region: ap-northeast-1
    Parameter Environment: dev
    #Shows you resources changes to be deployed and require a 'Y' to initiate deploy Confirm changes before deploy [Y/n]: Y
    #SAM needs permission to be able to create roles to connect to the resources in your template Allow SAM CLI IAM role creation[Y/n]: Y
    ××××× may not have authorization defined, Is this okay? [y/N]: y (Input "y" for all)

    SAM configuration file [samconfig.toml]: Press Enter only
    SAM configuration environment [default]: Press Enter only

    Save arguments to samconfig.toml [Y/n]: Y
    Deploy this changeset? [y/N]: y
```

- Notes on API Gateway URL and CloufFrontDomainName
Take a note of the API Gateway endpoint and CloudFrontDomainName displayed in OutPut when the deployment is successful. You'll use them in the later steps.

## Error handling

- If you encounter the following error when deploying, follow this procedure to resolve it.
  ```
  Export with name xxxxx is already exported by stack sam-app. Rollback requested by user.
  ```
  - Deploy after modifying backend > Layer > template.yaml with reference to the following:
    ```
    Outputs:
      UseCaseLayerName:
        Description: "UseCaseLayerDev Layer Name"
        Value: !FindInMap [EnvironmentMap, !Ref Environment, LayerName]
        Export:
          Name: LinePayLayerDev > Modify this to any name you want
    ```
  - Modify backend > batch > template.yaml with reference to the following description.
    ```
    !ImportValue LinePayLayerDev > Modify LinePayLayerDev to the name you just entered
    ```
  - Modify backend > APP > template.yaml with reference to the following description.
    ```
    !ImportValue LinePayLayerDev > Modify LinePayLayerDev to the name you just entered
    ```

[Next page](front-end-construction.md)

[Back to Table of Contents](README_en.md)

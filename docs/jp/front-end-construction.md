# フロントエンド環境構築

## index.jsの修正
front -> js -> index.jsにて、環境ごとに変更が必要な値があるため、そちらを修正してください。  
以下の記載箇所のURLを、アプリのデプロイ時にメモを取ったAPIGatewayのURLに変更してください。  
1. request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/reserve/', true);

## confirm.jsの修正
front -> js -> confirm.jsにて、環境ごとに変更が必要な値があるため、そちらを修正してください。  
以下の記載箇所のURLを、アプリのデプロイ時にメモを取ったAPIGatewayのURLに変更してください。  
1. request.open('POST', 'https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/dev/confirm/', true);
## S3にフロントエンドのモジュールを配置
 frontフォルダ内の全てのファイルを、バックエンド構築手順にて作成した対象のS3バケットに配置してください。


[次の頁へ](validation.md)

[目次へ戻る](../../README.md)

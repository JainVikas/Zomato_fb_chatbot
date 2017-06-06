from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os, json, boto3
import pandas as pd

data= pd.DataFrame();
filename="";
app = Flask(__name__)
language = [{'name':'JS'},{'name':'python'}]
@app.route('/webhook', methods=['POST'])
def webhook():
    filepath = request.json["filename"]
    if filepath != filename:
      filename= filepath
      data = pd.read_csv(filename) 
    #fileread(filename)
    l1 = list(data)	
    return jsonify({'list':data})


@app.route('/sign_s3/')
def sign_s3():
  S3_BUCKET = os.environ.get('S3_BUCKET')

  file_name = request.args.get('file_name')
  file_type = request.args.get('file_type')

  s3 = boto3.client('s3')

  presigned_post = s3.generate_presigned_post(
    Bucket = S3_BUCKET,
    Key = file_name,
    Fields = {"acl": "public-read", "Content-Type": file_type},
    Conditions = [
      {"acl": "public-read"},
      {"Content-Type": file_type}
    ],
    ExpiresIn = 3600
  )

  return json.dumps({
    'data': presigned_post,
    'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
  })
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)
import sys
import boto
import boto.s3

# AWS ACCESS DETAILS
AWS_ACCESS_KEY_ID = 'AKIAIBKBOVF6DTJ3LPQQ'
AWS_SECRET_ACCESS_KEY = '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'

bucket_name = AWS_ACCESS_KEY_ID.lower() + '-mah-bucket' 
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)
uploadfile = sys.argv[1]

print ('Uploading %s to Amazon S3 bucket %s') 

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

from boto.s3.key import Key
k = Key(bucket)
k.key = 'my test file'
k.set_contents_from_filename(uploadfile, cb=percent_cb, num_cb=10)
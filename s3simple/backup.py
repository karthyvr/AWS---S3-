import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        AWS_ACCESS_KEY_ID = 'AKIAICUEFWET7MYXIQUA'
        AWS_SECRET_ACCESS_KEY = '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'
        conn=S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,validate_certs=False,is_secure=False)
        my_bucket_name = 'karthy'
        print"before getting bucket karthy"
        my_bucket = conn.get_bucket(my_bucket_name)
        print"after  getting bucket , print bucket name"
        print my_bucket.name
        input_file = request.files['input_file']
        print input_file.filename
        print"before puttinh inyo bucket karthy"
        k = Key(my_bucket)
        k.key=input_file.filename
        k.set_contents_from_string(input_file.read())

        print"after puttinh inyo bucket karthy"

    return render_template('index.html')


if __name__ == '__main__':
     app.run()
    # forlocal run uncomment below
    #  app.run(
    #     host='0.0.0.0',
    #     port=int('8080'),
    #     debug=True
    # )

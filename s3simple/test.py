import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import urllib
from flask import Flask, request, redirect, url_for, render_template, send_file, Response, make_response

app = Flask(__name__)

file_dir =  '/tmp/download/'
# home page for this application
@app.route('/')
def welcome():
    print"inside welcome"
    return render_template('user.html')
    # with open('password.txt') as f:
    #     content = f.readlines()
    # print content
@app.route('/checkuser', methods=['POST'])
def checkuser():
    print "checkuserrrr"
    ip_username =  request.form['username']
    # Local
    # with open('password.txt') as f:
    with open('/var/www/html/flaskapp/password.txt') as f:
        content = f.readlines()
    print content
    for name in content:
        name = name[:-1]
        print name
        if name == ip_username:
            print "user exists"
            result_message = 'welcome ...!'+ ip_username + '....!'
            return render_template('index.html',result_msg=result_message)
    result_message = ip_username +' is not a valid user...please retry!'
    return render_template('user.html',result_msg=result_message)


@app.route('/index')
def index():
    return render_template('index.html')

# # else do not save the file
@app.route('/goupload')
def goupload():
    print 'in goupload'
    return render_template('upload.html')
def getconnection():
    AWS_ACCESS_KEY_ID = 'AKIAICUEFWET7MYXIQUA'
    AWS_SECRET_ACCESS_KEY = '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'
    conn=S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,validate_certs=False,is_secure=False)
    return conn
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        conn = getconnection()
        my_bucket_name = 'karthy'
        print"before getting bucket karthy"
        my_bucket = conn.get_bucket(my_bucket_name)
        print"after  getting bucket , print bucket name"
        print my_bucket.name
        input_file = request.files['input_file']
        files_list = listalldocuments()
        for i in files_list:
            if i.name == input_file.filename:
                print "file already exists"
                upload_message = input_file.filename +' already exists ..!'
                # print upload_message
                return render_template('upload.html', result_msg=upload_message)
        print input_file.filename
        print"before puttinh inyo bucket karthy"
        k = Key(my_bucket)
        k.key=input_file.filename
        k.set_contents_from_string(input_file.read())

        print"after puttinh inyo bucket karthy"

        upload_message = input_file.filename +' uploaded successfully..!'
    # print upload_message
    return render_template('upload.html', result_msg=upload_message)

@app.route('/list')
def list():
    print "inside the list file function "
    files_list = listalldocuments()

    return render_template('list.html', files_list=files_list)

@app.route('/deleteordownload')
def deleteordownload():
    print "deleteOrDownload"
    ip_filename = request.args.get('filename')
    ip_operation = request.args.get('operation')

    if ip_operation == 'Download':
        return redirect(url_for('download', filename=ip_filename))
    elif ip_operation == 'Delete':
        return redirect(url_for('delete', filename=ip_filename))
    elif ip_operation == 'View':
        return redirect(url_for('view', filename=ip_filename))

@app.route('/delete/<filename>')
def delete(filename):
    print "In Delete"
    print 'file name ', filename
    conn = getconnection()
    my_bucket_name = 'karthy'
    my_bucket = conn.get_bucket(my_bucket_name)
    my_bucket.delete_key(filename)
    files_list = listalldocuments()
    return render_template('list.html', result_msg="File deleted successfully..!", files_list=files_list)

@app.route('/download/<filename>')
def download(filename):
    print "In Download"
    conn = getconnection()
    my_bucket_name = 'karthy'
    my_bucket = conn.get_bucket(my_bucket_name)
    k = Key(my_bucket)
    k.key = filename
    file_download = open(file_dir + filename, 'wb')
    print" after file output"
    k.get_contents_to_file(file_download)
     # print file_output.read()
    file_download.close()
    file_download = open(file_dir + filename, 'rb')
    print"before return",
    return send_file(file_download.name, as_attachment=True)


@app.route('/view/<filename>')
def view(filename):
    print"testttttttttt"
    conn = getconnection()
    my_bucket_name = 'karthy'
    my_bucket = conn.get_bucket(my_bucket_name)
    k = Key(my_bucket)
    k.key = filename

    file_download = open(file_dir + filename, 'wb')
    print" after file output"
    k.get_contents_to_file(file_download)
     # print file_output.read()
    file_download.close()
    file_download = open(file_dir + filename, 'rb')
    print"before return",
    return send_file(file_download.name, as_attachment=False)

def listalldocuments():
    conn = getconnection()
    my_bucket_name = 'karthy'
    bucket  = conn.get_bucket(my_bucket_name)
    rs = bucket.list()
    return rs
if __name__ == '__main__':
     # app.run()
    # forlocal run uncomment below
     app.run(
        host='0.0.0.0',
        port=int('8080'),
        debug=True
    )

from flask import Flask, request, jsonify
import logging
import os
from google.cloud import storage


from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)


project_id = os.environ.get('PROJECT_ID')
storage_bucket_name = os.environ.get('STORAGE_NAME')

logging.info("Storage account checker for internal tests")
logging.info("**** Environment variables:")
logging.info("** PROJECT_ID: {}".format(project_id))
logging.info("** STORAGE_NAME: {}".format(storage_bucket_name))
logging.info ("Contact: klodnicki.k@pg.com")

if (project_id==None):  logging.error("Missing env variable 'PROJECT_ID'")
if (storage_bucket_name==None):  logging.error("Missing env variable 'STORAGE_NAME'")

app = Flask(__name__)


def list_blobs(bucket_name):
	"""Lists all the blobs in the bucket."""

	storage_client = storage.Client()
	blob_list = []

	blobs = storage_client.list_blobs(bucket_name)

	for blob in blobs:
		blob_list.append(blob.name)

	logging.info("Number of objects in storage account {}: {}".format(storage_bucket_name, len(blob_list)))
        

	return blob_list




@app.route('/', methods=['GET'])
def request_main_page():
	blobs = list_blobs(storage_bucket_name)


	message = {
	'project_id' :  project_id,
	'storage_bucket_name' : storage_bucket_name,
	'list_of_objects' : blobs
	}

	return jsonify(message)



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
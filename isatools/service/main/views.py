__author__ = 'alfie'

import os, zipfile, string, requests, uuid, glob
import subprocess
from flask import render_template, request, current_app, redirect, url_for, send_from_directory, json, make_response
from os.path import basename
from werkzeug import secure_filename
from bs4 import BeautifulSoup
from . import main
from isatabToJsonWriterV2 import IsatabToJsonWriterV2
from isaJsonToTabWriter import IsajsonToIsatabWriter
from .common_functions import CommonFunctions


commonFunctions = CommonFunctions()


@main.route('/isatab-to-isajson', methods=['GET'])
def isatabToIsajsonInterface():
    return render_template('isatab-to-isajson.html')


@main.route('/isajson-to-isatab', methods=['GET'])
def isajsonToIsatabInterface():
    return render_template('isajson-to-isatab.html')


@main.route('/sra-to-isatab', methods=['GET'])
def sraToIsatabInterface():
    return render_template('sra-to-isatab.html')


@main.route('/create-isa', methods=['GET'])
def createIsaInterface():
    return render_template('create-isa.html')


@main.route('/hello/')
@main.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# For a given file, return whether it is an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
def index():
    return render_template('index.html')


def zipdir(path, ziph):
    # ziph is the zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            # basename is passed as the second argument in order to eliminate the absolute path in the zip archive
            ziph.write(os.path.join(root, file), os.path.join(os.path.basename(root), file))


# Route that will process the isa-tab to isa-json conversion (by file)
@main.route('/uploadIsatabByFile', methods=['POST'])
def uploadIsatabByFile():
    # Get the name of the uploaded file
    file = request.files["inputIsatabFile"]
    # Get if the json output is to be chunked or not
    pst = request.form["inputIsajsonFileOption"]
    chunked = commonFunctions.strToBool(pst)
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # create the uploads folder if it does not exists
        if not os.path.exists(current_app.config['OUTPUT_FOLDER']):
            os.makedirs(current_app.config['OUTPUT_FOLDER'])
        # create the folder to contain the uploaded isa-tab file
        fuuid = uuid.uuid4()
        fuuid_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], str(fuuid))
        os.makedirs(fuuid_dir)
        # Move the file from the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename))
        # get the folder of the isa-tab files
        isatab_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename.split('.')[0])
        # extract the uploaded file
        with zipfile.ZipFile(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename)) as zfile:
            zfile.extractall(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir))
        # set the name of the folder of the isa-json files
        isajson_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename.split('.')[0] + "-json")
        # create the json folder if it does not exists
        if not os.path.exists(isajson_dir):
            os.makedirs(isajson_dir)
        # call the method to create the json files
        writer = IsatabToJsonWriterV2()
        writer.parsingIsatab(isatab_dir, isajson_dir, chunked)
        # TODO: Check that the isa-json generated passed the isa-json schema
        # Zip the isa-json directory
        zipName = isajson_dir + ".zip"
        zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        zipdir(isajson_dir, zipf)
        zipf.close()
        # Return back the .zip file
        return redirect(url_for('.uploaded_Isadoc', directory=str(fuuid), filename=filename.split('.')[0] + "-json.zip"))
    else:
        # TODO: To return back a meaningful error message
        return render_template('500.html')


def processSRAData(fuuid, fuuid_dir, accessionNumber, chunked):
    # Note: problem in using lxml that is why we are using subprocess and running the xslt stylesheet using the command line
    f_xsl = os.path.join(current_app.config['XSLT_FOLDER'], 'sra/sra-embl-online2isatab-txt.xsl')
    f_xml = os.path.join(current_app.config['XSLT_FOLDER'], 'sra/blank.xml')

    subprocess.call(['java', '-jar', os.path.join(current_app.config['LIB_FOLDER'], 'saxon9ee.jar'), f_xml, f_xsl, 'acc-number=' + accessionNumber, 'output-dir=' + str(fuuid)])
    # check the isa-tab for the sra has been created
    sra_isatab_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], str(fuuid), accessionNumber)
    if not os.path.exists(sra_isatab_dir):
        return False
    else:
         # set the name of the folder of the isa-json files
        isajson_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, accessionNumber + "-json")
        # create the json folder if it does not exists
        if not os.path.exists(isajson_dir):
            os.makedirs(isajson_dir)
        # call the method to create the json files
        writer = IsatabToJsonWriterV2()
        writer.parsingIsatab(sra_isatab_dir, isajson_dir, chunked)
        # TODO: Check that the isa-json generated passed the isa-json schema
        # Zip the isa-json directory
        zipName = isajson_dir + ".zip"
        zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        zipdir(isajson_dir, zipf)
        zipf.close()
        return True


def processMetabolightsData(fuuid_dir, accessionNumber, chunked):
    # create the isatab accession number folder if it does not exists
    isatab_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, accessionNumber + "-tab")
    if not os.path.exists(isatab_dir):
        os.makedirs(isatab_dir)
    try:
        url = 'http://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/' + accessionNumber
        fResponse = requests.get(url)
        soup = BeautifulSoup(fResponse.text)
        # the list of isa-tab files to be downloaded and download them
        investigationFilePattern = "i_"
        studyFilePattern = "s_"
        assayFilePattern = "a_"
        # get the isa-tab files
        for link in soup.findAll('a'):
            if link.get('href').startswith(investigationFilePattern) or link.get('href').startswith(studyFilePattern) or link.get('href').startswith(assayFilePattern):
                res = requests.get(url + '/' + link.get('href'), stream=True)
                with open(os.path.join(isatab_dir, link.get('href')), 'wb') as f_handle:
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                            f_handle.write(chunk)
                            f_handle.flush()
                f_handle.close()
        # set the name of the folder of the isa-json files
        isajson_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, accessionNumber + "-json")
        # create the json folder if it does not exists
        if not os.path.exists(isajson_dir):
            os.makedirs(isajson_dir)
        # convert the isa-tab to isa-json
        writer = IsatabToJsonWriterV2()
        writer.parsingIsatab(isatab_dir, isajson_dir, chunked)
        # TODO: Check that the isa-json generated passed the isa-json schema
        # Zip the isa-json directory
        zipName = isajson_dir + ".zip"
        zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        zipdir(isajson_dir, zipf)
        zipf.close()
        return True
    except requests.exceptions.ConnectionError as e:
        print "Couldn't find the url"
        return False


# Route that will process the isa-tab upload (by accession number)
@main.route('/uploadIsatabByAccessionNumber', methods=['POST'])
def uploadIsatabByAccessionNumber():
    # Get the repository to be used
    repository = request.form["inputIsatabRepositoryOption"]
    # Get the accession number of the isa-tab
    accessionNumber = request.form["inputIsatabAccessionNumber"]
    # Get if the json output is to be chunked or not
    pst = request.form["inputIsajsonAccessionOption"]
    chunked = commonFunctions.strToBool(pst)
    # create the uploads folder if it does not exists
    if not os.path.exists(current_app.config['OUTPUT_FOLDER']):
        os.makedirs(current_app.config['OUTPUT_FOLDER'])
    # create the folder to contain the uploaded isa-tab file
    fuuid = uuid.uuid4()
    fuuid_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], str(fuuid))
    os.makedirs(fuuid_dir)
    # Choose which repository to process
    if (repository.lower() == 'metabolights'):
        processDataFromRepo = processMetabolightsData(fuuid_dir, accessionNumber, chunked)
    else:
        processDataFromRepo = processSRAData(fuuid, fuuid_dir, accessionNumber, chunked)

    if processDataFromRepo:
        # Return back the .zip file
        return redirect(url_for('.uploaded_Isadoc', directory=str(fuuid), filename=accessionNumber + "-json.zip"))
    else:
        return render_template('500.html')


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the output
# directory and show it on the browser
@main.route('/uploadsIsadoc/<directory>/<filename>', methods=['GET'])
def uploaded_Isadoc(directory, filename):
    return send_from_directory(os.path.join(current_app.config['OUTPUT_FOLDER'], directory), filename)


# Route that will process the isa-json upload
@main.route('/uploadIsajson', methods=['POST'])
def uploadIsajson():
    # Get the name of the uploaded isa-json file
    file = request.files["inputIsajsonFile"]
    # Get if the json output is to be chunked or not
    pst = request.form["inputIsajsonFileFormat"]
    chunked = commonFunctions.strToBool(pst)
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # create the uploads folder if it does not exists
        if not os.path.exists(current_app.config['OUTPUT_FOLDER']):
            os.makedirs(current_app.config['OUTPUT_FOLDER'])
        # create the folder to contain the uploaded isa-tab file
        fuuid = uuid.uuid4()
        fuuid_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], str(fuuid))
        os.makedirs(fuuid_dir)
        # Move the file from the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename))
        # get the folder of the isa-json files
        isajson_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename.split('.')[0])
        # extract the uploaded file
        with zipfile.ZipFile(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename)) as zfile:
            #zfile.extractall(isajson_dir)
            zfile.extractall(os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir))
            isajson_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, zfile.namelist()[0].split('/')[0])
        # set the name of the folder of the isa-json files
        isatab_dir = os.path.join(current_app.config['OUTPUT_FOLDER'], fuuid_dir, filename.split('.')[0] + "-tab")
        # create the tab folder if it does not exists
        if not os.path.exists(isatab_dir):
            os.makedirs(isatab_dir)
        # call the method to create the json files
        writer = IsajsonToIsatabWriter()
        if (chunked):
            writer.parsingJson(isajson_dir, isatab_dir)
            # TODO: Check that the isa-tab generated is correct
        else:
            # if it is not chunked then we assume that there is only one file
            # so we just need to get the file path and pass it to the parser
            notChunkedList = glob.glob(os.path.join(isajson_dir, "*.json"))
            if len(notChunkedList) > 1:
                # TODO: To return back a meaningful error message
                return render_template('500.html')
            else:
                writer.parsingJsonCombinedFile(notChunkedList[0], isatab_dir)
                # TODO: Check that the isa-tab generated is correct
        # Zip the isa-json directory
        zipName = isatab_dir + ".zip"
        zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
        zipdir(isatab_dir, zipf)
        zipf.close()
        # Return back the .zip file
        return redirect(url_for('.uploaded_Isadoc', directory=str(fuuid), filename=filename.split('.')[0] + "-tab.zip"))
    else:
        # TODO: To return back a meaningful error message
        return render_template('500.html')

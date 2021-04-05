from flask import Flask, Response
import os
import requests
import shutil
from npm_package_handeler import NpmPackageHandler
from enums import *
import json
from semgrep_runner import SemgrepRunner

app = Flask(__name__)


@app.route('/api/v1/npm/<pacakge_name>/', defaults={'version': "latest"})
@app.route('/api/v1/npm/<pacakge_name>/<version>')
def npm_handeler(pacakge_name, version):
    result_path = NpmPackageHandler.check_if_results_exists(pacakge_name, version)
    if result_path["status"] == STATUS.ERROR.value:
        npm_package_result = NpmPackageHandler.download_npm_package(pacakge_name, version)
        if npm_package_result["status"] == STATUS.SUCCESS.value:
            SemgrepRunner.run_semgrep(npm_package_result['path'])
        else:
            return Response(json.dumps(npm_package_result), mimetype=MIMETYPE.JSON.value)

    return Response(open(result_path["path"],"r").read(), mimetype=MIMETYPE.JSON.value)



if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")

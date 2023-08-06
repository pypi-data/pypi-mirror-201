# * Implement REST API to access, manipulate IoT publish information in database
# * and implement additional operations

## Errors
# 0 → No error
# 1 → Arguments to create a new gate are not in the correct format
from flask import Flask, request, abort
from .gCentralComponentDB import listData, newPayload, listDataByID, listDataByDataType, row2dict, table2dict



GATEDATASERVICE = "http://localhost:8000"

app = Flask(__name__)

def raise_error(errorNumber, errorDescription):
    return {"error": errorNumber, "errorDescription":errorDescription}

# GET   /API/gates -> Register new gate
# POST  /API/gates -> List registered gates
@app.route("/API/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST': #With the Post come one json like {"topic":"9999", "type":"something"}
        #parse body
        body = request.json
        try:
            topic = body['topic']
            iotDeviceID = body['iotDeviceID']
            dataType = body['dataType']
            data = body['data']
        except:
            abort(400)

        # Register Gate
        if (error := newPayload( topic,iotDeviceID, dataType,data )) > 0:
            
            return { 
                "error": 0
            }
        elif error == -1:
            return raise_error(1,"Arguments to create a new gate are not in the correct format.")
        else:
            return raise_error(100, "Something went wrong")
    
    elif request.method == 'GET':

        list = table2dict(listData())
        
        return {
            "data": list,
            "error": 0
        }
    
    else:
        return raise_error(404, "Method not allowed")

@app.route("/API/data/ID/<path:dataID>", methods=['GET'])
def getDataByID(dataID):
    
    try:
        result = listDataByID(int(dataID))
    except:
        abort(404)
    
    if isinstance(result, int):
        abort(404)

    else:
        return row2dict(result)    
    
@app.route("/API/data/dataType/<path:dataType>", methods=['GET'])
def getDataByTopic(dataType):

    try:
        result = listDataByDataType(dataType)
    except:
        abort(404)

    if isinstance(result, int):
        abort(404)

    else:
        return table2dict(result)    

def launchDataBase(host = '0.0.0.0', port = 8000):
    
    app.run(host = host, port = port, debug = True)




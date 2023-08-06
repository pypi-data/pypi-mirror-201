import requests, json, time, pprint

# This is the master webex.py that we will publish

def ppJson(jsonThing, sort=True, indents=4):
    if type(jsonThing) is str:
        print(json.dumps(json.loads(jsonThing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(jsonThing, sort_keys=sort, indent=indents))
    return None

def timestamp():
    timestr = time.strftime("%Y%m%d-%H%M%S") + " "
    return timestr

def getTokenFromCode(clientId,clientSecret,code,redirectUri):
    APIURI = "https://webexapis.com/v1/access_token"

    httpBodyText = {'grant_type': 'authorization_code',
            'client_id' : clientId,
            'client_secret' : clientSecret,
            'code' : code,
            'redirect_uri' : redirectUri}
            
    httpBodyJSON = json.dumps(httpBodyText) 
    APIHEADERS = { 'Content-Type' : 'application/json'}
    APIRESPONSE = requests.post(APIURI, headers=APIHEADERS, data = httpBodyJSON) 
    results = APIRESPONSE.json()
    
    if "error" in json.dumps(results):
        errorDescription = json.dumps(results['error_description'])
        return errorDescription
    else:
        return results

#Usage for getTokenFromCode()

#results = webex.getTokenFromCode(client_id, client_secret, code, redirect_uri)

#if "access_token" in results:
#    print("Access Token: " + results['access_token'] + "\n")
#    print("Refresh Token: " + results['refresh_token'] + "\n")
#else:
#    print("Error: " + results + "\n")


#Get a bearer token from the refresh token (the bearer tokens expire frequently, while the refresh tokens do not)
def refreshToken(clientId,clientSecret,refreshToken):
    APIURI = "https://webexapis.com/v1/access_token"
    
    httpBodyText = {'grant_type': 'refresh_token',
            'client_id' : clientId,
            'client_secret' : clientSecret,
            'refresh_token' : refreshToken}

    httpBodyJSON = json.dumps(httpBodyText) 
    APIHEADERS = {'Content-Type' : 'application/json'}
    APIRESPONSE = requests.post(APIURI, headers=APIHEADERS, data = httpBodyJSON) 
    results = APIRESPONSE.json()
    if "error" in json.dumps(results):
        errorDescription = json.dumps(results['error_description'])
        return errorDescription
    else:
        return results

#Usage for refreshToken()
# results = webex.refreshToken(client_id,client_secret,refresh_token)

# if "access_token" in results:
#     print("Access Token: " + results['access_token'] + "\n")
#     print("Refresh Token: " + results['refresh_token'] + "\n")
#     #print("Scope: " + results['scope'] + "\n")
    
# else:
#     print("Error: " + results + "\n")

#This function will get the Webex UserID value from a provided email address
def getUserIdFromEmail(accessToken, emailAddress): 
    APIURIPARAMETERS = {'emailAddress' : 'email=' + emailAddress }
    APIURI = "https://webexapis.com/v1/people/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "?" + APIURIPARAMETERS['emailAddress']
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    results = APIRESPONSE.json()
    return results

#Usage for getUserId()
# results = webex.getUserIdFromEmail(accessToken,emailAddress)

# id = results["items"][0]["id"]
# if "items" in results:
#      print("ID: " + id + "\n")    
# else:
#      print("Error: " + results + "\n")


#List admin audit events in your organization
def adminAuditEvents(accessToken, orgId, fromDateTime, toDateTime, actorId): 
    APIURIPARAMETERS = {
        'orgId' : 'orgId=' + orgId,
        'fromDateTime' : 'from=' + fromDateTime,
        'toDateTime' : 'to=' + toDateTime,
        'actorId' : 'actorId=' + actorId   
     }

    APIURI = "https://webexapis.com/v1/adminAudit/events"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "?" + APIURIPARAMETERS['orgId'] + "&" + APIURIPARAMETERS['fromDateTime'] + "&" + APIURIPARAMETERS['toDateTime'] + "&" + APIURIPARAMETERS['actorId']
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    results = APIRESPONSE.text
    return results

#Usage for adminAuditEvents()
# orgId = "your org id"
# fromDateTime= "2022-01-01T13:12:11.789Z"
# toDateTime = "2022-12-01T13:12:11.789Z"
# actorId = "id of the user to audit"
# results = webex.adminAuditEvents(accessToken, orgId, fromDateTime, toDateTime, actorId)
# webex.ppJson(results)

        
#Shows details for a person, by ID.
def getUserDetails(accessToken, userId): 
    
    APIURI = "https://webexapis.com/v1/people"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "/" + userId
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    results = APIRESPONSE.json()
    return results

#Usage for getUserDetails()
# results = webex.getUserDetails(accessToken, id)
# webex.ppJson(results)

#This function will get the licenses associated with an organization from a provided org id
def getLicenses(accessToken, orgId):
    APIURIPARAMETERS = {
        'orgId' : 'orgId=' + orgId  
     }
    APIURI = "https://webexapis.com/v1/licenses"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "?" + APIURIPARAMETERS['orgId']
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    results = APIRESPONSE.text
    return results

#Usage for getLicenses()
# results = webex.getLicenses(accessToken, orgId)
# webex.ppJson(results)
 

def getLocationIds(accessToken, orgId):
    APIURI = "https://webexapis.com/v1/locations"
    APIURIPARAMETERS = {
        'orgId' : 'orgId=' + orgId,
     }
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "?" + APIURIPARAMETERS['orgId']
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True)  
    results = APIRESPONSE.text
    return results

#Usage for getLocationIds()
# results = webex.getLocationIds(accessToken, orgId)
# webex.ppJson(results)

def toggleVoicemailEnable(accessToken, orgId, userId, state):
    APIURI = "https://webexapis.com/v1/people/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "/" + userId + "/features/voicemail" + "?orgId=" + orgId
    
    if state == "TRUE" or state == "true" or state == "True" or state == "t" or state == "T":
        data = { 
                "enabled": True         
            }
    elif state == "FALSE" or state == "false" or state == "False" or state == "f" or state == "F":
        data = {
                "enabled": False         
            }

    httpBodyJSON = json.dumps(data)

    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, verify=True, data=httpBodyJSON)  
    results = APIRESPONSE.text
    return results


def setVoicemailZeroOut(accessToken, orgId, userId, state, destination):
    APIURI = "https://webexapis.com/v1/people"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "/" + userId + "/features/voicemail" + "?orgId=" + orgId

    if state == "enable" or state == "ENABLE" or state == "TRUE" or state == "true" or state == "True" or state == "t" or state == "T":
        data = { 
                "transferToNumber": {
                    "enabled": True,
                    "destination": destination
                }
            }        
    
    if state == "disable" or state == "DISABLE" or state == "FALSE" or state == "false" or state == "False" or state == "f" or state == "F": 
        data = { 
                "transferToNumber": {
                    "enabled": False
                }
            }        
    
    httpBodyJSON = json.dumps(data)

    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, data=httpBodyJSON)     
    results = APIRESPONSE.text
    return results

#Usage for setVoicemailZeroOut()
# results = webex.setVoicemailZeroOut(accessToken, enableOrDisable, userId, destination)

def setVoicemailEmailNotify(accessToken, orgId, userId, state, destination):
    APIURI = "https://webexapis.com/v1/people"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "/" + userId + "/features/voicemail" + "?orgId=" + orgId

    if state == "enable" or state == "ENABLE" or state == "TRUE" or state == "true" or state == "True" or state == "t" or state == "T":
        print("Enabling Email Notification")
        data = {"messageStorage" : {
                    "storageType": "INTERNAL" 
                    },  
                "emailCopyOfMessage": {
                "enabled": True,
                "emailId": destination
                }
            }        

    if state == "disable" or state == "DISABLE" or state == "FALSE" or state == "false" or state == "False" or state == "f" or state == "F": 
        print("Disabling Email Notification")
        data = { 
                "emailCopyOfMessage": {
                "enabled": False
                }
            }          
    
    httpBodyJSON = json.dumps(data) 

    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, data=httpBodyJSON)     
    results = APIRESPONSE.text
    return results

#Usage for setVoicemailEmailNotify()
#results = webex.setVoicemailEmailNotify(accessToken, enableOrDisable, userId, destination)

def addPstnNumber(accessToken, number, orgId, location):
    APIURI = "https://webexapis.com/v1/telephony/config/locations/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + location + "/numbers" + "?orgId=" + orgId

    data = { 
        "phoneNumbers": [ number],
     "state": "ACTIVE"  
    }

    httpBodyJSON = json.dumps(data) 

    APIRESPONSE = requests.post(APIURI, headers=APIHEADER, data=httpBodyJSON) 
    if APIRESPONSE.text == "":
        results = ""
    else: 
        results = APIRESPONSE.json()
    return results

#Usage for addPstnNumber()
#results = webex.addPstnNumber(accessToken, number, orgId, location)


def getLicenses(accessToken, orgId):
    APIURI = "https://webexapis.com/v1/licenses"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "?orgId=" + orgId
  
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER) 
    results = APIRESPONSE.text
    return results

#Usage for getLicenses()
#results = webex.getLicenses(accessToken, orgId)

def updateUser(accessToken, userId, orgId, jsondata):
    APIURI = "https://webexapis.com/v1/people/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + userId + "?callingData=true" + "&orgId=" + orgId

    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, data = json.dumps(jsondata))
    return APIRESPONSE.json()


def getOrganizations(accessToken):
    APIURI = "https://webexapis.com/v1/organizations"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
     
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER) 
    return APIRESPONSE.text

def getOrganizationDetails(accessToken, orgId):
    APIURI = "https://webexapis.com/v1/organizations"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + "/" + orgId
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    return APIRESPONSE.text

def listHuntGroups(accessToken, orgId):
    APIURI = "https://webexapis.com/v1/telephony/config/huntGroups"
    APIURLPARAMETERS = "?orgId=" + orgId
    APIURI = APIURI + APIURLPARAMETERS
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER) 
    huntGroups = APIRESPONSE.text
    return huntGroups

def getHuntGroupDetails(accessToken, locationId, huntGroupId, orgId): 
    APIURI = "https://webexapis.com/v1/telephony/config/locations/" + locationId + "/huntGroups/" + huntGroupId
    APIURLPARAMETERS = "?orgId=" + orgId
    APIURI = APIURI + APIURLPARAMETERS
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER, verify=True) 
    results = APIRESPONSE.json()
    return results

def addHuntGroupAgent(accessToken, locationId, huntGroupId, jsonData, orgId):
    APIURI = "https://webexapis.com/v1/telephony/config/locations/" + locationId + "/huntGroups/" + huntGroupId
    APIURLPARAMETERS = "?orgId=" + orgId
    APIURI = APIURI + APIURLPARAMETERS
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    API_DATA = jsonData
        
    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, data = API_DATA)
    results = APIRESPONSE.text
    return results

def listCallerId(accessToken, userId, orgId):
    APIURI = "https://webexapis.com/v1/people/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + userId + "/features/callerId" + "?orgId=" + orgId
    APIRESPONSE = requests.get(APIURI, headers=APIHEADER) 
    callerId = APIRESPONSE.json()
    return callerId

def updateCallerId(accessToken, userId, orgId, jsondata):
    APIURI = "https://webexapis.com/v1/people/"
    APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
    APIURI = APIURI + userId + "/features/callerId" + "?orgId=" + orgId

    APIRESPONSE = requests.put(APIURI, headers=APIHEADER, data = json.dumps(jsondata))
    return APIRESPONSE.text

#Functions below this point are in progress

# def getAutoAttendants(accessToken, orgId):

#     API_URL_ENDPOINT = "telephony/config/autoAttendants"
#     APIURLPARAMETERS = "?orgId=" + orgId
#     FULL_URL = API_URL_PATH + API_URL_ENDPOINT + APIURLPARAMETERS
  
#     APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
          
#     #bodyPayloadText = json.dumps(data) # This formats the contents of 'data' into proper JSON for sending in the request body
#     APIRESPONSE = requests.get(FULL_URL, headers=APIHEADER) 
#     autoAttendants = APIRESPONSE.text
#     return autoAttendants


# def createUser(accessToken, email, extension, DID, firstName, lastName, location, license, orgId):
#     data = { 
#         "emails": email,
#         #"phoneNumbers": 
#         #{
#          #"type" : "work",
#          #"value" : DID
#         #},
#         "extension": extension,
#         "firstName": firstName,
#         "lastName": lastName,
#         "orgId": orgId,
#         "location": location,
#         "licenses": license
        
#     }
   
#     APIURI = APIURI + "people/" + "?" + "callingData=true"
#     APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}

#     bodyPayloadText = json.dumps(data) 
#     print(bodyPayloadText)
#     APIRESPONSE = requests.post(APIURI, headers=APIHEADER, data = bodyPayloadText) 
#     results = APIRESPONSE.text
#     return results

#     bodyPayloadText = json.dumps(data) 




# def deleteUser(accessToken, userId):
#     APIURI = APIURI + "people/"+ userId
#     APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
#     APIRESPONSE = requests.delete(APIURI, headers=APIHEADER, verify=True) 
    
#     if APIRESPONSE.status_code == 204:
#         print("Deleted Successfully") 
#         return("User Found")
#     else:
#         return("No User Found")
   
# def createCallQueue(accessToken, locationId, name, phoneNumber, extension, firstName, lastName, callPolicies, agents):
#     data = {
#         "locationId" : locationId, 
#         "name": name,
#         "phoneNumber": phoneNumber,
#         "extension": extension,
#         "firstName": firstName,
#         "lastName": lastName,
#         "callPolicies": callPolicies,
#         "agents": agents,
#         "enabled": "true",
#         #"phoneNumbers": 
#         #{
#          #"type" : "work",
#          #"value" : DID
#         #},
          
        
#     }
#     APIURI = APIURI + "telephony/config/locations/"+ locationId + "/queues"
#     APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
#     APIRESPONSE = requests.post(APIURI, headers=APIHEADER, data = bodyPayloadText) 


# def getLicenseDetails(accessToken, licenseId):

#     API_URL_ENDPOINT = "licenses"
#     APIURLPARAMETERS = "/" + licenseId
#     FULL_URL = API_URL_PATH + API_URL_ENDPOINT + APIURLPARAMETERS

#     APIHEADER =   {'Authorization': 'Bearer ' + accessToken,
#                 'Content-Type' : 'application/json',
#                 'Accept' : '*/*'}

#     APIRESPONSE = requests.get(FULL_URL, headers=APIHEADER) 
    
#     return APIRESPONSE


# def getLicenses(accessToken, orgId):

#     API_URL_ENDPOINT = "licenses"
#     APIURLPARAMETERS = "?orgId=" + orgId
#     FULL_URL = API_URL_PATH + API_URL_ENDPOINT + APIURLPARAMETERS
  
#     APIHEADER = {'Authorization': 'Bearer ' + accessToken, 'Content-Type' : 'application/json', 'Accept' : '*/*'}
          
#     #bodyPayloadText = json.dumps(data) # This formats the contents of 'data' into proper JSON for sending in the request body
#     APIRESPONSE = requests.get(FULL_URL, headers=APIHEADER) 
#     licenses = APIRESPONSE.text
#     return licenses

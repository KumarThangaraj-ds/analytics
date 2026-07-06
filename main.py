from fastapi import FastAPI, Header, Request, Body
from starlette.responses import JSONResponse

app = FastAPI(title="analytics")

def GetAnalyticsResult (payload):
    events = payload["events"]
    analytics = {}

    for event in events:
        user = event['user']
        if (analytics.get(user) == None):
            analytics [user] = {}
            analytics [user]["name"] =  user
            if (event['amount'] > 0):
                analytics [user]["amount"] = event['amount']
            else:
                analytics [user]["amount"] = 0
        else:
            if (event['amount'] > 0):
                analytics [user]["amount"] = analytics [user]["amount"] + event['amount']

    return analytics



@app.post("/analytics")
def predict(request: Request, payload: dict = Body(...)):
    
    all_headers = request.headers

    api_key = all_headers.get ("X-API-Key")

    if (api_key == None):
        return JSONResponse(status_code=401, content={"valid": False})
    
    if (api_key != 'ak_6hv5gi4kzogajyvf317nvnp8'):
        return JSONResponse(status_code=401, content={"valid": False})

    analytics = GetAnalyticsResult (payload)
    sum = 0
    topper = ''
    count = 0
    
    for user in analytics:
        if (sum == 0):
            topper = user
        else:
            if (analytics.get(user)['amount'] > analytics.get(topper)['amount']):
                topper = user

        sum = sum+analytics.get(user)['amount']
        count = count+1

    responsebody = { "email":"23ds1000074@ds.study.iitm.ac.in", "total_events": len (payload["events"]), "unique_users": count, "revenue": sum, "top_user": topper}

    return responsebody

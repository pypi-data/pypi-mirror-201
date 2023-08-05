from urllib.parse import urlparse
from flask import request
from urllib.parse import parse_qs
import hashlib
from functools import wraps
import datetime


def validateCredentials(apiSecret):
    def decorator(f):
        @wraps(f)
        def validate(*args, **kwargs):
            try:
                signature = request.headers.get('signature')
                
                parsedUrl = urlparse(request.url)
                query = parse_qs(parsedUrl.query)
                computedSignature = computeSignature(apiSecret, query)
                if computedSignature != signature:
                    return {
                        "message":"Request Expired"
                    }, 401
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                return {
                        "message":"Error in credential validation."
                    }, 500
        return validate 
    return decorator

def computeSignature(apiSecret, query):
    queryKeys = list(query.keys())
    queryKeys.sort()

    queryStringArray = []
    for key in queryKeys:
        queryStringArray.append(key + '=' + query[key][0])

    sortedString = "|".join(queryStringArray)
    hashString = apiSecret + sortedString
    computedHash = hashlib.md5(hashString.encode('utf-8')).hexdigest()
    return computedHash


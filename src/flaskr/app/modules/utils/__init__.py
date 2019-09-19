import json

def getValues(values):
    # data =  getValues(request.form.to_dict())
    #type dictionary: {'{"email":"f@f.com","password":"a","code":"5053"}': ''}

    #type list: ['{"email":"f@f.com","password":"a","code":"5053"}']
    to_list = [k for k in values]

    #type string: "{"email":"f@f.com","password":"a","code":"5053"}"
    string = to_list[0]

    #type: dictionary: {'email': 'f@f.com', 'password': 'a', 'code': '5053'}
    dic = json.loads(string)

    return dic

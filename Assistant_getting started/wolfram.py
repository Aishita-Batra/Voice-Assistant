# Python program to  
# demonstrate creation of an 
# assistant using wolf ram API 
  
import wolframalpha 
  

def removeBrackets(variable):
  return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

# Taking input from user 
text = input('Question: ')
# App id obtained by the above steps 
app_id = "J4URRJ-ULPLQ7XPWP"

while text != "end" :
     
    # Instance of wolf ram alpha  
    # client class 
    client = wolframalpha.Client(app_id) 
      
    res = client.query(text)
    
    # Wolfram cannot resolve the question
    if res['@success'] == 'false':
        print('Question cannot be resolved')
      # Wolfram was able to resolve question
    else:
        result = ''
        # pod[0] is the question
        pod0 = res['pod'][0]
        # pod[1] may contains the answer
        pod1 = res['pod'][1]
        # checking if pod1 has primary=true or title=result|definition
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
          # extracting result from pod1
          result = resolveListOrDict(pod1['subpod'])
          print(result)
          question = resolveListOrDict(pod0['subpod'])
          question = removeBrackets(question)
          #primaryImage(question)
        else:
          # extracting wolfram question interpretation from pod0
          question = resolveListOrDict(pod0['subpod'])
          # removing unnecessary parenthesis
          question = removeBrackets(question)
          # searching for response from wikipedia
          #search_wiki(question)
          print("Search from wiki")
          print(question)
          
    text = input('Question: ')


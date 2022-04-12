# Python program to  
# demonstrate creation of an 
# assistant using wolf ram API 
  
import wolframalpha
import wikipedia
import requests
  

def removeBrackets(variable):
  return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

def wiki_search(question):
    results = wikipedia.search(question)

    if not results:
        print("No results found for your search")
        return

    try:
        page = wikipedia.page(results[0])
    except wikipedia.DisambiguationError as err:  #multiple results for same query (OR) question interpreted in more than one way
        page = wikipedia.page(err.options[0])     #then return 1st option
    except:
        print("Some unexpected error occured. Please try again.")
        return

    #title = page.title.encode('utf-8')
    content = page.summary.encode('utf-8')
    print(content)


def wolf_ram_compute(client, text):
    res = client.query(text)
    
    # question not resolved by wolfram
    if res['@success'] == 'false':
        print('Question cannot be resolved')
      # Wolfram was able to resolve question
    else:
        result = ''
        # pod[0] contains simplified question with only keywords in it.
        pod0 = res['pod'][0]
        # pod[1] may contains the answer
        pod1 = res['pod'][1]
        
        # check if pod1 has primary=true or title=result|definition
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
          # extracting result from pod1
          result = resolveListOrDict(pod1['subpod'])
          print(result)
          question = resolveListOrDict(pod0['subpod'])
          question = removeBrackets(question)
        else:
          # extracting wolfram question interpretation from pod0
          question = resolveListOrDict(pod0['subpod'])
          # removing unnecessary parenthesis for simplicity
          question = removeBrackets(question)
          
          print("Searching from wiki...")
          wiki_search(question)
    







text = input('Question: ')
user_id = "J4URRJ-ULPLQ7XPWP"
client = wolframalpha.Client(user_id) # Instance of wolfram alpha 

while text != "end" :

    wolf_ram_compute(client, text)
    text = input('Question: ')



# Python program to  
# demonstrate creation of an 
# assistant using wolf ram API 
  
import wolframalpha
  
# Taking input from user 
question = input('Question: ')
# App id obtained by the above steps 
app_id = "J4URRJ-ULPLQ7XPWP"

while question != "end" :
     
    # Instance of wolf ram alpha  
    # client class 
    client = wolframalpha.Client(app_id)
      
    # Stores the response from  
    # wolf ram alpha 
    res = client.query(question) 
      
    # Includes only text from the response 
    answer = next(res.results).text
      
    print(answer)
    question = input('Question: ')

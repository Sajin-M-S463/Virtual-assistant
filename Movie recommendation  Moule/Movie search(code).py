import requests
RAPIDAPI_KEY  = "9ac726b243mshf1526d4a4856e28p1c37a8jsn2a37c4adf8a9" 
#url =  "https://imdb8.p.rapidapi.com/title/auto-complete"
RAPIDAPI_HOST =  "imdb8.p.rapidapi.com"
search_string = ""
movie_id = ""
movie_title = ""
movie_year  = ""
top_cast_name = list()
top_crew_name = dict()
api_error = False
def search_movie(search_keyword):
  #titanic
  #response =requests.request("GET", url, headers=headers, params=querystring) 
  url = "https://imdb8.p.rapidapi.com/title/find"
  querystring = {"q":"game of thr"}
  headers={
    "imdb8.p.rapidapi.com": RAPIDAPI_HOST,
    "9ac726b243mshf1526d4a4856e28p1c37a8jsn2a37c4adf8a9": RAPIDAPI_KEY,
    #"Content-Type": "application/json"
    }
  #}
  response =requests.request("GET", url, headers=headers, params=querystring) 
  return response
def search_cast(title_id):
  
  url = "https://imdb8.p.rapidapi.com/title/get-top-cast"
  querystring = {"tconst":"tt0944947"} 
  headers={
    "imdb8.p.rapidapi.com": RAPIDAPI_HOST,
    "9ac726b243mshf1526d4a4856e28p1c37a8jsn2a37c4adf8a9": RAPIDAPI_KEY,
    "Content-Type": "application/json"
        }
    #)
  response = requests.request("GET", url, headers=headers, params=querystring)
  return response
def search_character(movie_id,name_id):
  
  url = "https://imdb8.p.rapidapi.com/title/get-charname-list"
  querystring = {"id":"nm3964231","tconst":"tt0944947","currentCountry":"US","marketplace":"ATVPDKIKX0DER","purchaseCountry":"US"}
  headers={
    "imdb8.p.rapidapi.com": RAPIDAPI_HOST,
    "9ac726b243mshf1526d4a4856e28p1c37a8jsn2a37c4adf8a9": RAPIDAPI_KEY,
    "Content-Type": "application/json"
        }
    #)
  response = requests.request("GET", url, headers=headers, params=querystring)
  return response
def search_crew(movie_id):
  
  url = "https://imdb8.p.rapidapi.com/title/get-top-crew"
  querystring = {"tconst":"tt0944947"}
  headers={
    "imdb8.p.rapidapi.com": RAPIDAPI_HOST,
    "9ac726b243mshf1526d4a4856e28p1c37a8jsn2a37c4adf8a9": RAPIDAPI_KEY,
    "Content-Type": "application/json"
      }
    #)
  response = requests.request("GET", url, headers=headers, params=querystring)
  return response
def display_results():
  if api_error == False:
    print ("Movie Title: " + movie_title)
    print ("Release Year:" + movie_year)
    print ("n")
    print ("Cast:")
    for name in top_cast_name:
      print (name)
    print ("n")
    
    print ("Crew:")
    for role,name in top_crew_name.items():
      print (role.capitalize() + " - " + ",".join(name ))
  else:
    print ("API Error. Please try again later")
if __name__ == "__main__":
  try:
    while len(search_string) <= 2:
      search_string = input("Enter the movie name to search: ")
    print ("Finding the best match for " + search_string + "...  n")
    main_response = search_movie(search_string)
    if(main_response.status_code == 200):
      if "results" in main_response.body:
        
        best_match = main_response.body["results"][0]
        movie_id = best_match["id"][7:-1]  
            
        movie_title = best_match["title"]
            
        movie_year = str(best_match["year"])
        
        cast_response = search_cast(movie_id)
        if(cast_response.status_code == 200):
          top_cast_id = cast_response.body[0:4]
          for cast_id in top_cast_id:
            
            char_response = search_character(movie_id,cast_id[6:-1])
            if(char_response.code == 200):
              top_cast_name.append(char_response.body[cast_id[6:-1]]["name"]["name"])        
            else:
              print ("Cannot fetch the star cast for " + movie_title)
          crew_response = search_crew(movie_id)
          if crew_response.status_code == 200:
            for crew,details in crew_response.body.items():
              
              if len(details) > 0:
                for data in details:
                
                  if(False == top_crew_name.has_key(crew)):  
                    top_crew_name[crew] = list()
                    
                  top_crew_name[crew].append(data["name"])
          else:
            print ("Unable to fetch crew data for " + movie_title)
            api_error = True
        else:
          print ("Unable to fetch the star cast for " + movie_title)
          api_error = True
        display_results()
    else:
      print ("Invalid request or error in response")
      api_error = True
  except Exception as e:
    print ("Error")   
    print (e)

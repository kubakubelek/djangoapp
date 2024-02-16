from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
import requests
import json
from main.models import Movies
# Create your views here.
#def response(request):
#    return HttpResponse()
def main(request):
    return render(request, 'main/main.html')
def shuffle_divs2(request):
    movies=[]
    list_with_years=[i for i in range(1880,2024)]
    random.shuffle(list_with_years)
    for year in list_with_years:
        movies_with_title = Movies.objects.filter(year=year)
        count_movies = movies_with_title.count()
        if count_movies>3:
            liczba=random.randint(1,400)
            for movie in movies_with_title[0:4]:
                movies.append(f"{movie.title}")
                if movie.id==liczba:
                    liczba=random.randint(1,400)

            single=Movies.objects.get(pk=liczba)
            movies.append(f"{single.title}")
            break
        else:
            pass

    random.shuffle(movies)
    right_answer=movies.index(f"{single.title}")+1
    #for i in range(len(movies)):
    #    movies[i]=movies[i]+" "+ str(right_answer)


    return JsonResponse({'shuffled_texts':movies, 'right': right_answer})

def shuffle_divs(request):
    data = json.loads(request.body)
    try:
        score = str(int(data['scoreText'])+1)
    except Exception:
        score=0
    return generating_filters_to_url(score)


def creating_response(correct_url, opposite_url, text, score):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5OTdhNzY4OGQxYzIyZTU0ODczZDk1YzEyMzA1ZWRiNiIsInN1YiI6IjY1YTI3NTRiYjdiNjlkMDEyNTNiZjI4MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.yJh0z1Q-zYFTtPCUo-ATUyxzSPi-R5-BIP4_ZcIGATw"
    }
    response = requests.get(correct_url, headers=headers)
    data_json = json.loads(response.content)
    correct_movies = []

    for i in data_json['results']:
        securl=i['poster_path']
        url_to_img='https://image.tmdb.org/t/p/w500'+securl
        correct_movies.append((i['title'], url_to_img))
        print(url_to_img)
    answer = random.sample(correct_movies, 4)
    response = requests.get(opposite_url, headers=headers)
    data_json = json.loads(response.content)
    opposite_movies = []
    for i in data_json['results']:
        securl = i['poster_path']
        url_to_img = 'https://image.tmdb.org/t/p/w500' + securl
        opposite_movies.append((i['title'], url_to_img))
    one_of_opposite_movies=random.sample(opposite_movies, 1)[0]
    answer.append(one_of_opposite_movies)
    random.shuffle(answer)
    right=answer.index(one_of_opposite_movies)+1
    return JsonResponse({'shuffled_texts': answer, 'right': right, 'text':text, 'score': score})
def url_year(score):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=vote_count.desc"
    year_for_url=random.randint(1960,2024)
    year_for_opposite_url=random.randint(1960,2023)
    while abs(year_for_opposite_url-year_for_url)<15 or year_for_opposite_url==year_for_url:
        year_for_opposite_url = random.randint(1960, 2023)
    correct_url=url+f'&primary_release_year={year_for_url}'
    opposite_url=url+f'&primary_release_year={year_for_opposite_url}'
    text='There are 4 movies released in the same year and 1 Impostor '
    return creating_response(correct_url,opposite_url,text, score)
def url_genre(score):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=vote_count.desc"
    genres = ['37', '10752', '878', '10749', '9648', '10402', '27', '36', '14', '99', '80', '35', '16','28']

    genre_for_url=random.choice(genres)
    correct_url=url+'&with_genres='+genre_for_url+'&page='+str(random.randint(1,5))
    opposite_url=url+'&without_genres='+genre_for_url+'&page='+str(random.randint(1,7))
    text='There are 4 movies in the same genre and 1 Impostor '
    return creating_response(correct_url,opposite_url,text,score)

def generating_filters_to_url(score):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=vote_count.desc"
    choices=['genre','year']
    choice=random.choice(choices)

    #if choice=='director':
        #pass
        #director_url()
    if choice=='genre':
        return url_genre(score)
    elif choice=='year':
        return url_year(score)




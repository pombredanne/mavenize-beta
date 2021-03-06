from movie.models import Movie
import urllib as urllib
import urllib2,json
import os,glob
from django.template import defaultfilters
import unicodedata
author_list = []

BASE='http://api.rottentomatoes.com/api/public/v1.0/'
KEY='mz7z7f9zm79tc3hcaw3xb85w'
movieURL=BASE+'movies.json'

def main():


    print('starting.')
    checkStrSet = set([])
    for movie in Movie.objects.order_by("-theater_date"):

        movieSearchURL=movieURL+'?'+urllib.urlencode({'apikey':KEY, 'q': movieName})
        movieData = json.loads(urllib2.urlopen(movieSearchURL).read())
        movieData = movieData['movies']
        #We need to find the right movie now, because we don't want to just take the 1st result
        #  Filter by year.
        correctMovieID=-1
        for movietomatoe in movieData:
            if int(movietomatoe['alternate_ids']['imdb']) == movie.imdb_id:
                correctMovieID=movietomatoe['id']
                break
        if correctMovieID==-1:
            raise Exception('Error: Cannot find movie with that year and name.')

        print('Getting reviews for movie '+movie.title)
        singlemoviereviews  = getAuthors(movie,correctMovieID)
        for review in singlemoviereviews:
            checkStr = review['critic'][0:5]+review['link'][7:14]
            print('checkStr is '+ checkStr)
            if not checkStr in checkStrSet:
                author_list.append(tempset)
                print('Successfully added author set for'+movie.tite)
                checkStrSet.add(checkStr)

def getAuthors(movie,movieid):
    print('Get authors from'+movie.title)
    title = movie.title
    imdb_id = movieid
    reviewSearchURL=BASE+'movies/'+str(imdb_id)+'/reviews.json?'

    reviewSearchURL = reviewSearchURL+urllib.urlencode({'apikey':KEY})
    print('Search url is ' + reviewSearchURL)
    reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
    reviewData = reviewData['reviews']
    print('Printing reviewData')
    print(reviewData)
    returnSet=[]
    for review in reviewData:
        returnSet.append({'author':review['critic'],
        'link':review['links']['review']})
    return returnSet
        #tempset now an array of dictionaries that contain
        #author and url
        #Check whether author and url combination exists
        #If found duplicate, set addMovie to false

        #We want to have one url for each unique author


def downloadJSON(movie,directory,movieid):
    print('...Grabbing JSONs for ' + movie.title)
    title = movie.title
    imdb_id = movieid
    reviewSearchURL=BASE+'movies/'+str(imdb_id)+'/reviews.json?'
    reviewSearchURL = reviewSearchURL+urllib.urlencode({'apikey':KEY})
    #print('Search url is ' + reviewSearchURL)
    reviewData=json.loads(urllib2.urlopen(reviewSearchURL).read())
    reviewData = reviewData['reviews']
    if len(reviewData) > 0:
        with open(directory+'/'+str(movie.imdb_id),'wb') as fp:
            json.dump(reviewData,fp)
        print('...Successfully dumped  JSON of ' + movie.title)
    else:
        print('...No reviews available for movie ' + movie.title)
        print('...Skipping write')
    #f = open(directory+'/'+str(imdb_id), 'w')
    #f.write(reviewData)
    #f.close()
#Indexes 0 to # movies - 1
def downloadJSONRange(directory,start,end):
    if os.path.exists(directory) == False:
        try:
            os.mkdir(directory)
            print('Directory created: ' + directory)
        except Exception as err:
            print('Error creating dir')
            exit(2)
    #print('destination directory is ' + directory)
    for movie in Movie.objects.order_by("-theater_date")[start:end]:
        print('Starting download of ' + movie.title)
	decodedTitle = unicodedata.normalize('NFKD',movie.title).encode('ascii','ignore')
        movieSearchURL=movieURL+'?'+urllib.urlencode({'apikey':KEY, 'q': decodedTitle})
        movieData = json.loads(urllib2.urlopen(movieSearchURL).read())
        movieData = movieData['movies']
        #We need to find the right movie now, because we don't want to just take the 1st result
        #  Filter by year.
        correctMovieID=-1
        matchByYear = False
        for movietomatoe in movieData:
            try:
                #print('tomatoes id get '+ movietomatoe['alternate_ids']['imdb'])
                #print('database id get ' + str(movie.imdb_id))
                if int(movietomatoe['alternate_ids']['imdb']) == movie.imdb_id:
                    correctMovieID=movietomatoe['id']
                    break
            except KeyError:
                print('...No imdb found, match by year')
                matchByYear = True
            except:
                print('...invalid imdb id found')
                
        if matchByYear == True:
            try:

                for movietomatoe in movieData:
                    movieYear = defaultfilters.date(movie.theater_date,'Y')
                    #print('tomatoes date get ' + str(movietomatoe['year']))
                    #print('database date get ' + movieYear)
                    if movietomatoe['year'] == int(movieYear):
                        correctMovieID = movietomatoe['id']
                        break
            except:
		print('...No year value set, skipping.')

        if correctMovieID==-1:
            
            print('...Skipping: Cannot find movie with that year ' + defaultfilters.date(movie.theater_date,'Y') + 'and name ' + movie.title)
            print('...Skipping write.')

        elif correctMovieID != -1:
            downloadJSON(movie,directory,correctMovieID)
            print('...Finished processing movie '+ movie.title)


def extractAuthors(directory,outdir,outname):
    os.chdir(directory)
    f = open(outdir + '/' + outname,'w')
    print('listing current files')
    for filename in os.listdir('.'):
        print(filename)
    for files in os.listdir('.'):
        print('Current file is ' + files)
        listofreviews = json.loads(open(files,'r').read())
        for review in listofreviews:
            try:
                authorName = review['critic']
                print('authorname is: '+authorName)
            except KeyError:
                print('cannot find author name')
                authorName = ' '
            try:
                link = review['links']['review']
                print('link is' + link)
            except KeyError:
                print('cannot find link')
                link = ' '
            tempstr = authorName + ' : ' + link
            f.write(tempstr)
            f.write('\n\n')
    f.close()






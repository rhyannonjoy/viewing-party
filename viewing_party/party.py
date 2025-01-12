import statistics

# Wave 1
def create_movie(title, genre, rating):
    """
    Takes in three parameters: title, genre,
    and rating to build and return dictionary movie.
    If any of these parameters are falsy, returns None.
    """
    if title and genre and rating:
        movie = {
            "title": title,
            "genre": genre,
            "rating": rating,
             }
        return movie


def add_to_watched(user_data, movie):
    """
    Takes in two parameters: user_data and movie.
    User_data is a dictionary with a list of dictionaries.
    Add each movie, its own dictionary, to list "watched."
    Returns user_data.
    """
    if movie:
        user_data["watched"].append(movie)
    return user_data


def add_to_watchlist(user_data, movie):
    """
    Takes two parameters user_data and movie.
    User_data is a dictionary with a list of dictionaries.
    Add each movie, it's own dictionary, to list "watchlist."
    Returns user_data.
    """
    user_data["watchlist"].append(movie)
    return user_data
    

def watch_movie(user_data, title):
    """
    Takes in two parameters user_data and title.
    Removes title from list watchlist, adds to list watched.
    Returns user_data.
    """
    watchlist = user_data["watchlist"]
    watched = user_data["watched"]
    
    for movie in watchlist:
        if title in movie["title"]:
            watchlist.remove(movie)
            watched.append(movie)
    
    return user_data


# Wave 2
def get_watched_avg_rating(user_data):
    """
    Takes in parameter user_data,
    returns the average rating among the movies.
    """
    watched = user_data["watched"]
    rating_sum = 0
    
    if len(watched) == 0:
        average_rating = 0
    for movie in watched:
        rating_sum += movie["rating"]  
        average_rating = rating_sum / len(watched)
    return average_rating


def get_most_watched_genre(user_data):
    """
    Takes in parameter user_data,
    returns the most watched genre among the movies.
    """
    most_watched = user_data["watched"]
    genres = []
    if len(most_watched) == 0:
        return None
    for movie in most_watched:
        genres.append(movie["genre"])
    # consider the big o notation of importing statistics, mode    
    return statistics.mode(genres)


# Wave 3
def get_unique_watched(user_data):
    """
    Takes one parameter user_data,
    returns list of dictionaries unique_watched, 
    representing movies that the user has watched,
    but none of their friends have watched.
    """
    user_watched = user_data["watched"]
    friends_watched = user_data["friends"]
    
    friends_titles = []
    for friend in friends_watched:
        for title in friend["watched"]:
            friends_titles.append(title['title'])

    unique_watched = []

    for title in user_watched:
        if title["title"] not in friends_titles:
            unique_watched.append(title)

    return unique_watched
    
    
def get_friends_unique_watched(user_data):
    """
    Takes in one parameter user_data,
    returns list of dictionaries friends_unique_watched,
    representing movies at least one friend has watched,
    but the user has not watched. 
    """
    user_watched = user_data["watched"]
    friends_watched = user_data["friends"]
    
    user_movies = [movie["title"] for movie in user_watched]
    friends_unique_watched = []

    for friend in friends_watched:
        for movie in friend["watched"]:
            if movie["title"] not in user_movies:
                if movie not in friends_unique_watched:
                    friends_unique_watched.append(movie)

    return friends_unique_watched


# Wave 4
def user_has_watched(movie, watched_movies):
    """
    Takes two parameters, movie and watched_movies.
    Determines if user has watched a movie,
    returns a Boolean. 
    """
    if movie in watched_movies:
        return True
    else:
        return False


def in_friends_watchlist(movie, watched_by_friends):
    """
    Takes two parameters, movie and watched_by_friends.
    Determines whether at least one friend has watched the movie.
    Returns a Boolean.
    """
    if movie in watched_by_friends:
        return True
    else:
        return False


def in_users_subscriptions(host, subscriptions):
    """
    Takes two parameters, host and subscriptions.
    Determines whether the movie host is a service subscription.
    Returns a Boolean.
    """
    if host in subscriptions:
        return True
    else:
        return False


def get_friends_movies(user_data):
    """
    Takes in one parameter user_data.
    Determines which movies friends has watched.
    Returns list of dictionaries, movies.
    """
    titles = set()
    friends = user_data["friends"]
    movies = []
    for friend in friends:
        for movie in friend["watched"]:
            if movie["title"] not in titles:
                movies.append(movie)
                titles.add(movie["title"])
    return movies


def get_available_recs(user_data):
    """
    Takes in one parameter user_data.
    Determines movies user has not watched, at least
    one friend has watche, and is available to stream.
    Returns list of dictionaries available_recs.
    """
    user_watched = user_data["watched"]
    friends_movies = get_friends_movies(user_data)
    available_recs = []

    if len(friends_movies) == 0:
        return []

    user_watched_titles = set()
    for movie in user_watched:
        user_watched_titles.add(movie["title"])

    for movie in friends_movies:
        if movie["title"] not in user_watched_titles:
            if in_users_subscriptions(movie["host"], user_data["subscriptions"]):
                available_recs.append(movie)

    return available_recs


# Wave 5
def get_new_rec_by_genre(user_data):
    """
    Takes in one parameter, user_data.
    Determines movies user has not watched, at least one
    friend has watched, and matches most frequent genre.
    Returns list of dictionaries new_rec_by_genre.
    """
    user_watched = user_data["watched"]
    friends_movies = get_friends_movies(user_data)

    if len(user_watched) == 0 or len(friends_movies) == 0:
        return []

    user_watched_set = set()
    for movie in user_watched:
        user_watched_set.add(movie["title"])

    new_rec_by_genre = []
    for movie in friends_movies:
        if movie["title"] not in user_watched_set:
            if movie["genre"] == get_most_watched_genre(user_data):
                new_rec_by_genre.append(movie)
    return new_rec_by_genre


def get_rec_from_favorites(user_data):
    """
    Takes one parameter, user_data.
    Determines movies in user's list of dictionaries 
    "favorites," and has not been watched by friends.
    Returns list of dictionaries rec_from_favorites.
    """
    watched = user_data["watched"]
    favorites = user_data["favorites"]

    if len(watched) and len(favorites)== 0:
        return []

    friends_movies = get_friends_movies(user_data)
    rec_from_favorites = []
    for movie in user_data["favorites"]:
        if movie not in friends_movies:
            rec_from_favorites.append(movie)
    return rec_from_favorites



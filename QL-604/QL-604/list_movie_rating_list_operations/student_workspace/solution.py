class MovieManager:
    """Manage movie records and provide analysis operations."""

    def __init__(self):
        """Initialize the movie list with sample data."""
        self.movies = [
            {"title": "Inception", "genre": "Sci-Fi", "rating": 8.8},
            {"title": "3 Idiots", "genre": "Comedy", "rating": 8.4},
            {"title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6},
            {"title": "Dangal", "genre": "Drama", "rating": 8.3},
            {"title": "War", "genre": "Action", "rating": 6.5}
        ]

    def count_movies_by_genre(self, genre: str) -> int:
        """
        Count the number of movies in a specific genre.
        
        Args:
            genre: The genre to filter by
            
        Returns:
            Count of movies in the specified genre
        """
        count = 0
        for movie in self.movies:
            if movie["genre"] == genre:
                count += 1
        return count

    def find_highest_rated_movie(self) -> str:
        """
        Find the movie with the highest rating.
        
        Returns:
            String in format "Title - Rating"
        """
        highest = self.movies[0]
        for movie in self.movies:
            if movie["rating"] > highest["rating"]:
                highest = movie
        return f"{highest['title']} - {highest['rating']}"

    def calculate_average_rating(self) -> float:
        """
        Calculate the average rating of all movies.
        
        Returns:
            Average rating rounded to 2 decimal places
        """
        total_rating = sum(movie["rating"] for movie in self.movies)
        average = total_rating / len(self.movies)
        return round(average, 2)

    def list_top_rated_movies(self) -> str:
        """
        List all movies with rating >= 8.
        
        Returns:
            Comma-separated string of movie titles with rating >= 8
        """
        top_movies = [movie["title"] for movie in self.movies if movie["rating"] >= 8]
        return ", ".join(top_movies)

    def check_movie(self, title: str) -> str:
        """
        Check if a movie exists by title and display its details.
        
        Args:
            title: The movie title to search for
            
        Returns:
            Movie details or "not found" message
        """
        for movie in self.movies:
            if movie["title"] == title:
                return f"Genre {movie['genre']} - Rating {movie['rating']}"
        return "not found"

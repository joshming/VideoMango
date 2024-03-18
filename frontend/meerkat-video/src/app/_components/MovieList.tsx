import Link from "next/link";

type Movie = {
    id: number
    title: string
}

async function getMovies(): Promise<Movie[]> {
   const response = await fetch("http://localhost:8000/movies");
   if (!response.ok) {
     throw new Error("Bad")
   }
   return response.json();
}

export default async function MovieList() {
    const movies= await getMovies();
    const movieButtons = movies.map((movie) => <Link href={`/watch/${movie.id}`}>
            <button
                className="moviebutton"
                key={movie.id}
                id={`${movie.id}`}>{`${movie.title}`}
            </button>
        </Link>
    );
    // const movieButtons = null;
    return (
      <div className="purplebox blockdisplay">
        <div>
          <h2>What would you like to watch?</h2>
          <div>
              {
                movieButtons && movieButtons.map(e => e)
              } 
          </div>
        </div>
      </div>
    );
}
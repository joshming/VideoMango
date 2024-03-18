 import Link from "next/link";
import {Movie} from "@/app/watch/page";

export default function MovieList( {movies} : { movies: Movie[]}) {

    const movieButtons = movies.map(movie =>
        <Link href={`/watch/${movie.id}`}>
            <button
                className="moviebutton"
                key={movie.id}
                id={`${movie.id}`}>{`${movie.title}`}
            </button>
        </Link>
    );
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
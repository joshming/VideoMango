import MovieList from "@/app/_components/MovieList";
import Image from 'next/image'
import NavBar from "../_components/NavBar";

export type Movie = {
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

export default async function Watch() {
    const movieList = await getMovies();

    return (
      <div>
          <NavBar />
          <div className="borderleft"/>
          <div className="bodyarea">
            <MovieList movies={movieList} />
          </div>
          <div className="borderright"/>
      </div>
    );
}
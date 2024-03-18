import MovieList from "@/app/_components/MovieList";

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
        <div className={`h-full flex flex-col justify-center text-center m-10`}>
            <MovieList movies={movieList} />
        </div>
    );
}
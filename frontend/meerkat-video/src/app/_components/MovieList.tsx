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
                className={`bg-amber-200 w-24 p-2 rounded-md border-2 border-amber-200 hover:bg-transparent mr-5`}
                key={movie.id}
                id={`${movie.id}`}>{`${movie.title}`}
            </button>
        </Link>
    );
    return (
      <div className={`h-full flex flex-col justify-center text-center`}>
          <h1>What would you like to watch?</h1>
          <div className={`m-20 flex justify-center text-center`}>
              {
                movieButtons && movieButtons.map(e => e)
              }
          </div>
      </div>
    );
}
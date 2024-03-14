import Video from "@/app/_components/VideoComponent";

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

export default async function Watch() {
    const movies= await getMovies();
    const movieButtons = movies.map((movie) => <button
        className={`bg-amber-200 w-24 p-2 rounded-md border-2 border-amber-200 hover:bg-transparent mr-5`}
        key={movie.id}
        id={`${movie.id}`}>{`${movie.title}`}
        </button>
    );
    return (
      <div className={`h-full w-full flex flex-col justify-center text-center m-10`}>
          <h1>What would you like to watch?</h1>
          <div className={`m-20 flex justify-center text-center`}>
              {
                movieButtons && movieButtons.map(e => e)
              }
          </div>
      </div>
    );
}
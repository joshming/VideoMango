import MovieList from "@/app/_components/MovieList";

export default async function Watch() {
    return (
      <div className={`h-full flex flex-col justify-center text-center m-10`}>
          <MovieList />
      </div>
    );
}
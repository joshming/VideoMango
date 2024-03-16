import Video from "@/app/_components/VideoComponent";

type Movie = {
    id: number
    title: string
}

async function getMovieInformation(id: number): Promise<Movie> {
   const response = await fetch(`http://localhost:8000/movie/${id}`);
   if (!response.ok) {
     throw new Error("Bad");
   }
   return response.json();
}

export default async function VideoPlayer({ params }: {
    params: { id: number }
}) {
    const movieInformation : Movie = await getMovieInformation(params.id);

    return (
        <div className={`flex flex-col justify-center text-center`}>
            <h1 className={`m-10`}>Let's watch that movie {movieInformation.title}</h1>
            <Video videoId={params.id}/>
        </div>
    );
}
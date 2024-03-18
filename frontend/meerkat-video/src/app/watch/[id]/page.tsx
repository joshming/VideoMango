import Video from "@/app/_components/VideoComponent";
import NavBar from "@/app/_components/NavBar";

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
        <div>
            <NavBar />
            <div className="borderleft"/>
            <div className="bodyarea">
                <div className="purplebox">
                    <h1>Now playing: {movieInformation.title}</h1>
                </div>
                <div className="purplebox">
                    {/* <h1 className={`m-10`}>Let's watch that movie {movieInformation.title}</h1> */}
                    <Video videoId={params.id}/>
                </div>
            </div>
            <div className="borderright"/>
        </div>
    );
}
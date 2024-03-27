import Video from "@/app/_components/VideoComponent";
import NavBar from "@/app/_components/NavBar";
import Comment from "@/app/_components/Comment";

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
                    <Video videoId={params.id}/>
                </div>
            </div>
            <div className="borderright"/>
            <div className="flex justify-center">
                <div className={`flex flex-col bg-off-white rounded-md w-4/5 p-5`}>
                    <h2>Comments</h2>
                    <Comment id={params.id}/>
                </div>
            </div>
        </div>
    );
}
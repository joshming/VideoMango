import Image from "next/image";
import Video from "@/app/_components/VideoComponent";

async function getMovies() {
   const response = await fetch("http://localhost:8000/movies");
   if (!response.ok) {
     throw new Error("Bad")
   }
   return response.json();
}

export default function Home() {
  const movies = getMovies();
  console.log(movies);
  return (
    <main className="">
        <Video videoId={1}/>
    </main>
  );
}

import MovieList from "@/app/_components/MovieList";
import Image from 'next/image'
import NavBar from "../_components/NavBar";

export default async function Watch() {
    return (
      <div>
          <NavBar />
          <div className="borderleft"/>
          <div className="bodyarea">
            <MovieList /> 
            <div className="purplebox">
              <h2>Don't see any movies?</h2>
              <h3>Upload one now --- add instructions ---</h3>
            </div>
          </div>
          <div className="borderright"/>
      </div>
    );
}
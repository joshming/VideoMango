import NavBar from "./_components/NavBar"
import Image from 'next/image'
import Video from "@/app/_components/VideoComponent"
import Link from "next/link"

export default function Home() {
  return (
    <main>
        <NavBar/>
        <div className="borderleft"/>
        <div className='bodyarea'>
          <div className="purplebox">
            <div className="imgcontainer">
              <Image
                src="/meerkats.png"
                height={400}
                width={400}
                // layout="fill"
                alt="Cartoon picture of meerkats programming"
            />
          </div>
          <div style={{ margin: '15px' }}>
            <h2>Welcome to VideoMango!</h2>
            <h3>This is a video streaming platform to allow you and your friends watch movies together.</h3>
            <h3></h3>
            <br></br>
            <h3>Made by Joshua, Nicolas, Bartek, Julia</h3>
          </div>
        </div>
        {/* <div className="purplebox">
          <h2>Description</h2>
        </div> */}
      </div>
      <div className="borderright" />
    </main>
  );
}

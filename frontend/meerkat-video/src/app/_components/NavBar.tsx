import Image from 'next/image'
import Link from "next/link"
import Login from "@/app/_components/Login";

export default function NavBar() {
    return (
        <div className="nav">
            <Image 
                className="image"
                src='/logofull.png'
                height={200}
                width={200}
                alt="Mango icon"
            />
            <div className="links">
                <Link className="navlink" href={`/`}>About</Link>
                <Link className="navlink" href={`/watch`}>Watch</Link>
                {/* <Link className="navbutton" href={`/login?modal=true`}> Login </Link> */}
                <Login/>
                <Link className="navlink" href={`/signup?modal=true`}> Sign Up </Link>
            </div>
        </div>
    );
}
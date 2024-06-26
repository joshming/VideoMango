import Image from 'next/image'
import Link from "next/link"
import Login from "@/app/_components/Login";

export default function NavBar() {
    return (
        <div className="nav">
            <Link href={`/watch`}>
                <Image
                className="image"
                src='/logofull.png'
                height={160}
                width={160}
                alt="Mango icon"
            />
            </Link>
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
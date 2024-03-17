import Video from "@/app/_components/VideoComponent";
import Link from "next/link";

export default function Home() {
  return (
    <main className="flex justify-center">
      <Link href={`/login`}> Login </Link>
      <Link href={`/signup`}> Sign Up </Link>
    </main>
  );
}

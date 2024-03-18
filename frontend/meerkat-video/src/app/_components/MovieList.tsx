'use client';

import Cookies from 'js-cookie'
import {useEffect} from 'react'
import {useRouter} from 'next/navigation'
import Link from "next/link";
import {Movie} from "@/app/watch/page";

export default function MovieList( {movies} : { movies: Movie[]}) {
    const router = useRouter();

    // useEffect(() => {
    //     const token = Cookies.get('token');
    //     const user = Cookies.get('user');
    //     if (!token || !user) {
    //         router.replace('/');
    //         return;
    //     }
    //
    //     const validateToken = async () => {
    //         const res = await fetch(`/api/auth?username=${user}&token=${token}`);
    //
    //         if (!res.ok) {
    //             router.replace('/');
    //         }
    //     }
    //
    //     validateToken()
    // }, [router])

    const movieButtons = movies.map(movie =>
        <Link href={`/watch/${movie.id}`}>
            <button
                className={`bg-amber-200 w-24 p-2 rounded-md border-2 border-amber-200 hover:bg-transparent mr-5`}
                key={movie.id}
                id={`${movie.id}`}>{`${movie.title}`}
            </button>
        </Link>
    );

    return (
        <div className={`h-full flex flex-col justify-center text-center`}>
            <h1>What would you like to watch?</h1>
            <div className={`m-20 flex justify-center text-center`}>
                {
                    movieButtons && movieButtons.map(e => e)
                }
            </div>
        </div>
    );
}
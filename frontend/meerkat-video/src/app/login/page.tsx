'use client';

import React, { useState, FormEvent} from "react";
import { useRouter } from 'next/navigation';
import Error from "@/app/_components/Error";

export default function Login() {
    const router = useRouter();
    const [isSuccess, setIsSuccess] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            const formData = new FormData(event.currentTarget);
            let requestBody : {} = {};
            // @ts-ignore
            formData.forEach((value, key) => requestBody[key] = value);

            const response = await fetch('http://localhost:8000/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const data = await response.json()
                console.log(data)
                setIsSuccess(false)
                setError(data["message"])
                return;
            }
            router.push('/watch');
        } catch (error) {
            setIsSuccess(false);
            console.log(error)
        }
    }

    return (
      <main>
        <div className="flex justify-center">
          <div className="backdrop-blur-md bg-amber-200 absolute p-4 text-center transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 rounded-2xl">
            <h1 className="text-xl">Login</h1>
              { isSuccess ? <></> : <Error message={error} /> }
            <form onSubmit={onSubmit}>
                <div className="grid grid-cols-3 gap-4 m-5 justify-center">
                    <div>
                        <label htmlFor="">Username</label>
                    </div>
                    <div className="col-span-2">
                        <input className="w-full rounded-sm bg-tan" type="text" name="username" required/>
                    </div>
                    <div>
                        <label htmlFor="">Password</label>
                    </div>
                    <div className="col-span-2">
                        <input className="w-full rounded-sm bg-tan" type="password" name="password" required/>
                    </div>
                    <div></div>
                    <button className="bg-sage p-2 rounded-xl hover:bg-amber-600">Login</button>
                </div>
            </form>
          </div>

        </div>
      </main>
    );
  }
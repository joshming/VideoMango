'use client';

import {useRouter} from "next/navigation";
import {FormEvent, useState} from "react";
import Error from "@/app/_components/Error";

export default function SignUp() {
    const router = useRouter();
    const [isSuccess, setIsSuccess] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            const formData = new FormData(event.currentTarget);
            const username = formData.get("username");
            const password = formData.get("password");
            const confirm = formData.get("confirm");

            if (confirm !== password) {
                setIsSuccess(false);
                setError("Passwords don't match");
                return;
            }

            const authJson = JSON.stringify({username, password})
            const response = await fetch('/api/create-account', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: authJson
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
                <div
                    className="backdrop-blur-md bg-amber-200 absolute p-4 text-center transform -translate-x-1/2 -translate-y-1/2 top-1/2 left-1/2 rounded-2xl">
                    <h1 className="text-3xl font-medium">So you like Meerkats?</h1>
                    {isSuccess ? <></> : <Error message={error}/>}
                    <form onSubmit={onSubmit}>
                        <div className="grid grid-cols-3 gap-4 m-5 justify-center">
                            <div>
                                <label htmlFor="">Username</label>
                            </div>
                            <div className="col-span-2">
                                <input className="w-full rounded-sm bg-tan" type="text" name="username"/>
                            </div>
                            <div>
                                <label htmlFor="">Password</label>
                            </div>
                            <div className="col-span-2">
                                <input className="w-full rounded-sm bg-tan" type="password" name="password"/>
                            </div>
                            <div>
                                <label htmlFor="">Confirm Password</label>
                            </div>
                            <div className="col-span-2">
                                <input className="w-full rounded-sm bg-tan" type="password" name="confirm"/>
                            </div>
                            <div></div>
                            <button className="bg-sage p-2 rounded-xl hover:bg-amber-600">Sign Up</button>
                        </div>
                    </form>
                </div>

            </div>
        </main>
    );
}
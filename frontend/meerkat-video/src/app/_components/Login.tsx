'use client';

import React, { useState, FormEvent, useRef, useEffect } from "react";
import { useRouter } from 'next/navigation';
// import Error from "@/app/_components/Error";
import { useSearchParams, usePathname } from "next/navigation";
import Link from "next/link"

export default function Login() {
    const router = useRouter();
    const [isSuccess, setIsSuccess] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    // const searchParams = useSearchParams();
    // const modal = searchParams.get("modal");
    // const pathname = usePathname();

    const [showModal, setShowModal] = useState(false);
    const openModal = () => setShowModal(true);
    const closeModal = () => setShowModal(false);

    // useEffect(() => { // like component did mount
    //     const handleClickOutside = (event: MouseEvent) => {
    //         console.log("here");
    //         const modalBox = document.getElementById('modal-box');
    //         if (modalBox && !modalBox.contains(event.target as Node)) {
    //             console.log("here2");
    //             closeModal();
    //         }
    //     };

    //     document.addEventListener('click', handleClickOutside);
    //     return () => {
    //         document.removeEventListener('click', handleClickOutside);
    //     };
    // }, []);

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        try {
            const formData = new FormData(event.currentTarget);
            let requestBody: {} = {};
            // @ts-ignore
            formData.forEach((value, key) => requestBody[key] = value);
            const response = await fetch('/api/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const data = await response.json()
                console.log("Error" + JSON.stringify(data));
                setIsSuccess(false)
                setError(data["message"])
                return;
            }
            closeModal();
            router.push('/watch');
        } catch (error) {
            setIsSuccess(false);
            console.log(error)
        }
    }

    return (
        <>
            {!isSuccess && <button className="navbutton" onClick={openModal}>Log in</button>}
            {showModal &&
                <div className="modal">
                    <div className="modalbox" id="modal-box">
                        <div style={{display: "flex", justifyContent: "space-between", padding: 5}}>
                        <h1 className="text-xl">Login</h1>
                        <button onClick={closeModal} style={{margin: 10}}>&#10060;</button>
                        </div>
                        {isSuccess ? <></> : <h1></h1>}
                        <form onSubmit={onSubmit}>
                            <div className="grid grid-cols-3 gap-4 m-5 justify-center">
                                <div>
                                    <label htmlFor="">Username</label>
                                </div>
                                <div className="col-span-2">
                                    <input className="w-full rounded-sm bg-tan" type="text" name="username" required />
                                </div>
                                <div>
                                    <label htmlFor="">Password</label>
                                </div>
                                <div className="col-span-2">
                                    <input className="w-full rounded-sm bg-tan" type="password" name="password" required />
                                </div>
                                <div></div>
                                <button className="bg-sage p-2 rounded-xl hover:bg-amber-600">Login</button>
                            </div>
                        </form>
                    </div>
                </div>
            }
        </>
    );
}
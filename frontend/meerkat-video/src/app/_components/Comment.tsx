'use client';

import {useEffect, useState} from "react";

type message = {
    user: string
    message: string
    time: string
}

type Comments = {
    users: string[]
    messages: message[]
}

// interval is in milliseconds -- default is 5000ms, change it as you want to
const FETCH_DATA_INTERVAL = 5000;

export default function Comment({id}: { id: number }) {

    const [comments, setComments] = useState<JSX.Element[] | null>(null);
    const [newComment, setNewComment] = useState<string>('');
    const [refresh, setRefresh] = useState(false);
    const fetchData = async () => {
        try {
            console.log("fetching...")
            const response = await fetch(`http://localhost:3000/api/comments?id=${id}`, {
                method: 'GET'
            });
            const data: Comments = await response.json();
            const commentJSX = data.messages.map(message => {
                return (
                    <div className={`grid grid-cols-4 grid-rows-2 w-full mb-2`}>
                        <h3 className={`col-span-4 row-span-1 m-0 font-bold`}>{message.user}:</h3>
                        <p className={`col-span-3`}>{message.message.replaceAll("`", "'")}</p>
                        <p className={`col-span-1`}>{message.time}</p>
                    </div>
                )
            })
            commentJSX.reverse();
            setComments(commentJSX);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const postComment = async () => {
        try {
            const pythonSafeString = newComment.replaceAll("'", "`");
            console.log(pythonSafeString);
            const postBody = { "message": pythonSafeString}
            const response = await fetch(`http://localhost:3000/api/comments?id=${id}`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postBody)
            })

            if (!response.ok) {
                console.log("could not post comment")
                return;
            }
            setNewComment('');
            setRefresh(true);
        } catch (error) {
            console.error('Error posting comment', error);
        }
    };

    useEffect(() => {
            fetchData();
            const intervalId = setInterval(fetchData, FETCH_DATA_INTERVAL);
            return () => clearInterval(intervalId);
        }, []
    );

    useEffect(() => {
        console.log("refreshing")
        fetchData();
    }, [refresh]);

    return (
        <div className={`w-full`}>
            <div className={'grid grid-cols-12 bg-opacity-50 bg-amber-200 rounded-2xl p-5 w-full'}>
                <input className={'col-span-11 rounded-xl p-3 focus:border-0'}
                       placeholder="New Comment"
                       value={newComment}
                       onChange={e => setNewComment(e.currentTarget.value)}
                >
                </input>
                <button className={`col-span-1 bg-tangerine hover:bg-orange-400 ml-3 rounded-md`}
                        onClick={postComment}
                >
                    Send
                </button>
            </div>
            <div className={`max-h-36 overflow-y-scroll mt-10`}>
                {
                    comments && comments.map(e => e)
                }
            </div>
        </div>

    )
}
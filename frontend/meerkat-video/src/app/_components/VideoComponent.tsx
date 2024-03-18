'use client';

import Cookies from 'js-cookie'

export default function Video({ videoId }: { videoId: number }) {
    console.log(Cookies.get('user'));
    return (
        <div className={`flex justify-center`}>
            <video controls>
                <source src={`http://localhost:8000/stream/${videoId}`} type='video/mp4'/>
            </video>
        </div>
    );
}
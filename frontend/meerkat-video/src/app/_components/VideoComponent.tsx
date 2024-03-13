'use client'

export default function Video({ videoId }: { videoId: number }) {
    console.log(videoId);
    return (
        <div>
            <video controls>
                <source src={`http://localhost:8000/stream/${videoId}`} type='video/mp4'/>
            </video>
        </div>
    );
}
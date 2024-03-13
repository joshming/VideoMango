'use client'

export default function Video(videoId: number) {
    console.log(videoId.videoId);
    return (
        <div>
            <video controls>
                <source src={`http://localhost:8000/stream/${videoId.videoId}`} type='video/mp4'/>
            </video>
        </div>
    );
}
export default function Video({ videoId }: { videoId: number }) {
    console.log(videoId);
    return (
        <div className='vid'>
            <video width="1200" height="900" controls>
                <source src={`http://localhost:8000/stream/${videoId}`} type='video/mp4'/>
            </video>
        </div>
    );
}
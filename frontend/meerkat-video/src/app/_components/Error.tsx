export default function Error({ message } : { message : string | null }) {
    return (
      <div className={`outline-2 outline-red-400`}>
          <h3>Error: ${message}</h3>
      </div>
    );
}
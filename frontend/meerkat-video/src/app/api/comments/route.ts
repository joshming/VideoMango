import {NextRequest, NextResponse} from "next/server";

export async function POST(req: NextRequest) {
    const searchParams = req.nextUrl.searchParams
    const id = searchParams.get("id")
    const body = await req.json();
    const user = req.cookies.get("user")?.value;
    const message = body.message;
    if (user === null) {
        return NextResponse.redirect("/login");
    }
    const requestBody = { user, message};
    console.log(requestBody);
    const commentResponse = await fetch (`http://localhost:50000/comment/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    });
    return NextResponse.json({});
}

export async function GET(req: NextRequest) {
    const searchParams = req.nextUrl.searchParams
    const id =  searchParams.get("id");

    const commentResponse = await fetch(`http://localhost:50000/comment/${id}`);
    if (!commentResponse.ok) {
        return NextResponse;
    }
    const comments = await commentResponse.json();

    return NextResponse.json(comments);

}
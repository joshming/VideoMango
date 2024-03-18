import {NextRequest, NextResponse} from "next/server";

export async function POST(req: Request | NextRequest) {
    const body = await req.json();
    const {username, password}: { username: string, password: string } = body;
    const authJson = {username, password}
    const authResponse = await fetch('http://localhost:8000/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(authJson)
    });

    if (!authResponse.ok) {
        return NextResponse.json({
                message: "Could not authenticate"
            },
            {
                status: 401
            })
    }

    const authResponseBody = await authResponse.json();
    const {user, token}: { user: string, token: number } = authResponseBody
    const response = new NextResponse();
    response.cookies.set("token", token.toString());
    response.cookies.set("user", user);
    return response;
}

export async function GET(req: NextRequest) {
    const searchParams = req.nextUrl.searchParams
    const token =  searchParams.get("token");
    const username = searchParams.get("username");

    const authResponse = await fetch(`http://localhost:8000/user/authenticated?token=${token}&username=${username}`);

    if (!authResponse.ok) {
        return NextResponse.json({
                message: "Could not authenticate"
            },
            {
                status: 401
            });
    }

    return NextResponse.json({}, { status: 200 });

}
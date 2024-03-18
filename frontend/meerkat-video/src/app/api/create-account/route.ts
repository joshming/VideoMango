import {NextRequest, NextResponse} from "next/server";

export async function POST(req: Request | NextRequest) {
    const body = await req.json();
    const {username, password}: { username: string, password: string } = body;
    const authJson = {username, password}
    const authResponse = await fetch('http://localhost:8000/user/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(authJson)
    });22

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
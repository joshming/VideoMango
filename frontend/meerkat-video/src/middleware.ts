import type {NextRequest} from 'next/server'
import {NextResponse} from 'next/server'

export function middleware(request: NextRequest) {
    if (!request.cookies.get("token") && request.nextUrl.pathname.startsWith("/watch")) {
        return NextResponse.redirect(new URL('/login', request.url))
    }
    return NextResponse.next();
}
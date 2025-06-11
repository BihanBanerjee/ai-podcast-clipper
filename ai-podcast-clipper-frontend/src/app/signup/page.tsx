"use server";

import { redirect } from "next/navigation";
import { auth } from "~/server/auth";

export default async function Page() {

    const session = await auth();

    if (session) {
        redirect("/dashboard");    
    }

    return (
        <div>
            <h1>Signup</h1>
        </div>
    );
}
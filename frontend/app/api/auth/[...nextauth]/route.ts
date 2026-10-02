import NextAuth from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import { JWT } from "next-auth/jwt"
import { Session } from "next-auth"

interface ExtendedToken extends JWT {
  id?: string
}

interface ExtendedSession extends Session {
  user: {
    id?: string
    name?: string | null
    email?: string | null
    image?: string | null
  }
}

const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null

        // Check against environment variables
        if (
          credentials.email === process.env.ADMIN_EMAIL &&
          credentials.password === process.env.ADMIN_PASSWORD
        ) {
          return {
            id: "1",
            email: credentials.email,
            name: "Admin User"
          }
        }

        return null
      }
    })
  ],
  pages: {
    signIn: "/login"
  },
  session: {
    strategy: "jwt",
    maxAge: 24 * 60 * 60 // 24 hours
  },
  callbacks: {
    async jwt({ token, user }): Promise<ExtendedToken> {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }): Promise<ExtendedSession> {
      const extendedToken = token as ExtendedToken
      return {
        ...session,
        user: {
          ...session.user,
          id: extendedToken.id
        }
      }
    }
  }
})

export const GET = handler
export const POST = handler 
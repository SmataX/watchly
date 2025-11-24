import './globals.css'
export const metadata = {
    title: 'WATCHLY',
    description: 'WATCH MOVIES AND RATE THEM',
}


export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="pl">
            <body>{children}</body>
        </html>
    )
}
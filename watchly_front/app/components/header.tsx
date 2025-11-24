import Image from "next/image";
import Link from 'next/link'
import styles from "./header.module.css";

export default function Header() {
    return (
        <header className={styles.header}>
            <div className={styles.left}>
                <Image src="/images/logo.png" alt="logo" width={40} height={40} />
                <Link href="/" className={styles.logoText}>WATCHLY</Link>
            </div>

            <nav className={styles.nav}>
                <a href="/movies">Movies</a>
                <a href="/reviews">Reviews</a>
                <a href="/friends">Friends</a>
                <a href="/my-ratings">My Ratings</a>
            </nav>

            <Link href="/auth/login" className={styles.signIn}>Sign in</Link>
        </header>
    );
}

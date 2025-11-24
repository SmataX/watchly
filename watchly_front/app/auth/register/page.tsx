// app/auth/register/page.tsx
import Link from 'next/link'
import styles from '../authForm.module.css'
import Image from 'next/image';

export default function RegisterPage() {
    return (
        <div className={styles.authContainer}>
            <Link href="/" className={styles.logoText}>WATCHLY</Link>
            <Link href="/" className={styles.logoText}>WATCHLY</Link>
            <Image
                src="/images/logo.png"
                alt="Logo"
                width={300}
                height={300}
                className={styles.logo} />
            <h1 className={styles.mainTitle}>Sign up</h1>
            <p className={styles.subTitle}>Join to 1000+ users and rate movies</p>
            <form className={styles.authForm}>
             
                <input type="email" placeholder="Email@gmail.com" className={styles.inputButton} />
                <input type="password" placeholder="Password" className={styles.inputButton} />
                <input type="password" placeholder="Password again" className={styles.inputButton} />
                <button type="submit" className={styles.inputButton}>Continue with email</button>
            </form>

            <hr className={styles.hrLine} />

            <button className={styles.inputButton}>Continue with Google</button>

            <div className={styles.footerText}>
                <p>Already have an account? <Link href="/auth/login">Sign in</Link></p>
            </div>
        </div>
    )
}

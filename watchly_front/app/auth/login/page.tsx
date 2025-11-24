// app/auth/login/page.tsx
import Link from 'next/link'
import styles from '../authForm.module.css'
import Image from 'next/image';

export default function LoginPage() {
    return (
       
        
           
        <div className={styles.authContainer}>
            <Link href="/" className={styles.logoText}>WATCHLY</Link>
            <Image
                src="/images/logo.png"
                alt="Logo"
                width={300}
                height={300}
                className={styles.logo}
                />
            <h1 className={styles.mainTitle}>Sign in</h1>
            <p className={styles.subTitle}>Welcome Back</p>

            <form className={styles.authForm}>
                <input type="email" placeholder="Email@gmail.com" className={styles.inputButton} />
                <input type="password" placeholder="Password" className={styles.inputButton} />
                <button type="submit" className={styles.inputButton}>Continue with Email</button>
            </form>

            <hr className={styles.hrLine} />

            <button className={styles.inputButton}>Continue with Google</button>

            <div className={styles.footerText}>
                <p>Dont have an account? <Link href="/auth/register">Sign up</Link></p>
            </div>
           
        </div>
       
        
    )
}

import Link from 'next/link'
import styles from './footer.module.css'
import Image from 'next/image';

export default function Footer() {
    return (

        <footer className={styles.footer}>
            <div className={styles.footerContent}>
                <div className={styles.logoSection}>
                    <h2 className={styles.logoText}>WATCHLY</h2>
                    <p>Your ultimate destination for movie and TV series ratings, reviews, and recommendations.</p>
                    <div className={styles.socialIcons}>
                        <Image src="/images/ig_icon.png" alt="Instagram" width={50} height={50} />
                        <Image src="/images/twitter_icon.png" alt="Twitter" width={50} height={50} />
                    </div>
                </div>

                <div className={styles.linksSection}>
                    <div>
                        <h4>Explore</h4>
                        <ul>
                            <li>Movies</li>
                            <li>TV Series</li>
                            <li>Top Rated</li>
                            <li>New Releases</li>
                            <li>Coming Soon</li>
                        </ul>
                    </div>
                    <div>
                        <h4>Community</h4>
                        <ul>
                            <li>Reviews</li>
                            <li>Ratings</li>
                            <li>Watchlist</li>
                            <li>Friends</li>
                            <li>Top Contributors</li>
                        </ul>
                    </div>
                    <div>
                        <h4>About</h4>
                        <ul>
                            <li>About Us</li>
                            <li>Contact</li>
                            <li>Privacy Policy</li>
                            <li>Terms of Service</li>
                            <li>FAQ</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div className={styles.copy}>2025 WATCHLY. All rights reserved.</div>
        </footer>
    )
}

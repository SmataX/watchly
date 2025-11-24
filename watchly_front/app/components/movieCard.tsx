import styles from './movieCard.module.css';

export default function MovieCard() {
    const movie = {
        title: "Deadpool & Wolverine",
        year: 2024,
        duration: "2h 42m",
        genres: ["Komedia", "Akcja"],
        description: "Dochodzący do siebie Wolverine spotyka pyskatego Deadpoola, z którym łączy siły, by stawić czoła wspólnemu wrogowi.",
        globalRating: 7.8,
        friendsRating: 7.8,
        userRating: 7.8,
        image: "/images/sadcat.jpg"

    };

    return (
        <div className={styles.movieCard}>
            <div className={styles.movieContent}>
                <div className={styles.movieImage}>
                    <img src={movie.image} alt={movie.title} />
                </div>
                <div className={styles.movieDetails}>

                    <div className={styles.movieHeader}>
                        <h1 className={styles.movieTitle}>{movie.title}</h1>
                    </div>

                    <div className={styles.movieInfo}>
                        <span>{movie.year}</span>
                        <span>{movie.duration}</span>
                        <div className={styles.genres}>
                            {movie.genres.map((genre, index) => (
                                <span key={index} className={styles.genre}>{genre}</span>
                            ))}
                        </div>
                    </div>

                    <div className={styles.description}>
                        <p>{movie.description}</p>
                    </div>

                    <div className={styles.ratingsSection}>
                        <div className={styles.ratingsGrid}>
                            <div className={styles.ratingItem}>
                                <div className={styles.ratingLabel}>Global Rating</div>
                                <div className={styles.ratingStars}>
                                    <span>★</span>
                                    <span>{movie.globalRating}</span>
                                </div>
                            </div>

                            <div className={styles.ratingItem}>
                                <div className={styles.ratingLabel}>Friends Average</div>
                                <div className={styles.ratingStars}>
                                    <span>★</span>
                                    <span>{movie.friendsRating}</span>
                                </div>
                            </div>

                            <div className={styles.ratingItem}>
                                <div className={styles.ratingLabel}>Your Rating</div>
                                <div className={styles.ratingStars}>
                                    <span>★</span>
                                    <span>{movie.userRating}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <hr className={styles.divider} />

                    <div className={styles.actions}>
                        <div className={styles.rateRow}>
                            <h3 className={styles.rateTitle}>Rate this movie:</h3>
                            <div className={styles.starRating}>
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        className={styles.starButton}
                                        onClick={() => console.log(`Rated: ${star}`)}
                                    >
                                        ★
                                    </button>
                                ))}
                            </div>
                            <button className={styles.reviewButton}>
                                Write review
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
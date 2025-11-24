'use client';
import styles from './movieList.module.css';
import { useState } from "react";
import { Range } from 'react-range';

export default function MovieList() {
    const RATING_STEP = 0.1;
    const RATING_MIN = 0;
    const RATING_MAX = 5;
    const YEAR_MIN = 1955;
    const YEAR_MAX = 2025;
    const YEAR_STEP = 1;

    const [ratingValues, setRatingValues] = useState([0, 5]);
    const [yearValues, setYearValues] = useState([1955, 2025]);
    const [rating, setRating] = useState(0);

    return (
        <div className={styles.pageContainer}>
            <h1>Discover Movies</h1>
            <h2>Rate, review and share with friends</h2>
            <div className={styles.searchContainer}>
               
                <div className={styles.searchBox}>
                    <input type="text" placeholder="Search movies..." />
                </div>
            </div>
            <hr className={styles.hrLine} />
            <aside className={styles.filterSidebar}>
                {/* categories */}
                <section className={styles.filterSection}>
                <p>Showing 100 movies</p>
                    <h3>Sort by</h3>
                    <ul className={styles.categoryList}>
                        <li><label><input type="radio" name="category" /> Most Popular</label></li>
                        <li><label><input type="radio" name="category" /> Highest Rated</label></li>
                        <li><label><input type="radio" name="category" /> Newest</label></li>
                    </ul>
                </section>

                {/* genres*/}
                <section className="filter-section">
                    <h3>Genres</h3>
                    <ul className={styles.genreList}>
                        <li><label><input type="checkbox" /> Action</label></li>
                        <li><label><input type="checkbox" /> Comedy</label></li>
                        <li><label><input type="checkbox" /> Drama</label></li>
                        <li><label><input type="checkbox" /> Horror</label></li>
                        <li><label><input type="checkbox" /> Romance</label></li>
                        <li><label><input type="checkbox" /> Sci-Fi</label></li>
                        <li><label><input type="checkbox" /> Thriller</label></li>
                        <li><label><input type="checkbox" /> Fantasy</label></li>
                        <li><label><input type="checkbox" /> Animation</label></li>
                        <li><label><input type="checkbox" /> Adventure</label></li>
                    </ul>
                </section>

                {/* rating slider */}
                <section className={styles.filterSection}>
                    <h3>Ratings: {ratingValues[0].toFixed(1)} - {ratingValues[1].toFixed(1)}</h3>
                    <Range
                        step={RATING_STEP}
                        min={RATING_MIN}
                        max={RATING_MAX}
                        values={ratingValues}
                        onChange={(vals) => setRatingValues(vals)}
                        renderTrack={({ props, children }) => (
                            <div
                                {...props}
                                style={{
                                    ...props.style,
                                    height: '6px',
                                    width: '10%',
                                    backgroundColor: '#ccc',
                                    borderRadius: '3px'
                                }}
                            >
                                {children}
                            </div>
                        )}
                        renderThumb={({ props, index }) => {
                            const { key, ...rest } = props;
                            return <div key={key} {...rest} 
                                style={{
                                    ...props.style,
                                    height: '15px',
                                    width: '15px',
                                    backgroundColor: '#007bff',
                                    borderRadius: '50%',
                                    outline: 'none'
                                }}
                            />
                        }}
                    />
                </section>

                {/* year slider*/}
                <section className={styles.filterSection}>
                    <h3>Years: {yearValues[0]} - {yearValues[1]}</h3>
                    <Range
                        step={YEAR_STEP}
                        min={YEAR_MIN}
                        max={YEAR_MAX}
                        values={yearValues}
                        onChange={(vals) => setYearValues(vals)}
                        renderTrack={({ props, children }) => (
                            <div
                                {...props}
                                style={{
                                    ...props.style,
                                    height: '6px',
                                    width: '10%',
                                    backgroundColor: '#ccc',
                                    borderRadius: '3px'
                                }}
                            >
                                {children}
                            </div>
                        )}
                        renderThumb={({ props, index }) => {
                            const { key, ...rest } = props;
                            return <div key={key} {...rest}
                                style={{
                                    ...props.style,
                                    height: '15px',
                                    width: '15px',
                                    backgroundColor: '#007bff',
                                    borderRadius: '50%',
                                    outline: 'none'
                                }}
                            />
                        }}
                    />
                </section>

                {/* reset button */}
                <section className={styles.filterSection}>
                    <button className={styles.resetButton}>Reset Filters</button>
                </section>
            </aside>
            {/* tu pozniej dopisze reszte */}
            <main className={styles.mainContent}>
                <div className={styles.movieGrid}></div>
            </main>
        </div>
    )
}
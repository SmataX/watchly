'use client';
import styles from './movieList.module.css';
import { useState } from "react";
import { Range } from 'react-range';
import MovieCard from '../components/movieCard';
import Footer from '../components/footer'
import Header from '../components/header'


export default function MovieList() {
    const RATING_STEP = 0.1;
    const RATING_MIN = 0;
    const RATING_MAX = 5;
    const YEAR_MIN = 1955;
    const YEAR_MAX = 2025;
    const YEAR_STEP = 1;

    const initialRatingValues = [0, 5];
    const initialYearValues = [1955, 2025];
    const initialSortBy = 'Most Popular';
    const initialGenres = {
        Action: false,
        Comedy: false,
        Drama: false,
        Horror: false,
        Romance: false,
        SciFi: false,
        Thriller: false,
        Fantasy: false,
        Animation: false,
        Adventure: false

    };

    const [ratingValues, setRatingValues] = useState(initialRatingValues);
    const [yearValues, setYearValues] = useState(initialYearValues);
    const [sortBy, setSortBy] = useState(initialSortBy);
    const [genres, setGenres] = useState(initialGenres);
    const [searchQuery, setSearchQuery] = useState('');

    //reset all filters
    const resetFilters = () => {
        setRatingValues(initialRatingValues);
        setYearValues(initialYearValues);
        setSortBy(initialSortBy);
        setGenres(initialGenres);
        setSearchQuery('');
    };

    //changing genres
    const handleGenreChange = (genre: string) => {
        setGenres(prev => ({ ...prev, [genre]: !prev[genre as keyof typeof genres] }));
    };

    //changing radio button sorting
    const handleSortChange = (sortOption: string) => {
        setSortBy(sortOption);
    };

    return (
        <div className={styles.pageContainer}>
        <Header/>

            <h1>Discover Movies</h1>
            <h2>Rate, review and share with friends</h2>
            <div className={styles.searchContainer}>

                <div className={styles.searchBox}>
                    <input type="text" placeholder="Search movies..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
                </div>
            </div>
            <hr className={styles.hrLine} />
            <div className={styles.mainLayout}>

                <aside className={styles.filterSidebar}>
                    {/* categories */}
                    <section className={styles.filterSection}>
                        <p>Showing 100 movies</p>
                        <h3>Sort by</h3>
                        <ul className={styles.categoryList}>
                            <li><label><input type="radio" name="category" checked={sortBy === 'Most Popular'} onChange={() => handleSortChange('Most Popular')} /> Most Popular</label></li>
                            <li><label><input type="radio" name="category" checked={sortBy === 'Highest Rated'} onChange={() => handleSortChange('Highest Rated')} /> Highest Rated</label></li>
                            <li><label><input type="radio" name="category" checked={sortBy === 'Newest'} onChange={() => handleSortChange('Newest')} /> Newest</label></li>
                        </ul>
                    </section>

                    {/* genres*/}
                    <section className="filter-section">
                        <h3>Genres</h3>
                        <ul className={styles.genreList}>
                            {Object.entries(genres).map(([genre, isChecked]) => (
                                <li key={genre}>
                                    <label>
                                        <input type="checkbox" checked={isChecked} onChange={() => handleGenreChange(genre)}
                                        />{genre}
                                    </label>
                                </li>))}
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
                                    {...props} className={styles.sliderTrack}

                                >
                                    {children}
                                </div>
                            )}
                            renderThumb={({ props, index }) => {
                                const { key, ...rest } = props;
                                return <div key={key} {...rest} className={styles.sliderThumb}

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
                                    {...props} className={styles.sliderTrack}

                                >
                                    {children}
                                </div>
                            )}
                            renderThumb={({ props, index }) => {
                                const { key, ...rest } = props;
                                return <div key={key} {...rest} className={styles.sliderThumb}

                                />
                            }}
                        />
                    </section>

                    {/* reset button */}
                    <section className={styles.filterSection}>
                        <button className={styles.resetButton} onClick={resetFilters}>Reset Filters</button>
                    </section>
                </aside>
                
                <main className={styles.mainContent}>

                    <div className={styles.movieGrid}>
                        <MovieCard />
                        <MovieCard />
                        <MovieCard />
                    </div>

                </main>
            </div>
            <Footer/>
        </div>
    )
}
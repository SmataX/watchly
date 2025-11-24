// app/page.tsx
import styles from './home.module.css'
import Header from './components/header'
import Footer from './components/footer'


interface Movie {
  id: number;
  title: string;
  description?: string;
  duration?: number;
  poster_url?: string;
  realse_date?: string;
  created_at?: string;
}

// 2. Create a helper function to fetch data
async function getMovies(): Promise<Movie[]> {
  // We use no-store to ensure we get fresh data every time (good for dev)
  // In production, you might want 'force-cache' or 'revalidate'
  const res = await fetch('http://127.0.0.1:8000/api/movies', { 
    cache: 'no-store' 
  });

  if (!res.ok) {
    // This will activate the closest `error.tsx` Error Boundary
    throw new Error('Failed to fetch movies');
  }

  return res.json();
}

// 3. Make the component async
export default async function Home() {
  // 4. Fetch the data
  const movies = await getMovies();

  return (
    <main className={styles["main-screen"]}>
      <Header />

      <div className={styles.content}>
        <div>
          <h1 className="text-4xl font-bold mb-4">Hello!</h1>
          <p className="text-lg mb-8">
            Bo to nie ma tak że dobrze albo że nie dobrze...
          </p>

          {/* 5. Display the data */}
          <h2 className="text-2xl font-bold mb-4">Available Movies</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {movies.map((movie) => (
              <div key={movie.id} className="border p-4 rounded shadow hover:bg-gray-50">
                {/* Render your movie data here */}
                <h3 className="font-bold">{movie.title}</h3>
                {movie.description && <p className="text-sm text-gray-600">{movie.description}</p>}
              </div>
            ))}
          </div>

          {/* Handle empty state */}
          {movies.length === 0 && <p>No movies found.</p>}
        </div>
      </div>

      <Footer />
    </main>
  );
}
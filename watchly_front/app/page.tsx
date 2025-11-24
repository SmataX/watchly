// app/page.tsx
import styles from './home.module.css'
import Header from './components/header'
import Footer from './components/footer'

export default function Home() {
  return (
    <main className={styles["main-screen"]}>
    <Header />

    <div className={styles.content}>
        <div>
            <h1 className="text-4xl font-bold mb-4">Hello!</h1>
            <p className="text-lg">
                Bo to nie ma tak że dobrze albo że nie dobrze. Gdybym miała
                powiedzieć co cenię w życiu najbardziej, powiedziałabym że ludzi...
            </p>
        </div>
    </div>

    <Footer />
    </main>
  );
}

import Head from 'next/head';

// Styles
import '../public/assets/css/template_main.css';
import '../public/assets/css/custom.css';
import '../public/assets/css/spinner.css';

function MyApp({ Component, pageProps }) {
  return (
    <div>
      <Head>
        <link rel='shortcut icon' href='/favicon.png' />
        <title>#DiputadxDelDía</title>
        <meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no' />
      </Head>
      <Component {...pageProps} />
    </div>
  ) 
}

export default MyApp

import Head from 'next/head';
import { useEffect } from 'react';

// Styles
import '../public/assets/css/template_main.css';
import '../public/assets/css/custom.css';
import '../public/assets/css/spinner.css';

function MyApp({ Component, pageProps }) {

  // Add external scripts
  useEffect(() => {

    function add_script (source) {
      const script = document.createElement('script');
      script.src = source;
      script.async = true;
      document.body.appendChild(script);
      return script;
    }

    const scripts = [
      add_script('assets/js/jquery.min.js'),
      // add_script('assets/js/browser.min.js'),
      // add_script('assets/js/breakpoints.min.js'),
      // add_script('assets/js/util.js'),
      // add_script('assets/js/main.js'),
    ]
    
    return () => scripts.forEach(script => document.body.removeChild(script));
  }, []);

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

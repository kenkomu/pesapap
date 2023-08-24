from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.callbacks import get_openai_callback
from PyPDF2 import PdfReader
import openai
import streamlit as st
import os
import requests

# Page configuration
st.set_page_config(
    page_title="PesaQ",
    page_icon="💸",
    layout="",
)

#set Open-AI key
openai.api_key = "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"

html_code = """
<!DOCTYPE html>
<html>

<head>
<style>
body {
    background-color: transparent;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
#visualizer-container {
    position: relative;
    width: 200px;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
}
#visualizer {
    border: 5px solid orange;
    border-radius: 200px;
    position: absolute;
}
</style>
<title>
Creating an audio visualizer
using HTML CANVAS API
</title>
</head>

<body>
<div id="visualizer-container">
<canvas id="visualizer" width="200px"
    height="200px">
</canvas>
</div>

<script type="text/javascript">
document.addEventListener("DOMContentLoaded", async () => {
    let stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        video: false
    });

    const audioContext = new AudioContext();
    const analyser = audioContext.createAnalyser();
    const mediaStreamSource =
        audioContext.createMediaStreamSource(stream);

    // Connecting the analyzer to the media source
    mediaStreamSource.connect(analyser);
    analyser.fftSize = 256;
    drawVisualizer();

    function drawVisualizer() {
        requestAnimationFrame(drawVisualizer)
        const bufferLength = analyser.frequencyBinCount
        const dataArray = new Uint8Array(bufferLength)

        // Updating the analyzer with the new
        // generated data visualization
        analyser.getByteFrequencyData(dataArray)
        const width = visualizer.width
        const height = visualizer.height
        const barWidth = 3 // Adjust bar width here
        const centerX = width / 2; // Calculate center X
        const centerY = height / 2; // Calculate center Y
        const canvasContext = visualizer.getContext('2d')
        canvasContext.clearRect(0, 0, width, height)
        let x = -barWidth // Start x at -barWidth to remove gap
        dataArray.forEach((item, index, array) => {

            // This formula decides the height of the vertical
            // lines for every item in dataArray
            const y = item / 255 * height * 0.45; // Adjusted for reflection effect
            canvasContext.strokeStyle = `orange`

            // This decides the distances between the
            // vertical lines
            x = x + barWidth
            canvasContext.beginPath();
            canvasContext.lineCap = "round";
            canvasContext.lineWidth = 2;

            // Reflect on the top and bottom as well as left and right
            canvasContext.moveTo(centerX + x, centerY + y);
            canvasContext.lineTo(centerX + x, centerY - y);
            canvasContext.moveTo(centerX - x, centerY + y);
            canvasContext.lineTo(centerX - x, centerY - y);

            canvasContext.stroke();
        })
    }
});
</script>
</body>

</html>
"""


html_code1 = """

<!-- svg icons--><!DOCTYPE html>
<html class="wide wow-animation" lang="en">
  <head>
    <title>Home</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <script src="https://ld-wt73.template-help.com/cdn-cgi/apps/head/3ts2ksMwXvKRuG480KNifJ2_JNM.js"></script><link rel="icon" href="https://ld-wt73.template-help.com/tf/brics_v1/images/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Mulish:500,600,700,900%7COpen+Sans:400,700&amp;display=swap">
    <link rel="stylesheet" href="https://ld-wt73.template-help.com/tf/brics_v1/css/bootstrap.css">
    <link rel="stylesheet" href="https://ld-wt73.template-help.com/tf/brics_v1/css/fonts.css">
    <link rel="stylesheet" href="https://ld-wt73.template-help.com/tf/brics_v1/css/style.css">
  </head>
  <body>
  <div class="padding-left:100px">
    <div class="preloader">
      <div class="preloader-body">
        <div class="cssload-container">
          <div class="cssload-speeding-wheel"></div>
        </div>
      </div>
    </div>
    <div class="page">
      <!-- Header-->
      <header class="section page-header">
        <!--RD Navbar-->
       
      </header>

      <!--Swiper-->
      <section class="section swiper-container swiper-slider swiper-slider-1" data-autoplay="4987" data-loop="true" data-simulate-touch="false" data-direction="horizontal">
        <div class="swiper-wrapper">
          <!-- Slide-->
          <div class="swiper-slide" data-slide-bg="" alt="/index.html" width="800" height="900">
            <div class="swiper-slide-caption">
              <div class="container">
                <div class="row">
                  <div class="col-lg-8 col-md-9 col-sm-10">
                    <h1 data-caption-animate="fadeInUp" data-caption-delay="100" data-caption-duration="900">Get professional<br class="d-none d-lg-block">financial guidance</h1>
                    <p class="lead" data-caption-animate="fadeInUp" data-caption-delay="250" data-caption-duration="900">It’s time to make your money work for you</p><a class="button button-secondary" href="/index.html" data-caption-animate="fadeInUp" data-caption-delay="450" data-caption-duration="900">View our solutions</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Slide-->
          <div class="swiper-slide"  data-slide-bg="" alt="/index.html" width="800" height="900">
            <div class="swiper-slide-caption">
              <div class="container">
                <div class="row">
                  <div class="col-lg-8 col-md-9 col-sm-10">
                    <h1 data-caption-animate="fadeInUp" data-caption-delay="100" data-caption-duration="900">Interpret and<br class="d-none d-lg-block">understand financial documents</h1>
                    <p class="lead" data-caption-animate="fadeInUp" data-caption-delay="250" data-caption-duration="900">Advisory solutions that cover your business needs</p><a class="button button-secondary" href="/index.html" data-caption-animate="fadeInUp" data-caption-delay="450" data-caption-duration="900">View our solutions</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Slide-->
          <div class="swiper-slide" data-slide-bg="" alt="/index.html" width="800" height="900">
            <div class="swiper-slide-caption">
              <div class="container">
                <div class="row">
                  <div class="col-lg-8 col-md-9 col-sm-10">
                    <h1 data-caption-animate="fadeInUp" data-caption-delay="100" data-caption-duration="900">Result-oriented financial strategies</h1>
                    <p class="lead" data-caption-animate="fadeInUp" data-caption-delay="250" data-caption-duration="900">Learn how to achieve the profit your business needs</p><a class="button button-secondary" href="/index.html" data-caption-animate="fadeInUp" data-caption-delay="450" data-caption-duration="900">View our solutions</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--Swiper Pagination-->
        <div class="swiper-pagination"></div>
        <!--Swiper Navigation-->
        <div class="swiper-button-prev">
          <svg width="26" height="20" viewBox="0 0 26 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 2L23 10L15 18" stroke-width="4"></path>
            <path d="M23 10H0" stroke-width="4"></path>
          </svg>
        </div>
        <div class="swiper-button-next">
          <svg width="26" height="20" viewBox="0 0 26 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 2L23 10L15 18" stroke-width="4"></path>
            <path d="M23 10H0" stroke-width="4"></path>
          </svg>
        </div>
      </section>

      <!-- Who we are-->
      <section class="section section-xl bg-default">
        <div class="container">
          <div class="row row-xl-wide row-50 align-items-center align-items-xl-start">
            <div class="col-md-6">
              <div class="figure-box parallax-scene-js">
                <div class="figure figure-1 layer" data-depth="-.2"></div>
                <div class="figure figure-2 layer" data-depth=".3"></div><img class="figure-image layer" src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-04-460x223.jpg" alt="/index.html" width="460" height="223" data-depth=".1"/>
                <div class="figure figure-3 layer" data-depth="-.25"></div>
              </div>
            </div>
            <div class="col-md-6">
              <h6>About us</h6>
              <h2 class="text-primary">Professional approach to financial advisory</h2>
              <p>We aim at supporting companies and individuals in making informed and value-maximizing decisions and pave their way through the challenges of implementation.</p>
              <div class="group-box-counter">
                <!-- Counter-->
                <div class="box-counter box-counter-secondary">
                  <div class="box-counter-main">
                    <div class="counter counter-decimal">1.5</div>
                    <div class="counter-postfix">K</div>
                  </div>
                  <p class="box-counter-title">Satisfied clients</p>
                </div>
                <!-- Counter-->
                <div class="box-counter box-counter-primary">
                  <div class="box-counter-main">
                    <div class="counter">35</div>
                    <div class="counter-postfix">+</div>
                  </div>
                  <p class="box-counter-title">Skilled Professionals</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Our Services-->
      <section class="section section-bg-decor-right">
        <div class="bg-decor-image" style="background-image: url(https://ld-wt73.template-help.com/tf/brics_v1/images/home-05-565x685.jpg)"></div>
        <div class="container">
          <div class="section-md">
            <h6>Our Services</h6>
            <h2>What can we offer you</h2>
            <div class="row mt-xl-84">
              <div class="col-lg-8">
                <div class="row row-xl-58 row-50">
                  <div class="col-sm-6">
                    <!-- Services-->
                    <div class="services services-left">
                      <h5 class="services-header"><span class="services-number">01</span><span class="services-title"><a href="/index.html">Financial planning</a></span></h5>
                      <p class="services-text">We’ll work to analyze your unique financial situation and provide easy-to-understand recommendations for your business.</p>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <!-- Services-->
                    <div class="services services-right">
                      <h5 class="services-header"><span class="services-number">02</span><span class="services-title"><a href="/index.html">Business modelling</a></span></h5>
                      <p class="services-text">Business modelling can help you navigate complex issues and transactions by delivering tailored modelling solutions.</p>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <!-- Services-->
                    <div class="services services-left">
                      <h5 class="services-header"><span class="services-number">03</span><span class="services-title"><a href="/index.html">Investment management</a></span></h5>
                      <p class="services-text">Our investment managers will make all of the investment decisions for you – choosing which investments to buy or sell, etc.</p>
                    </div>
                  </div>
                  <div class="col-sm-6">
                    <!-- Services-->
                    <div class="services services-right">
                      <h5 class="services-header"><span class="services-number">04</span><span class="services-title"><a href="/index.html">Strategic planning</a></span></h5>
                      <p class="services-text">We also offer expertise and strategic planning for large scale project development in international markets.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div><a class="link-arrow" href="/index.html"><span>All our services</span>
              <svg width="17" height="12" viewBox="0 0 17 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 1L15 6L10 11" stroke-width="2"></path>
                <path d="M15 6H0" stroke-width="2"></path>
              </svg></a>
          </div>
        </div>
      </section>

     
          

      <!-- Project-->
      <section class="section isotope-wrap">
        <div class="row row-30 isotope" data-isotope-layout="masonry" data-column-class=".col-1">
          <div class="col-1 isotope-item isotope-sizer"></div>
          <div class="col-sm-6 isotope-item">
            <!-- Project--><a class="project" href="https://ld-wt73.template-help.com/tf/brics_v1/blog.html"><img src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-06-945x1013.jpg" alt="/index.html" width="945" height="1013"/>
              <div class="project-block">
                <h6 class="project-title">Business modelling</h6>
                <h3 class="project-description">Reviewing and developing financial models</h3>
              </div></a>
          </div>
          <div class="col-lg-3 col-sm-6 isotope-item">
            <!-- Project--><a class="project" href="https://ld-wt73.template-help.com/tf/brics_v1/blog.html"><img src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-07-476x511.jpg" alt="/index.html" width="476" height="511"/>
              <div class="project-block">
                <h6 class="project-title">Risk analysis</h6>
                <h3 class="project-description">Action plans to manage strategic risks</h3>
              </div></a>
          </div>
          <div class="col-lg-3 col-sm-6 isotope-item">
            <!-- Project--><a class="project" href="https://ld-wt73.template-help.com/tf/brics_v1/blog.html"><img src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-08-476x511.jpg" alt="/index.html" width="476" height="511"/>
              <div class="project-block">
                <h6 class="project-title">Strategic planning</h6>
                <h3 class="project-description">Helping ensure the future growth of your organization</h3>
              </div></a>
          </div>
          <div class="col-lg-3 col-sm-6 isotope-item">
            <!-- Project--><a class="project" href="https://ld-wt73.template-help.com/tf/brics_v1/blog.html"><img src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-09-476x511.jpg" alt="/index.html" width="476" height="511"/>
              <div class="project-block">
                <h6 class="project-title">Investment management</h6>
                <h3 class="project-description">Make the most of your money and funds with our help</h3>
              </div></a>
          </div>
          <div class="col-lg-3 col-sm-6 isotope-item">
            <!-- Project--><a class="project" href="https://ld-wt73.template-help.com/tf/brics_v1/blog.html"><img src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-10-476x511.jpg" alt="/index.html" width="476" height="511"/>
              <div class="project-block">
                <h6 class="project-title">financial planning</h6>
                <h3 class="project-description">Building a unique financial plan to reach your goals</h3>
              </div></a>
          </div>
        </div>
      </section>

      <!-- Counter-->
            <section class="section section-xxl">
              <div class="container position-relative"><img class="bg-decorative-center" src="https://ld-wt73.template-help.com/tf/brics_v1/images/home-11-1012x521.png" alt="/index.html" width="1012" height="521"/>
                <div class="row row-30">
                  <div class="col-lg-3 col-sm-6">
                    <div class="box-counter-corporate bg-white">
                      <div class="box-counter-icon">
                        <svg width="40" height="49" viewBox="0 0 40 49" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M20 48.5181C22.8438 48.5181 25.4062 48.3618 27.6875 48.0493C29.9688 47.7368 31.9062 47.3774 33.5 46.9712C35.0938 46.5962 36.3281 46.2368 37.2031 45.8931C38.0781 45.5806 38.5469 45.4087 38.6094 45.3774L39.5 45.0024V44.0181C39.5 41.9556 39.1094 40.0181 38.3281 38.2056C37.5469 36.3618 36.4688 34.7681 35.0938 33.4243C33.75 32.0493 32.1562 30.9712 30.3125 30.1899C28.5 29.4087 26.5625 29.0181 24.5 29.0181H15.5C13.4375 29.0181 11.4844 29.4087 9.64062 30.1899C7.82812 30.9712 6.23438 32.0493 4.85938 33.4243C3.51562 34.7681 2.45312 36.3618 1.67188 38.2056C0.890625 40.0181 0.5 41.9556 0.5 44.0181V45.0024L1.39062 45.3774C1.45312 45.4087 1.92188 45.5806 2.79688 45.8931C3.67188 46.2368 4.90625 46.5962 6.5 46.9712C8.09375 47.3774 10.0156 47.7368 12.2656 48.0493C14.5469 48.3618 17.125 48.5181 20 48.5181ZM15.5 32.0181H24.5C26.0625 32.0181 27.5312 32.2993 28.9062 32.8618C30.3125 33.4243 31.5469 34.2056 32.6094 35.2056C33.7031 36.2056 34.5781 37.3774 35.2344 38.7212C35.9219 40.0337 36.3281 41.4556 36.4531 42.9868C35.9219 43.2056 35.1562 43.4556 34.1562 43.7368C33.1562 44.0181 31.9531 44.2993 30.5469 44.5806C29.1719 44.8306 27.5938 45.0493 25.8125 45.2368C24.0312 45.4243 22.0938 45.5181 20 45.5181C17.9062 45.5181 15.9688 45.4243 14.1875 45.2368C12.4062 45.0493 10.8125 44.8306 9.40625 44.5806C8.03125 44.2993 6.84375 44.0181 5.84375 43.7368C4.84375 43.4556 4.07812 43.2056 3.54688 42.9868C3.67188 41.4556 4.0625 40.0337 4.71875 38.7212C5.40625 37.3774 6.28125 36.2056 7.34375 35.2056C8.4375 34.2056 9.67188 33.4243 11.0469 32.8618C12.4531 32.2993 13.9375 32.0181 15.5 32.0181ZM20 26.0181C21.7188 26.0181 23.3125 25.6118 24.7812 24.7993C26.25 23.9868 27.5156 22.9399 28.5781 21.6587C29.6406 20.3774 30.4688 18.9399 31.0625 17.3462C31.6875 15.7212 32 14.1118 32 12.5181C32 10.8618 31.6875 9.31494 31.0625 7.87744C30.4375 6.40869 29.5781 5.12744 28.4844 4.03369C27.3906 2.93994 26.1094 2.08057 24.6406 1.45557C23.2031 0.830566 21.6562 0.518066 20 0.518066C18.3438 0.518066 16.7812 0.830566 15.3125 1.45557C13.875 2.08057 12.6094 2.93994 11.5156 4.03369C10.4219 5.12744 9.5625 6.40869 8.9375 7.87744C8.3125 9.31494 8 10.8618 8 12.5181C8 14.1118 8.29688 15.7212 8.89062 17.3462C9.51562 18.9399 10.3594 20.3774 11.4219 21.6587C12.4844 22.9399 13.75 23.9868 15.2188 24.7993C16.6875 25.6118 18.2812 26.0181 20 26.0181ZM20 3.51807C22.4688 3.51807 24.5781 4.40869 26.3281 6.18994C28.1094 7.93994 29 10.0493 29 12.5181C29 13.7368 28.7656 14.9712 28.2969 16.2212C27.8281 17.4712 27.1875 18.5962 26.375 19.5962C25.5938 20.5962 24.6562 21.4243 23.5625 22.0806C22.4688 22.7056 21.2812 23.0181 20 23.0181C18.7188 23.0181 17.5312 22.7056 16.4375 22.0806C15.3438 21.4243 14.3906 20.5962 13.5781 19.5962C12.7969 18.5962 12.1719 17.4712 11.7031 16.2212C11.2344 14.9712 11 13.7368 11 12.5181C11 10.0493 11.875 7.93994 13.625 6.18994C15.4062 4.40869 17.5312 3.51807 20 3.51807Z"></path>
                        </svg>
                      </div>
                      <!-- Counter-->
                      <div class="box-counter">
                        <div class="box-counter-main">
                          <div class="counter">858</div>
                        </div>
                        <p class="box-counter-title">Satisfied Clients</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-lg-3 col-sm-6">
                    <div class="box-counter-corporate bg-primary">
                      <div class="box-counter-icon">
                        <svg width="47" height="48" viewBox="0 0 47 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M19.5 39.5181C19.875 39.5181 20.2656 39.5181 20.6719 39.5181C21.1094 39.4868 21.5156 39.4399 21.8906 39.3774L22.5 44.1587C22.5625 44.4712 22.6719 44.7368 22.8281 44.9556C23.0156 45.1431 23.25 45.2837 23.5312 45.3774C23.8438 45.4399 24.1406 45.4399 24.4219 45.3774C24.7031 45.3149 24.9062 45.2056 25.0312 45.0493L30 40.1274L36.4688 46.5493C36.5938 46.7056 36.75 46.8149 36.9375 46.8774C37.1562 46.9712 37.3438 47.0181 37.5 47.0181C37.6562 47.0181 37.8281 46.9712 38.0156 46.8774C38.2344 46.8149 38.4062 46.7056 38.5312 46.5493L46.0312 39.0493C46.3438 38.7681 46.5 38.4243 46.5 38.0181C46.5 37.6118 46.3438 37.2681 46.0312 36.9868L39.6094 30.5181L44.5312 25.5493C44.7812 25.3306 44.9375 25.0962 45 24.8462C45.0625 24.5649 45.0156 24.2993 44.8594 24.0493C44.7031 23.8306 44.5312 23.6274 44.3438 23.4399C44.1875 23.2212 43.9531 23.0806 43.6406 23.0181L38.8594 22.4087C38.9219 22.0337 38.9531 21.6587 38.9531 21.2837C38.9844 20.8774 39 20.4556 39 20.0181C39 17.3306 38.4844 14.7993 37.4531 12.4243C36.4531 10.0493 35.0625 7.98682 33.2812 6.23682C31.5312 4.45557 29.4688 3.06494 27.0938 2.06494C24.7188 1.03369 22.1875 0.518066 19.5 0.518066C16.8125 0.518066 14.2812 1.03369 11.9062 2.06494C9.53125 3.06494 7.45312 4.45557 5.67188 6.23682C3.92188 7.98682 2.53125 10.0493 1.5 12.4243C0.5 14.7993 0 17.3306 0 20.0181C0 22.7056 0.5 25.2368 1.5 27.6118C2.53125 29.9868 3.92188 32.0649 5.67188 33.8462C7.45312 35.5962 9.53125 36.9868 11.9062 38.0181C14.2812 39.0181 16.8125 39.5181 19.5 39.5181ZM28.5 21.0493L24 20.4868C24 20.3931 24 20.3149 24 20.2524C24 20.1587 24 20.0806 24 20.0181C24 18.7368 23.5625 17.6743 22.6875 16.8306C21.8438 15.9556 20.7812 15.5181 19.5 15.5181C18.2188 15.5181 17.1406 15.9556 16.2656 16.8306C15.4219 17.6743 15 18.7368 15 20.0181C15 21.2993 15.4219 22.3774 16.2656 23.2524C17.1406 24.0962 18.2188 24.5181 19.5 24.5181C19.5625 24.5181 19.625 24.5181 19.6875 24.5181C19.7812 24.5181 19.875 24.5181 19.9688 24.5181L20.5312 29.0181C20.4062 29.0181 20.25 29.0181 20.0625 29.0181C19.9062 29.0181 19.7188 29.0181 19.5 29.0181C17.0312 29.0181 14.9062 28.1431 13.125 26.3931C11.375 24.6118 10.5 22.4868 10.5 20.0181C10.5 17.5493 11.375 15.4399 13.125 13.6899C14.9062 11.9087 17.0312 11.0181 19.5 11.0181C21.9688 11.0181 24.0781 11.9087 25.8281 13.6899C27.6094 15.4399 28.5 17.5493 28.5 20.0181C28.5 20.1743 28.5 20.3306 28.5 20.4868C28.5 20.6431 28.5 20.8306 28.5 21.0493ZM19.5 21.5181C19.0625 21.5181 18.7031 21.3774 18.4219 21.0962C18.1406 20.8149 18 20.4556 18 20.0181C18 19.5806 18.1406 19.2212 18.4219 18.9399C18.7031 18.6587 19.0625 18.5181 19.5 18.5181C19.9375 18.5181 20.2969 18.6587 20.5781 18.9399C20.8594 19.2212 21 19.5806 21 20.0181C20.7812 20.0181 20.5781 20.0649 20.3906 20.1587C20.2344 20.2212 20.0938 20.3306 19.9688 20.4868C19.8125 20.6118 19.6875 20.7681 19.5938 20.9556C19.5312 21.1118 19.5 21.2993 19.5 21.5181ZM36.4688 29.4868C36.1562 29.7681 36 30.1118 36 30.5181C36 30.9243 36.1562 31.2681 36.4688 31.5493L42.8906 38.0181L37.5 43.4087L31.0312 36.9868C30.9062 36.8306 30.75 36.7212 30.5625 36.6587C30.4062 36.5649 30.2188 36.5181 30 36.5181C29.7812 36.5181 29.5781 36.5649 29.3906 36.6587C29.2344 36.7212 29.0938 36.8306 28.9688 36.9868L25.0312 40.8774L22.6406 23.2993L29.25 24.2368L40.2188 25.7368L36.4688 29.4868ZM19.5 3.51807C21.7812 3.51807 23.9219 3.95557 25.9219 4.83057C27.9219 5.67432 29.6719 6.84619 31.1719 8.34619C32.6719 9.81494 33.8438 11.5649 34.6875 13.5962C35.5625 15.5962 36 17.7368 36 20.0181C36 20.3306 35.9844 20.6587 35.9531 21.0024C35.9531 21.3462 35.9219 21.6743 35.8594 21.9868L31.3594 21.3774C31.3594 21.1587 31.375 20.9399 31.4062 20.7212C31.4688 20.4712 31.5 20.2368 31.5 20.0181C31.5 18.3618 31.1875 16.8149 30.5625 15.3774C29.9375 13.9087 29.0781 12.6274 27.9844 11.5337C26.8906 10.4399 25.6094 9.58057 24.1406 8.95557C22.7031 8.33057 21.1562 8.01807 19.5 8.01807C17.8438 8.01807 16.2812 8.33057 14.8125 8.95557C13.375 9.58057 12.1094 10.4399 11.0156 11.5337C9.92188 12.6274 9.0625 13.9087 8.4375 15.3774C7.8125 16.8149 7.5 18.3618 7.5 20.0181C7.5 21.6743 7.8125 23.2368 8.4375 24.7056C9.0625 26.1431 9.92188 27.4087 11.0156 28.5024C12.1094 29.5962 13.375 30.4556 14.8125 31.0806C16.2812 31.7056 17.8438 32.0181 19.5 32.0181C19.7188 32.0181 19.9375 32.0181 20.1562 32.0181C20.4062 31.9868 20.6406 31.9399 20.8594 31.8774L21.4688 36.3774C21.1562 36.4399 20.8281 36.4868 20.4844 36.5181C20.1406 36.5181 19.8125 36.5181 19.5 36.5181C17.2188 36.5181 15.0781 36.0962 13.0781 35.2524C11.0781 34.3774 9.32812 33.2056 7.82812 31.7368C6.32812 30.2368 5.14062 28.4868 4.26562 26.4868C3.42188 24.4556 3 22.2993 3 20.0181C3 17.7368 3.42188 15.5962 4.26562 13.5962C5.14062 11.5962 6.3125 9.84619 7.78125 8.34619C9.28125 6.84619 11.0312 5.67432 13.0312 4.83057C15.0625 3.95557 17.2188 3.51807 19.5 3.51807Z"></path>
                        </svg>
                      </div>
                      <!-- Counter-->
                      <div class="box-counter">
                        <div class="box-counter-main">
                          <div class="counter">358</div>
                        </div>
                        <p class="box-counter-title">Projects</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-lg-3 col-sm-6">
                    <div class="box-counter-corporate bg-white">
                      <div class="box-counter-icon">
                        <svg width="48" height="46" viewBox="0 0 48 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M46.5 6.01807H33V1.51807C33 1.08057 32.8594 0.721191 32.5781 0.439941C32.2969 0.158691 31.9375 0.0180664 31.5 0.0180664H16.5C16.0625 0.0180664 15.7031 0.158691 15.4219 0.439941C15.1406 0.721191 15 1.08057 15 1.51807V6.01807H1.5C1.0625 6.01807 0.703125 6.15869 0.421875 6.43994C0.140625 6.72119 0 7.08057 0 7.51807V31.5181C0 31.9556 0.140625 32.3149 0.421875 32.5962C0.703125 32.8774 1.0625 33.0181 1.5 33.0181H3V43.5181C3 43.9556 3.14062 44.3149 3.42188 44.5962C3.70312 44.8774 4.0625 45.0181 4.5 45.0181H43.5C43.9375 45.0181 44.2969 44.8774 44.5781 44.5962C44.8594 44.3149 45 43.9556 45 43.5181V33.0181H46.5C46.9375 33.0181 47.2969 32.8774 47.5781 32.5962C47.8594 32.3149 48 31.9556 48 31.5181V7.51807C48 7.08057 47.8594 6.72119 47.5781 6.43994C47.2969 6.15869 46.9375 6.01807 46.5 6.01807ZM18 3.01807H30V6.01807H18V3.01807ZM42 42.0181H6V33.0181H18V34.5181C18 34.9556 18.1406 35.3149 18.4219 35.5962C18.7031 35.8774 19.0625 36.0181 19.5 36.0181H28.5C28.9375 36.0181 29.2969 35.8774 29.5781 35.5962C29.8594 35.3149 30 34.9556 30 34.5181V33.0181H42V42.0181ZM27 33.0181H21V28.5181H27V33.0181ZM45 30.0181H30V27.0181C30 26.5806 29.8594 26.2212 29.5781 25.9399C29.2969 25.6587 28.9375 25.5181 28.5 25.5181H19.5C19.0625 25.5181 18.7031 25.6587 18.4219 25.9399C18.1406 26.2212 18 26.5806 18 27.0181V30.0181H3V9.01807H45V30.0181Z"></path>
                        </svg>
                      </div>
                      <!-- Counter-->
                      <div class="box-counter">
                        <div class="box-counter-main">
                          <div class="counter">145</div>
                        </div>
                        <p class="box-counter-title">Business Partners</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-lg-3 col-sm-6">
                    <div class="box-counter-corporate bg-primary">
                      <div class="box-counter-icon">
                        <svg width="38" height="46" viewBox="0 0 38 46" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M0.390625 39.9868C0.546875 40.2056 0.75 40.3618 1 40.4556C1.28125 40.5181 1.53125 40.5493 1.75 40.5493L7.60938 39.6587L10.6094 44.7681C10.7656 44.9868 10.9531 45.1743 11.1719 45.3306C11.3906 45.4556 11.6562 45.5181 11.9688 45.5181C11.9688 45.5181 12.0156 45.5181 12.1094 45.5181C12.3906 45.5181 12.6406 45.4399 12.8594 45.2837C13.1094 45.1274 13.3125 44.9087 13.4688 44.6274L18.7188 33.5181C18.7812 33.5181 18.8281 33.5181 18.8594 33.5181C18.8906 33.5181 18.9375 33.5181 19 33.5181C19.0625 33.5181 19.1094 33.5181 19.1406 33.5181C19.1719 33.5181 19.2188 33.5181 19.2812 33.5181L24.5312 44.6274C24.6875 44.8462 24.875 45.0493 25.0938 45.2368C25.3438 45.4243 25.6094 45.5181 25.8906 45.5181C25.9219 45.5181 25.9688 45.5181 26.0312 45.5181C26.2812 45.5181 26.5312 45.4556 26.7812 45.3306C27.0312 45.1743 27.2344 44.9868 27.3906 44.7681L30.3906 39.6587L36.25 40.5493C36.5625 40.6431 36.8281 40.6274 37.0469 40.5024C37.2656 40.3774 37.4531 40.2056 37.6094 39.9868C37.7656 39.7368 37.8594 39.4868 37.8906 39.2368C37.9531 38.9556 37.9062 38.7056 37.75 38.4868L32.2188 26.9087C33.25 25.5649 34.0469 24.0649 34.6094 22.4087C35.2031 20.7212 35.5 18.9712 35.5 17.1587C35.5 14.8774 35.0625 12.7368 34.1875 10.7368C33.3438 8.73682 32.1719 6.98682 30.6719 5.48682C29.1719 3.98682 27.4219 2.81494 25.4219 1.97119C23.4219 1.09619 21.2812 0.658691 19 0.658691C16.7188 0.658691 14.5625 1.08057 12.5312 1.92432C10.5312 2.76807 8.78125 3.92432 7.28125 5.39307C5.8125 6.86182 4.64062 8.59619 3.76562 10.5962C2.92188 12.5962 2.5 14.7368 2.5 17.0181C2.5 18.8931 2.78125 20.6587 3.34375 22.3149C3.9375 23.9399 4.75 25.4243 5.78125 26.7681L0.25 38.2993C0.1875 38.6118 0.15625 38.9087 0.15625 39.1899C0.15625 39.4712 0.234375 39.7368 0.390625 39.9868ZM29.6406 36.5181C29.3594 36.4556 29.0781 36.4868 28.7969 36.6118C28.5156 36.7368 28.2969 36.9556 28.1406 37.2681L26.0312 40.8774L22.4688 33.2368C23.875 32.9243 25.2344 32.4399 26.5469 31.7837C27.8594 31.1274 29.0469 30.2993 30.1094 29.2993L33.8594 37.2681L29.6406 36.5181ZM19 3.51807C20.875 3.51807 22.625 3.87744 24.25 4.59619C25.9062 5.28369 27.3438 6.23682 28.5625 7.45557C29.7812 8.67432 30.7344 10.1118 31.4219 11.7681C32.1406 13.3931 32.5 15.1431 32.5 17.0181C32.5 18.5806 32.2344 20.0806 31.7031 21.5181C31.2031 22.9243 30.4688 24.2212 29.5 25.4087C29.4375 25.5024 29.3594 25.5806 29.2656 25.6431C29.2031 25.7056 29.125 25.7837 29.0312 25.8774C27.9062 27.1587 26.5781 28.1899 25.0469 28.9712C23.5156 29.7524 21.8438 30.2212 20.0312 30.3774C20.0312 30.3774 19.9844 30.3774 19.8906 30.3774C19.7344 30.3774 19.5625 30.3774 19.375 30.3774C19.1875 30.3774 19.0156 30.3774 18.8594 30.3774C18.7031 30.3774 18.5469 30.3774 18.3906 30.3774C18.2344 30.3774 18.0938 30.3774 17.9688 30.3774C17.875 30.3774 17.7969 30.3774 17.7344 30.3774C17.6719 30.3774 17.6406 30.3774 17.6406 30.3774C15.9219 30.2212 14.3281 29.7524 12.8594 28.9712C11.3906 28.1899 10.0938 27.1587 8.96875 25.8774C8.875 25.7212 8.78125 25.5806 8.6875 25.4556C8.625 25.2993 8.51562 25.1899 8.35938 25.1274C7.45312 24.0649 6.75 22.8462 6.25 21.4712C5.75 20.0649 5.5 18.5806 5.5 17.0181C5.5 15.1431 5.84375 13.3931 6.53125 11.7681C7.25 10.1118 8.21875 8.67432 9.4375 7.45557C10.6562 6.23682 12.0781 5.28369 13.7031 4.59619C15.3594 3.87744 17.125 3.51807 19 3.51807ZM7.89062 29.1587C8.95312 30.1274 10.1406 30.9556 11.4531 31.6431C12.7656 32.2993 14.125 32.7681 15.5312 33.0493L11.9688 40.7368L9.85938 37.1274C9.70312 36.9087 9.48438 36.7368 9.20312 36.6118C8.92188 36.4556 8.64062 36.3774 8.35938 36.3774L4.28125 36.9868L7.89062 29.1587ZM13.6094 19.4087L12.8594 23.7681C12.7656 24.0806 12.7812 24.3774 12.9062 24.6587C13.0312 24.9087 13.2188 25.1118 13.4688 25.2681C13.6875 25.4243 13.9375 25.5337 14.2188 25.5962C14.5 25.6274 14.7969 25.5649 15.1094 25.4087L19 23.2993L22.8906 25.4087C22.9844 25.5024 23.0938 25.5493 23.2188 25.5493C23.3438 25.5493 23.4844 25.5493 23.6406 25.5493C23.7969 25.5493 23.9531 25.5181 24.1094 25.4556C24.2656 25.3931 24.4062 25.3306 24.5312 25.2681C24.7812 25.1118 24.9688 24.9087 25.0938 24.6587C25.2188 24.3774 25.2344 24.0806 25.1406 23.7681L24.3906 19.4087L27.5312 16.2681C27.7812 16.0493 27.9375 15.7993 28 15.5181C28.0625 15.2368 28.0625 14.9868 28 14.7681C27.9375 14.4556 27.7969 14.2212 27.5781 14.0649C27.3594 13.9087 27.0938 13.7993 26.7812 13.7368L22.4688 13.1274L20.5 9.04932C20.3438 8.83057 20.1562 8.62744 19.9375 8.43994C19.7188 8.25244 19.4531 8.15869 19.1406 8.15869C18.8594 8.15869 18.5938 8.23682 18.3438 8.39307C18.125 8.54932 17.9375 8.76807 17.7812 9.04932L15.8594 12.9868L11.5 13.5493C11.1875 13.6431 10.9219 13.7681 10.7031 13.9243C10.5156 14.0806 10.375 14.3149 10.2812 14.6274C10.2188 14.9087 10.2188 15.1899 10.2812 15.4712C10.3438 15.7524 10.4531 15.9712 10.6094 16.1274L13.6094 19.4087ZM16.8906 15.9868C17.1094 15.9868 17.3281 15.9243 17.5469 15.7993C17.7656 15.6431 17.9531 15.4556 18.1094 15.2368L19 13.2681L19.8906 15.2368C19.9844 15.4556 20.125 15.6431 20.3125 15.7993C20.5 15.9243 20.7188 16.0337 20.9688 16.1274L23.0312 16.4087L21.3906 17.9087C21.2344 18.0649 21.125 18.2837 21.0625 18.5649C21 18.8149 20.9688 19.0493 20.9688 19.2681L21.25 21.3774L19.2812 20.2993C19.2188 20.2368 19.1094 20.2056 18.9531 20.2056C18.8281 20.1743 18.6875 20.1587 18.5312 20.1587C18.4062 20.1587 18.2812 20.1743 18.1562 20.2056C18.0625 20.2056 17.9375 20.2368 17.7812 20.2993L15.8594 21.3774L16.2812 19.2681C16.375 19.0493 16.375 18.8149 16.2812 18.5649C16.2188 18.2837 16.0781 18.0649 15.8594 17.9087L14.3594 16.4087L16.8906 15.9868Z"></path>
                        </svg>
                      </div>
                      <!-- Counter-->
                      <div class="box-counter">
                        <div class="box-counter-main">
                          <div class="counter">28</div>
                        </div>
                        <p class="box-counter-title">Awards</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

      <!-- Testimonials-->
    

    
      <!-- Contacts-->
            <section class="section section-md bg-default">
              <div class="container">
                <div class="row row-50">
                  <div class="col-xl-6 col-md-5">
                    <h6>LET’S GET IN TOUCH</h6>
                    <h2>Contact details</h2>
                    <ul class="contacts-list">
                      <li class="contacts-item"><span class="contacts-title">Phone:</span><span class="contacts-description"><a href="tel:#">(254)123-4567</a></span></li>
                      <li class="contacts-item"><span class="contacts-title">E-mail:</span><span class="contacts-description"><a href="mailto:#">info@demolink.org</a></span></li>
                      <li class="contacts-item"><span class="contacts-title">Address:</span><span class="contacts-description"><a href="index.html#">9826 Nairobi, Kenya</a></span></li>
                      <li class="contacts-item"><span class="contacts-title">Opening hours:</span>
                        <div class="contacts-description-list">
                          <div class="contacts-description-list-item">Monday — Thursday 10:00 - 19:00</div>
                          <div class="contacts-description-list-item">Friday — Sunday 10:00 - 17:00</div>
                        </div>
                      </li>
                    </ul>
                  </div>
                  <div class="col-xl-6 col-md-7">
                    <!--RD Mailform-->
                    <form class="rd-form rd-mailform" data-form-output="form-output-global" data-form-type="contact" method="post" action="https://ld-wt73.template-help.com/tf/brics_v1/bat/rd-mailform.php">
                      <div class="form-wrap">
                        <input class="form-input" id="contact-2-name" type="text" name="name" data-constraints="@Required">
                        <label class="form-label" for="contact-2-name">Name*</label>
                      </div>
                      <div class="form-wrap">
                        <input class="form-input" id="contact-2-email" type="email" name="email" data-constraints="@Required @Email">
                        <label class="form-label" for="contact-2-email">Email*</label>
                      </div>
                      <div class="form-wrap">
                        <label class="form-label" for="contact-2-message">Message</label>
                        <textarea class="form-input" id="contact-2-message" name="message"></textarea>
                      </div>
                      <button class="button button-primary" type="submit">Submit now</button>
                    </form>

                  </div>
                </div>
              </div>
            </section>

      <!-- Footer-->
      <footer class="section footer bg-gray-900">
        <div class="container">
          <div class="footer-main">
            <div class="row row-50 justify-content-between">
              <div class="col-xl-5 col-md-6">
                <div class="row">
                  <div class="col-md-5 col-6">
                 
                  </div>
                  <div class="col-md-6 col-6 mx-auto">
                 
                  </div>
                </div>
              </div>
              <div class="col-xl-6 col-md-6">
                <p>Subscribe to our newsletter to receive weekly tips on the financial topics that interest you the most.</p>
                <form class="rd-form rd-mailform rd-form-inline" data-form-output="form-output-global" data-form-type="subscribe" method="post" action="https://ld-wt73.template-help.com/tf/brics_v1/bat/rd-mailform.php">
                  <div class="form-wrap">
                    <input class="form-input" id="subscribe-form-email-footer" type="email" name="email" data-constraints="@Email @Required">
                    <label class="form-label" for="subscribe-form-email-footer">Enter your email</label>
                  </div>
                  <div class="form-button">
                    <button class="button button-primary" type="submit">Submit now</button>
                  </div>
                </form>
                <div class="soc-list"><a class="soc-link icon fa-facebook-f" href="index.html#"></a><a class="soc-link icon fa-twitter" href="index.html#"></a><a class="soc-link icon fa-instagram" href="index.html#"></a><a class="soc-link icon fa-linkedin-square" href="index.html#"></a></div>
              </div>
            </div>
          </div>
          <div class="footer-bottom">
            <p class="rights"><span>&copy;&nbsp;</span><span class="copyright-year"></span><span>&nbsp;</span><span>ken</span><span>.&nbsp;</span><span>All Rights Reserved&nbsp;|&nbsp;</span><a href="https://ld-wt73.template-help.com/tf/brics_v1/privacy-policy.html">Privacy Policy</a></p>
          </div>
        </div>
      </footer>
    </div>
    <div class="snackbars" id="form-output-global"></div>
    <script src="https://ld-wt73.template-help.com/tf/brics_v1/js/core.min.js"></script>
    <script src="https://ld-wt73.template-help.com/tf/brics_v1/js/script.js"></script>
  </body>
   </div>
</html>
"""


# Sema Translator
def translate(userinput, target_lang, source_lang=None):
    if source_lang:
       url = "https://2015-34-197-127-12.ngrok-free.app/translate_enter/"
       data = {
           "userinput": userinput,
           "source_lang": source_lang,
           "target_lang": target_lang,
        }
       response = requests.post(url, json=data)
       result = response.json()
       print(type(result))
       source_lange = source_lang
       translation = result['translated_text']
       return source_lange, translation
    else:
      url = "https://2015-34-197-127-12.ngrok-free.app/translate_detect/"
      data = {
        "userinput": userinput,
        "target_lang": target_lang,
      }

      response = requests.post(url, json=data)
      result = response.json()
      source_lange = result['source_language']
      translation = result['translated_text']
      return source_lange, translation


# Function to render different pages
def render_page(page):
    if page == "Home":

        
        st.components.v1.html(html_code1,height=5000)
        
    elif page == "PesaChat":
        st.title("PesaChat")
        if "openai_model" not in st.session_state:
          st.session_state["openai_model"] = "gpt-3.5-turbo"

        if "messages" not in st.session_state:
          st.session_state.messages = []

        for message in st.session_state.messages:
          with st.chat_message(message["role"]):
            st.markdown(message["content"])

          st.components.v1.html(html_code1, height=300)
        if prompt := st.chat_input("Ask PesaQ anything ......?"):
          user_lang, Query = translate(prompt, 'eng_Latn')
          st.session_state.messages.append({"role": "user", "content": Query})
          with st.chat_message("user"):
            st.markdown(prompt)

          with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                  {"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            trans_response = translate(full_response, user_lang, 'eng_Latn')[1]
            message_placeholder.markdown(trans_response)
          st.session_state.messages.append({"role": "assistant", "content": full_response})


    elif page == "PesaDoc":
        st.title("PesaDoc 💬")
        st.write("Upload a financial Document and ask questions to get insights")

        #set your Open-AI key
        key="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"
        os.environ["OPENAI_API_KEY"] = key

        # upload file
        pdf = st.file_uploader("", type="pdf")

        # extract the text
        if pdf is not None:
          reader = PdfReader(pdf)
          pdf_text = ''
          for page in (reader.pages):
            text = page.extract_text()
            if text:
              pdf_text += text

          # Define our text splitter
          text_splitter = CharacterTextSplitter(
          separator = "\n",
          chunk_size = 1000, #thousand charctere
          chunk_overlap = 200,
          length_function = len,
          )
          #Apply splitting
          text_chunks = text_splitter.split_text(pdf_text)

          # Use embeddings from OpenAI
          embeddings = OpenAIEmbeddings()
          #Convert text to embeddings
          pdf_embeddings = FAISS.from_texts(text_chunks, embeddings)
          chain = load_qa_chain(OpenAI(), chain_type="stuff")

          #user_question = st.text_input("Get insights into your finances ...")
          # show user input
          if "messages" not in st.session_state:
              st.session_state.messages = []
          
          for message in st.session_state.messages:
              with st.chat_message(message["role"]):
                st.markdown(message["content"])

          if user_question := st.chat_input("Ask PesaDoc anything ......?"):
            with st.chat_message("user"):
                st.markdown(user_question)
            user_langd, Queryd = translate(user_question, 'eng_Latn')
            st.session_state.messages.append({"role": "user", "content": user_question})
            docs = pdf_embeddings.similarity_search(Queryd)
            # print(len(docs))
            response = chain.run(input_documents=docs, question=Queryd)
            output = translate(response, user_langd, 'eng_Latn')[1]
            with st.chat_message("assistant"):
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})

    elif page == "PesaVoice":
        st.components.v1.html(html_code, height=300)

# Main app
def main():

    # Create a sidebar with a dropdown menu for page selection
    menu = ["Home", "PesaChat", "PesaDoc", "PesaVoice"]
    choice = st.sidebar.radio("menu", menu)

    render_page(choice)

if __name__ == "__main__":
    main()
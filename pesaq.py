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
    layout="wide",
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
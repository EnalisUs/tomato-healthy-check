import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import base64

# DB
import sqlite3

conn = sqlite3.connect('dataresfes.db')
c = conn.cursor()

# Functions
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE,image TEXT)')

def add_data(author,title,article,postdate,image):
	c.execute('INSERT INTO blogtable(author,title,article,postdate,image) VALUES (?,?,?,?,?)',(author,title,article,postdate,image))
	conn.commit()

def view_all_notes():
	c.execute('SELECT * FROM blogtable')
	data = c.fetchall()
	return data

def view_first_note():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchone()  # Lấy bảng "blogtable" đầu tiên từ kết quả truy vấn
    return data

def view_all_titles():
	c.execute('SELECT DISTINCT title FROM blogtable')
	data = c.fetchall()
	return data

def get_blog_by_title_keyword(title):
	c.execute('SELECT * FROM blogtable WHERE title LIKE "%{}%"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_title(title):
	c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = c.fetchall()
	return data

def get_blog_by_author(author):
	c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = c.fetchall()
	return data

def delete_data(title):
	c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()

st.set_page_config(layout="wide")

# Load static css
with open("./static/vendor.css", "r") as vendor_css_file:
    vendor_css_code = vendor_css_file.read()
vendor_css_base64 = base64.b64encode(vendor_css_code.encode()).decode()

with open("./static/style.css", "r") as style_css_file:
    style_css_code = style_css_file.read()
style_css_base64 = base64.b64encode(style_css_code.encode()).decode()

# Load js
with open("./static/modernizr.js", "r") as modernizr_js_file:
    modernizr_js_code = modernizr_js_file.read()
modernizr_js_base64 = base64.b64encode(modernizr_js_code.encode()).decode()

with open("./static/jquery-1.11.0.min.js", "r") as jquery_js_file:
    jquery_js_code = jquery_js_file.read()
jquery_js_base64 = base64.b64encode(jquery_js_code.encode()).decode()

with open("./static/plugins.js", "r") as plugins_js_file:
    plugins_js_code = plugins_js_file.read()
plugins_js_base64 = base64.b64encode(plugins_js_code.encode()).decode()

with open("./static/script.js", "r") as script_js_file:
    script_js_code = script_js_file.read()
script_js_base64 = base64.b64encode(script_js_code.encode()).decode()

# Layout Templates

title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""

# View Post
head_news ="""
<div style="padding:10px;border-radius:5px;margin:10px;">
<div class="news-info">
<h3 class="main-title main-title-sizable" ><a style="text-decoration:none; color:#595252;text-align:center;font-family: "SofiaProRegular"" href="https://fruitgrowersnews.com/wp-content/uploads/2020/09/Cornell-Freshly-picked-Cordera-apples_photo-credit-Kevin-Maloney-1-e1689642051696-532x330.jpg" class="" >{}</a></h3>
<div class="news-cate-time" style="color:gray">
<span class="news-push-date">
<span style="font-weight:bold;color: gray">{}</span> - {}</span>
</div>
</div>
</div>
<div>
<img style="padding-left:20px" src="{}">
</div>
"""

body_news ="""
<div style="overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;">
{}
</p>
</div>
"""

card = """
            <div class="row ">
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=California growers react to India’s plan to end tariffs on apples, nuts" class="blog-img"><img src="./app/static/blog1.png" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-07-12</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=California growers react to India’s plan to end tariffs on apples, nuts" class="blog-link">California growers react to India’s plan to end tariffs on apples, nuts</a></h3>
                            <p class="pb-3">India’s agreement to remove retaliatory tariffs on some U.S. farm products is seen as a positive development, but with some trade impacts remaining, farmers and agricultural exporters say it may take time to regain market...
                            </p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=California growers react to India’s plan to end tariffs on apples, nuts"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=Clock House Farm: growing a better tomorrow" class="blog-img"><img src="./app/static/blog221.jpg" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-08-08</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=Clock House Farm: growing a better tomorrow"  class="blog-link">Clock House Farm: Growing A Better Tomorrow</a></h3>
                            <p class="pb-3">Clock House Farm has established a new containerised plant propagation business – Linton Growing – designed to provide the leading Kent-based fruit grower with seamless
                            </p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=Clock House Farm: growing a better tomorrow"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=Maidstone-based soft fruit grower offers eco tours to schools to showcase its pioneering green energy project" class="blog-img"><img src="./app/static/blog222.jpg" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-07-12</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=Maidstone-based soft fruit grower offers eco tours to schools to showcase its pioneering green energy project" class="blog-link">Maidstone-based soft fruit grower offers eco tours to schools to showcase its pioneering green energy project</a></h3>
                            <p class="pb-3">Pupils from Maidstone area schools are being offered guided tours around Clock House Farm’s Yalding base to experience first-hand how a modern farm is helping
                            </p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=Maidstone-based soft fruit grower offers eco tours to schools to showcase its pioneering green energy project"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=Clock House Farm Announces £10M Renewable Energy Project" class="blog-img"><img src="./app/static/blog223.jpg" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-07-12</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=Clock House Farm Announces £10M Renewable Energy Project" class="blog-link">Clock House Farm Announces £10M Renewable Energy Project</a></h3>
                            <p class="pb-3">Green technology employed to grow berries out of season – supporting British-grown ethos, clean energy and less waste Clock House Farm announces the rollout of</p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=Clock House Farm Announces £10M Renewable Energy Project"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=Around the clock sustainability" class="blog-img"><img src="./app/static/blog224.jpg" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-07-12</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=Around the clock sustainability" class="blog-link">Around the clock sustainability</a></h3>
                            <p class="pb-3">Soft-fruit producer and environmental dynamo Oli Pascall tells Fred Searle why his business, Clock House Farm, is leaving no stone unturned in its holistic approach to protecting the planet.
                            </p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=Around the clock sustainability"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="blog-post pt-5 pb-3">
                        <div class="image-zoom">
                            <a href="/Detail?a=Impulse Chickens and Trendy Goats: The Pitfalls of Modern Homesteading" class="blog-img"><img src="https://modernfarmer.com/wp-content/uploads/2023/07/Orpington-rooster-Ernie-with-hen-surrenders-1-768x576.jpeg" alt=""
                                    class="img-fluid"></a>
                        </div>
                        <div class="pt-4">
                            <span class="blog-date text-uppercase">2023-07-12</span>
                        </div>
                        <div class="">
                            <h3 class="py-3"><a href="/Detail?a=Impulse Chickens and Trendy Goats: The Pitfalls of Modern Homesteading" class="blog-link">Impulse Chickens and Trendy Goats: The Pitfalls of Modern Homesteading</a></h3>
                            <p class="pb-3">A few months after backyard chickens became popular in the spring of 2020, farm rescues and sanctuaries saw an influx of surrendered birds</p>
                        </div>
                        <div class="">
                            <a href="/Detail?a=Impulse Chickens and Trendy Goats: The Pitfalls of Modern Homesteading"
                                class="btn btn-outline-primary btn-arrow btn-pill btn-outline-light position-relative">
                                <span class="py-2 px-4">Read more</span>
                                <svg class="arrow-icon" width="18" height="20">
                                    <use xlink:href="#arrow-icon"></use>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
            </div>"""


banner = f"""
    <link rel="stylesheet" href="data:text/css;base64,{vendor_css_base64}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.css" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">
    <link rel="stylesheet" href="data:text/css;base64,{style_css_base64}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Jaldi&family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">
    <section id="hero" class="padding-2xlarge jarallax">
        <div class="container banner-content">
            <div class="  offset-md-0 col-md-8 mt-5 ">
                <p class="display-1 " style="color: #fff;font-family: cursive;">Agriculture news</p>
                <p class="hero-paragraph mt-3" style="color: #fff;font-family: cursive;">News related to agriculture both at home and abroad</p>
            </div>
        </div>
        <img src="./app/static/tomato.jpg" alt="banner" class="jarallax-img" style="filter: blur(2px);">
    </section>"""

footer = f"""
    <section id="blog-block">
        <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 row-cols-xl-5 g-0 ">
            <figure class="blog-block-content image-zoom m-0">
                <a href="/Detail/" class=" position-relative">
                    <img class="blog-block-img img-fluid position-relative" src="./app/static/blog111.png" alt="">
                </a>
            </figure>
            <figure class="blog-block-content image-zoom m-0">
                <a href="/Detail/" class=" position-relative">
                    <img class="blog-block-img img-fluid position-relative" src="./app/static/blog112.png" alt="">
                </a>
            </figure>
            <figure class="blog-block-content image-zoom m-0">
                <a href="/Detail/" class=" position-relative">
                    <img class="blog-block-img img-fluid position-relative" src="./app/static/blog113.png" alt="">
                </a>
            </figure>
            <figure class="blog-block-content image-zoom m-0">
                <a href="/Detail/" class=" position-relative">
                    <img class="blog-block-img img-fluid position-relative" src="./app/static/blog114.png" alt="">
                </a>
            </figure>
            <figure class="blog-block-content image-zoom m-0">
                <a href="/Detail/" class=" position-relative">
                    <img class="blog-block-img img-fluid position-relative" src="./app/static/blog115.png" alt="">
                </a>
            </figure>
        </div>
    </section>
    <section id="cta">
        <div class="container py-5">
            <div class="row align-items-center g-5 my-2 py-5">
                <div class="col-12 col-md-10 col-lg-6 offset-lg-1">
                    <h2 class=" display-3 my-3">Never miss a Post Subscribe Now</h2>
                    <p class="cta-paragraph mb-5">I am so happy, my dear friend, so absorbed in the exquisite sense of
                        mere tranquil existence, that I neglect my talents. I should be incapable of drawing</p>
                </div>
                <div class="col-12 col-md-10 col-lg-4 ms-lg-4">
                    <form>
                        <div class="form-group">
                            <input type="text" name="name" placeholder="Name" class="form-control p-3 " required="">
                            <input type="text" name="email" placeholder="Email" class="form-control p-3  my-2"
                                required="">
                            <div class="d-grid gap-2">
                                <button class="btn btn-primary text-uppercase p-3" type="button">Subscribe</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
    <section id="footer" class="position-relative">
        <div class="pattern-overlay pattern-left position-absolute">
            <img src="./app/static/leaf-img-pattern-left.png" alt="pattern">
        </div>
        <div class="pattern-overlay pattern-right position-absolute">
            <img src="./app/static/leaf-img-pattern-right.png" alt="pattern">
        </div>
        <div class="container footer-container py-5 ">
            <footer class="py-2 pt-4">
                <div class="d-flex flex-column align-items-center mt-3">
                    <p class="mb-0">© 2023 All rights reserved.</p>
                </div>
            </footer>
        </div>
    </section>
    <script type="text/javascript" src="data:text/javascript;base64,{jquery_js_base64}"></script>
    <script type="text/javascript" src="data:text/javascript;base64,{plugins_js_base64}"></script>
    <script type="text/javascript" src="data:text/javascript;base64,{script_js_base64}"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/iconify-icon@1.0.7/dist/iconify-icon.min.js"></script>
"""





def main():

	menu = ["Home","View Posts"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		# result = view_all_notes() 	

		# for i in result:
		# 	b_author = i[0]
		# 	b_title = i[1]
		# 	b_article = str(i[2])[0:200]
		# 	b_post_date = i[3]
		# 	b_image = i[4]
		st.markdown(banner,unsafe_allow_html=True)
		search_term = st.text_input('Enter your interested keyword')
		
		if st.button("Search"):
			article_result = get_blog_by_title_keyword(search_term)

			for i in article_result:
				b_author = i[0]
				b_title = i[1]
				b_article = i[2]
				b_post_date = i[3]
				b_image = i[4]
				st.markdown(head_news.format(b_title,b_author,b_post_date,b_image),unsafe_allow_html=True)
				st.markdown(body_news.format(b_article),unsafe_allow_html=True)	
		else:
			st.markdown(card,unsafe_allow_html=True)
			st.markdown(footer,unsafe_allow_html=True)
			
        # st.markdown(card,unsafe_allow_html=True)	
        # st.markdown(footer,unsafe_allow_html=True)
		# st.markdown(home_html.format(b_image,b_post_date,b_title,b_article),unsafe_allow_html=True)
        # st.markdown(card_article.format(b_title,b_author,b_article,b_post_date,b_image),unsafe_allow_html=True)

		
	# image, date, title, arti	    


	elif choice == "View Posts":
		st.subheader("View Articles")
		all_titles = [i[0] for i in view_all_titles()]
		postlist = st.sidebar.selectbox("View Posts",all_titles)
		post_result = get_blog_by_title(postlist)
		for i in post_result:
			b_author = i[0]
			b_title = i[1]
			b_article = i[2]
			b_post_date = i[3]
			b_image = i[4]
			st.markdown(head_news.format(b_title,b_author,b_post_date,b_image),unsafe_allow_html=True)
			st.markdown(body_news.format(b_article),unsafe_allow_html=True)




	elif choice == "Add Posts":
		st.subheader("Add Articles")
		create_table()
		blog_author = st.text_input("Enter Author Name",max_chars=50)
		blog_title = st.text_input("Enter Post Title")
		blog_article = st.text_area("Post Article Here",height=200)
		blog_post_date = st.date_input("Date")
		blog_image = st.text_input("Enter image link")
		if st.button("Add"):
			add_data(blog_author,blog_title,blog_article,blog_post_date, blog_image)
			st.success("Post:{} saved".format(blog_title))	




	elif choice == "Search":
		st.subheader("Search Articles")
		search_term = st.text_input('Enter Search Term')
		search_choice = st.radio("Field to Search By",("title","author"))
		
		if st.button("Search"):

			if search_choice == "title":
				article_result = get_blog_by_title_keyword(search_term)
			elif search_choice == "author":
				article_result = get_blog_by_author(search_term)


			for i in article_result:
				b_author = i[0]
				b_title = i[1]
				b_article = i[2]
				b_post_date = i[3]
				b_image = i[4]
				st.markdown(head_news.format(b_title,b_author,b_post_date,b_image),unsafe_allow_html=True)
				st.markdown(body_news.format(b_article),unsafe_allow_html=True)




	elif choice == "Manage Blog":
		st.subheader("Manage Articles")

		result = view_all_notes()
		clean_db = pd.DataFrame(result,columns=["Author","Title","Articles","Post Date","Image"])
		st.dataframe(clean_db)

		unique_titles = [i[0] for i in view_all_titles()]
		delete_blog_by_title = st.selectbox("Unique Title",unique_titles)
		new_df = clean_db
		if st.button("Delete"):
			delete_data(delete_blog_by_title)
			st.warning("Deleted: '{}'".format(delete_blog_by_title))


	# 	if st.checkbox("Metrics"):
			
	# 		new_df['Length'] = new_df['Articles'].str.len()
	# 		st.dataframe(new_df)


	# 		st.subheader("Author Stats")
	# 		new_df["Author"].value_counts().plot(kind='bar')
	# 		st.pyplot()

	# 		st.subheader("Author Stats")
	# 		new_df['Author'].value_counts().plot.pie(autopct="%1.1f%%")
	# 		st.pyplot()

	# 	if st.checkbox("Word Cloud"):
	# 		st.subheader("Generate Word Cloud")
	# 		# text = new_df['Articles'].iloc[0]
	# 		text = ','.join(new_df['Articles'])
	# 		wordcloud = WordCloud().generate(text)
	# 		plt.imshow(wordcloud,interpolation='bilinear')
	# 		plt.axis("off")
	# 		st.pyplot()

	# 	if st.checkbox("BarH Plot"):
	# 		st.subheader("Length of Articles")
	# 		new_df = clean_db
	# 		new_df['Length'] = new_df['Articles'].str.len()
	# 		barh_plot = new_df.plot.barh(x='Author',y='Length',figsize=(20,10))
	# 		st.pyplot()


if __name__ == '__main__':
	main()
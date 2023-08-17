import streamlit as st
import streamlit.components.v1 as components
import base64
import sqlite3

st.set_page_config(layout="wide")


conn = sqlite3.connect('dataresfes.db')
c = conn.cursor()

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



head_message_temp ="""
<div style="padding:10px;border-radius:5px;margin:10px;">

<div class="news-info">
                                    <h3 class="main-title main-title-sizable" ><a style="text-decoration:none; color:#595252;text-align:center;font-family: "SofiaProRegular"" href="https://fruitgrowersnews.com/wp-content/uploads/2020/09/Cornell-Freshly-picked-Cordera-apples_photo-credit-Kevin-Maloney-1-e1689642051696-532x330.jpg" class="" >California growers react to India’s plan to end tariffs on apples, nuts</a></h3>
                                    <div class="news-cate-time" style="color:gray">
                                        <span class="news-push-date">
                                        <span style="font-weight:bold;color: gray">Ching Lee</span> - 2023-07-12                                 </span>
                                    </div>
                                </div>


</div>
"""
image="""
<div>
    <img style="padding-left:20px" src="https://fruitgrowersnews.com/wp-content/uploads/2020/09/Cornell-Freshly-picked-Cordera-apples_photo-credit-Kevin-Maloney-1-e1689642051696-532x330.jpg">
</div>
"""

full_message_temp ="""
<div style="overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;">
India’s agreement to remove retaliatory tariffs on some U.S. farm products is seen as a positive development, but with some trade impacts remaining, farmers and agricultural exporters say it may take time to regain market share.

Under a deal reached June 21 between the U.S. and Indian governments, the South Asian nation will drop additional duties on American almonds, walnuts, apples, chickpeas and lentils. The duties, to be lifted within 90 days of the agreement, were imposed in retaliation for U.S. tariffs on steel and aluminum imports implemented by the Trump administration in 2018.

California Farm Bureau CFBTariffs on American goods increase the price that importers pay, making U.S. products less competitive. The higher value of the dollar also has hurt U.S. exporters. With grower prices for almonds and walnuts on a downward trend in recent years, India’s repeal of the retaliatory tariffs would provide U.S. exporters improved access to a key market, industry people say.

India remains a top export destination for California agricultural products, including tree nuts, cotton, dairy and processing tomatoes, with total export value reaching nearly $1 billion in 2020, according to the California Department of Food and Agriculture.

“It has shown amazing growth over the last 10 years, and now it’s way in front in terms of being our No. 1 export market,” said Richard Waycott, president and CEO of the Almond Board of California.

Valued at $854 million in 2021, almond exports to India represent 46% of all U.S. agricultural exports, according to the almond board.

With the recent agreement, tariffs will drop from 42 Indian rupees per kilogram to 35 rupees per kilo for in-shell almonds. A rupee is worth $0.0121, meaning that the in-shell almond tariff will drop by 10 cents. For almond kernels, tariffs will drop from 120 rupees per kilo to 100 rupees per kilo.

Due to the higher existing tariff rates on kernels, India imports almost 100% in-shell almonds, Waycott noted.

California Farm Bureau CFB Ag Alert logoHe said though he’s pleased tariffs have come down for U.S. almonds, California farmers and shippers of the nut remain “at quite a disadvantage” to Australia, which signed a bilateral trade agreement with India that cuts tariff rates in half.

Instead of paying the current 35 rupees per kilo, for example, importers pay 17 and a half rupees per kilo for Australian in-shell almonds. With the tariff reduction, Waycott said Australian almond shipments to India have increased.

The Golden State remains the world’s largest almond producer, accounting for more than 80% of global supplies. That means there aren’t too many places India could turn to for almonds, and India will “continue to be a customer of ours regardless of the tariffs,” Waycott said.

California almond exports to India rose despite the retaliatory tariffs, the almond board reported. But with the Australia-India trade deal, it has allowed almonds from Down Under to enter India with a larger market share than they’ve had, Waycott added.

“That is a very discouraging phenomenon,” he said, considering “a lot of California grower dollars” have gone into building the India market during the past 30 years. What the industry needs, Waycott said, is “something much larger,” such as a U.S.-India bilateral agreement, “to put us on an even footing with Australia.”

But he noted the U.S. government currently “is not interested in forging those.”

Don Barton, president of GoldRiver Orchards, a walnut grower, processor and shipper in San Joaquin County, described elimination of the 20% retaliatory tariff on U.S. in-shell walnuts as “a huge lift” for those in the walnut business. He said it will now allow California growers and exporters of the nut to “compete on a level playing field with Chile,” the world’s third-largest walnut producer and one of the state’s biggest competitors in export markets.

Chileans, Barton noted, have “taken full advantage of the lower tariff they were operating under” since 2018, when India imposed the retaliatory tariffs on U.S. walnuts. Indian buyers like Chilean walnuts, he said, and Chile will “have a leg up on California for the foreseeable future, even with the removal of the retaliatory tariff.”

Robert Verloop, CEO of the California Walnut Commission, said many factors besides trade tariffs during the past few years “created a very challenging global marketplace” that affected sales and distribution of California walnuts to India, resulting in lower grower returns.

Those impacts include pandemic-induced supply chain and transportation disruptions, overstocked supply pipelines, global economic downturn, inflationary pressures, high dollar values, and persistent drought and heat that damaged the 2022-23 crop.

He said he expects the tariff reduction “will allow for more equitable access to the India market.” Plus, with the current California walnut crop looking “outstanding” and the economy growing globally and in India, he said “we hope to see demand and moderate shipment volumes to start improving immediately.”

For GoldRiver Orchards, Barton said lifting the tariff will certainly help in the long term. More immediately, impact of the change will be “minimal,” he said, because “our trade contacts in India will have to be rebuilt after a five-year hiatus due to the tariff trade barrier.”

“This will take some time,” Barton said, adding that although he anticipates doing some business in India during the 2023-24 crop year, “it will likely take another two to three years beyond this one to fully rebuild our presence in India.”

Even though California ships virtually no apples to India, withdrawal of the 20% retaliatory tariff on U.S. apples was a welcome change, said Todd Sanders, executive director of the California Apple Commission.

Nearly one-third of the nation’s apple crop goes to foreign markets, with exports valued at about $1 billion, according to the U.S. Apple Association. Prior to 2018, India was the No. 2 export market for U.S. apples—and quickly growing.

When India retaliated by bringing total tariffs on U.S. apples to 70%, sales fell to nearly zero, costing U.S. growers half a billion dollars in sales, the association said.

Most U.S. apple exports are shipped from the Pacific Northwest, and when the retaliatory tariffs “essentially vaporized” the India market, Sanders said it created a “trickle-down effect on every other state.”

“Those apples that would have normally gone to India now needed a new home, which led to the displacement of our apples,” he said.

The tariff change means more accessible markets, Sanders said, which will take pressure off the domestic market and international markets closer to the U.S., namely Mexico and Canada.

He said the commission and other apple organizations around the U.S. have been working with Congress and the Biden administration to reduce tariffs, and “we applaud the result.”

</p>
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

def main():
    # menu = ["Home","View Posts"]
    # choice = st.sidebar.selectbox("Menu",menu)
    
    # if choice == "Home":
    #     st.markdown(head_message_temp.format(),unsafe_allow_html=True)
    #     st.image('https://fruitgrowersnews.com/wp-content/uploads/2020/09/Cornell-Freshly-picked-Cordera-apples_photo-credit-Kevin-Maloney-1-e1689642051696-532x330.jpg')
    #     st.markdown(full_message_temp.format(),unsafe_allow_html=True)   
    # parameter a = '1'
    # elif choice == "View Posts":
        # [a = "1"]
        getParams = st.experimental_get_query_params()
        all_titles = [i[0] for i in view_all_titles()]
        # postlist = st.sidebar.selectbox("View Posts",all_titles)
        post_result = get_blog_by_title(getParams["a"][0])
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            # b_title = getParams["a"][0]
            b_article = i[2]
            b_post_date = i[3]
            b_image = i[4]
            st.markdown(head_news.format(b_title,b_author,b_post_date,b_image),unsafe_allow_html=True)
            st.markdown(body_news.format(b_article),unsafe_allow_html=True)

if __name__ == '__main__':
	main()






from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

# products_link = []
def the_search():
    try:
        searchString = request.form['content'].replace(" ", "+")
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        uClient = uReq(flipkart_url)
        flipkartPage = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkartPage, "html.parser")
        sub_box = flipkart_html.find_all("div", {"class": "_13oc-S"})

        return sub_box

    except Exception as e:
        print('The Exception message is: ', e)
        return 'something is wrong in the search'


# def product_page():
#     sub_box = the_search()
#     p = []
#
#     for box in sub_box:
#         try:
#             p_Link = "https://www.flipkart.com" + box.div.div.a['href']
#             productLink = bs(p_Link, "html.parser")
#         except:
#             productLink = "NO LINK"
#         p.append(productLink)
#
#     return p


@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/searches',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def top_searches():
    if request.method == 'POST':
        try:
            sub_box = the_search()
            searches = []
            for box in sub_box:
                try:
                    # b_thumb.encode(encoding='utf-8')
                    thumb = box.find("div",{"class":"CXW8mj"})
                    b_thumb = thumb.img["src"]
                except:
                    b_thumb = "NO IMAGE"

                try:
                    # productName.encode(encoding='utf-8')
                    p_name = box.find("div",{"class":"CXW8mj"})
                    productName = p_name.img["alt"]

                except:
                    productName = "NO NAME"

                try:
                    # overallRating.encode(encoding='utf-8')
                    p_rating = box.find("div",{"class":"_3LWZlK"})
                    overallRating = p_rating.text
                except:
                    overallRating = "NO RATING"

                try:
                    # productPrice.encode(encoding='utf-8')
                    p_price = box.find("div",{"class":"_30jeq3"})
                    productPrice = p_price.text
                except:
                    productPrice = "NO PRICE"

                try:
                    p_Link = "https://www.flipkart.com" + box.div.div.a['href']
                    productLink = bs(p_Link, "html.parser")
                except:
                    productLink = "NO LINK"


                mydict = {"thumb": b_thumb, "Name": productName, "Rating": overallRating, "Price": productPrice, "Link": productLink}
                searches.append(mydict)

            return render_template('top_searches.html', searches=searches[0:(len(searches) - 1)])

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')



@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            try:
                pd = request.form['content']
                # print("product link.....", pd)
            except Exception as e:
                print('The Exception message is: ', e)
                return 'Unable to fetch product link.'

            reviews = []

            prodRes = requests.get(pd)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            try:
                rLink = prod_html.find_all("div", {"class": "col JOpGWq"})
                reviewLink = "https://www.flipkart.com" + rLink[0].a["href"]
                b_reviewLink = bs(reviewLink, "html.parser")
                rLinkRes = requests.get(b_reviewLink)
                rLinkRes.encoding = 'utf-8'
                rlink_html = bs(rLinkRes.text, "html.parser")
            except:
                print("No Reviws")


            commentboxes = rlink_html.find_all('div', {'class': "col _2wzgFH K0kLPL"})

            for i in commentboxes:
                try:
                    # productName.encode(encoding='utf-8')
                    name = i.find('p', {'class': '_2sc7ZR _2V5EHH'}).text

                except:
                    name = "NO NAME"

                try:
                    # overallRating.encode(encoding='utf-8')
                    rating = i.div.div.text

                except:
                    rating = "NO RATING"

                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = i.find('p', {'class': '_2-N8zT'}).text

                except:
                    commentHead = "NO commentHead"

                try:
                    # comtag.encode(encoding='utf-8')
                    comtag = i.find_all('div', {'class': ''})

                except:
                    comtag = "NO comment Tag"

                try:
                    # custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text

                except:
                    custComment = "NO comment"

                mydict = {"Name": name, "Rating": rating, "CommentHead": commentHead, "Comment": custComment}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)







    # if request.method == 'POST':
    #     try:
    #         pd = product_page()
    #         p = pd[0]
    #     except Exception as e:
    #         print('The Exception message is: ', e)
    #         return 'Unable to fetch product link.'
    #
    #     reviews = []
    #     try:
    #         prodRes = requests.get(p)
    #         prodRes.encoding = 'utf-8'
    #         prod_html = bs(prodRes.text, "html.parser")
    #     except Exception as e:
    #         print('The Exception message is: ', e)
    #         return 'Unable to fetch product page.'
    #
    #     try:
    #         rLink = prod_html.find_all("div", {"class": "col JOpGWq"})
    #         reviewLink = "https://www.flipkart.com" + rLink[0].a["href"]
    #         b_reviewLink = bs(reviewLink, "html.parser")
    #         rLinkRes = requests.get(b_reviewLink)
    #         rLinkRes.encoding = 'utf-8'
    #         rlink_html = bs(rLinkRes.text, "html.parser")
    #     except Exception as e:
    #         print('The Exception message is: ', e)
    #         return 'Unable to fetch review page.'
    #
    #     commentboxes = rlink_html.find_all('div', {'class': "col _2wzgFH K0kLPL"})
    #
    #     for i in commentboxes:
    #         try:
    #             # productName.encode(encoding='utf-8')
    #             name = i.find('p', {'class': '_2sc7ZR _2V5EHH'}).text
    #             # productName = p_name.img["alt"]
    #
    #         except:
    #             name = "NO NAME"
    #
    #         try:
    #             # overallRating.encode(encoding='utf-8')
    #             rating = i.div.div.text
    #             # overallRating = p_rating.text
    #         except:
    #             rating = "NO RATING"
    #
    #         try:
    #             # commentHead.encode(encoding='utf-8')
    #             commentHead = i.find('p', {'class': '_2-N8zT'}).text
    #             # productPrice = p_price.text
    #         except:
    #             commentHead = "NO commentHead"
    #
    #         try:
    #             # comtag.encode(encoding='utf-8')
    #             comtag = i.find_all('div', {'class': ''})
    #             # productPrice = p_price.text
    #         except:
    #             comtag = "NO commentHead"
    #
    #         try:
    #             # custComment.encode(encoding='utf-8')
    #             custComment = comtag[0].div.text
    #             # productPrice = p_price.text
    #         except:
    #             custComment = "NO commentHead"
    #
    #         mydict = {"Name": name, "Rating": rating, "CommentHead": commentHead, "Comment": custComment}
    #         reviews.append(mydict)
    #     return render_template('results.html', reviews=reviews[0:(len(reviews) - 1)])
    #     # except Exception as e:
    #     #     print('The Exception message is: ', e)
    #     #     return 'something is wrong'
    #     # # return render_template('results.html')
    # else:
    #     return render_template('index.html')
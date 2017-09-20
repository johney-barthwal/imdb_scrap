from bs4 import BeautifulSoup
import requests
from tkinter import *
import urllib.request
from PIL import Image
import webbrowser
import re
from datetime import datetime
from tkinter import messagebox
l=[]
fn=''
ln=''

def showmsg():
    messagebox.showerror("We Got Problem","Enter a Valid Name (Spelling Check) OR\nCheck Internet Connectivity")

def onClick():
    a = e1.get()
    b = e2.get()
    a=a.rstrip(' ')
    b=b.rstrip(' ')
    fn=a.title()
    ln=b.title()
    try:

        try:
            url = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + fn + "+" + ln + "=all")
            s = BeautifulSoup(url.text)
            for i in s.find_all('a', text=fn + " " + ln):
                l.append(i.get('href'))
            link = l[0]
        except:
            url = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + fn + "&s=all")
            s = BeautifulSoup(url.text)
            for i in s.find_all('a', text=fn):
                l.append(i.get('href'))
            link = l[0]

        url = requests.get("http://www.imdb.com" + link)
        s = BeautifulSoup(url.text)
        for i in s.find_all('div', id="details-height"):
            temp = (i.text).split('\n')
            height = temp[2]
            height = height.rstrip(' ')

        for i in s.find_all('div', id="dyk-star-sign"):
            temp = (i.text).split('\n')
            sign = temp[2]

        for i in s.find_all('img', id="name-poster"):
            imgsrc = i.get('src')
        urllib.request.urlretrieve(imgsrc, "F:/wall/xxx.jpg")
        im = Image.open('F:/wall/xxx.jpg')
        im.save('F:/wall/star.png')

        n = link.split('/')
        nm = n[2]
        moviep = []
        movier = []
        moviev = []
        url = requests.get("http://www.imdb.com/filmosearch?explore=title_type&role=" + nm + "&ref_=filmo_ref_typ&sort=num_votes,desc&mode=detail&page=1&title_type=movie")
        s = BeautifulSoup(url.text)
        for i in s.find_all('img'):
            moviev.append(i.get('alt'))

        url = requests.get("http://www.imdb.com/filmosearch?explore=title_type&role=" + nm + "&ref_=filmo_ref_typ&sort=user_rating,desc&mode=detail&page=1&title_type=movie")
        s = BeautifulSoup(url.text)
        for i in s.find_all('img'):
            movier.append(i.get('alt'))

        url = requests.get("http://www.imdb.com/filmosearch?explore=title_type&role=" + nm + "&ref_=filmo_ref_typ&sort=moviemeter,asc&mode=detail&page=1&title_type=movie")
        s = BeautifulSoup(url.text)
        for i in s.find_all('img'):
            moviep.append(i.get('alt'))

        url = requests.get("http://www.imdb.com/name/" + nm + "/bio?ref_=nm_dyk_aka")
        s = BeautifulSoup(url.text)
        for i in s.find_all('table', id="overviewTable"):
            dob = (i.text).split('\n')
            birth = dob[4] + " " + dob[6] + " " + dob[8]



        #new function for new window movies details
        def download_movies():
            mv_links = []
            url = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q="+moviev[2]+"&s=all")
            s = BeautifulSoup(url.text)
            for i in s.find_all('a', text=moviev[2]):
                mv_links.append(i.get('href'))
            link = mv_links[0]
            url = requests.get("http://www.imdb.com"+ link)
            s = BeautifulSoup(url.text)

            for i in s.find_all('a', itemprop='trailer'):
                mv_trailer = i.get('href')

            try:
                imgsrc=''
                for i in s.find_all('img', title=moviev[2]+" Poster"):
                    imgsrc = i.get('src')
                urllib.request.urlretrieve(imgsrc,"F:/wall/moviev.jpg")
                img = Image.open("F:/wall/moviev.jpg")
                img = img.resize((100, 150), Image.ANTIALIAS)
                img.save("F:/wall/moviev.png")
            except:
                img = Image.open("F:/wall/notavailable.png")
                img.save("F:/wall/moviev.png")

            mv_genres = ''
            for i in s.find_all('div', itemprop='genre'):
                mv_genres = mv_genres + i.text
            mv_genres = mv_genres.replace('\n', '')

            # kill all script and style elements
            for script in s(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = s.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            try:
                mv_director = re.findall(r'(?s)(?<=Director:).*?(?=Writer)', text)
                mv_director = mv_director[0].replace('\n', '')
            except:
                try:
                    mv_director = re.findall(r'(?s)(?<=Directors:).*?(?=Writer)', text)
                    mv_director = mv_director[0].replace('\n', '')
                except:
                    mv_director = re.findall(r'(?s)(?<=Directors:).*?(?=Stars)', text)
                    mv_director = mv_director[0].replace('\n', '')

            mv_country = re.findall(r'(?s)(?<=Country:).*?(?=Language)', text)
            mv_country = mv_country[0].replace('\n', '')

            mv_language = re.findall(r'(?s)(?<=Language:).*?(?=Release Date)', text)
            mv_language = mv_language[0].replace('\n', '')

            mv_release_date = re.findall(r'(?s)(?<=Release Date:).*?(?=See)', text)
            mv_release_date = mv_release_date[0].replace('\n', '')

            try:
                mv_gross = re.findall(r'(?s)(?<=Gross:).*?(?=See)', text)
                mv_gross = mv_gross[0].replace('\n', '')
            except:
                mv_gross = "Not Available"

            try:
                mv_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Sound Mix)', text)
                mv_runtime = mv_runtime[0].replace('\n', '')
            except:
                try:
                    mv_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Color)', text)
                    mv_runtime = mv_runtime[0].replace('\n', '')
                except:
                    mv_runtime = "Not Available"
            # *********************************************************************
            mr_links = []
            url = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q="+movier[2]+"&s=all")
            s = BeautifulSoup(url.text)
            for i in s.find_all('a', text=movier[2]):
                mr_links.append(i.get('href'))
            link = mr_links[0]
            url = requests.get("http://www.imdb.com"+ link)
            s = BeautifulSoup(url.text)

            for i in s.find_all('a', itemprop='trailer'):
                mr_trailer = i.get('href')

            try:
                imgsrc=''
                for i in s.find_all('img', title=movier[2]+" Poster"):
                    imgsrc = i.get('src')
                urllib.request.urlretrieve(imgsrc,"F:/wall/movier.jpg")
                img = Image.open("F:/wall/movier.jpg")
                img = img.resize((100, 150), Image.ANTIALIAS)
                img.save("F:/wall/movier.png")
            except:
                img = Image.open("F:/wall/notavailable.png")
                img.save("F:/wall/movier.png")

            mr_genres = ''
            for i in s.find_all('div', itemprop='genre'):
                mr_genres = mr_genres + i.text
            mr_genres = mr_genres.replace('\n', '')

            # kill all script and style elements
            for script in s(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = s.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            try:
                mr_director = re.findall(r'(?s)(?<=Director:).*?(?=Writer)', text)
                mr_director = mr_director[0].replace('\n', '')
            except:
                try:
                    mr_director = re.findall(r'(?s)(?<=Directors:).*?(?=Writer)', text)
                    mr_director = mr_director[0].replace('\n', '')
                except:
                    mr_director = re.findall(r'(?s)(?<=Directors:).*?(?=Stars)', text)
                    mr_director = mr_director[0].replace('\n', '')

            mr_country = re.findall(r'(?s)(?<=Country:).*?(?=Language)', text)
            mr_country = mr_country[0].replace('\n', '')

            mr_language = re.findall(r'(?s)(?<=Language:).*?(?=Release Date)', text)
            mr_language = mr_language[0].replace('\n', '')

            mr_release_date = re.findall(r'(?s)(?<=Release Date:).*?(?=See)', text)
            mr_release_date = mr_release_date[0].replace('\n', '')

            try:
                mr_gross = re.findall(r'(?s)(?<=Gross:).*?(?=See)', text)
                mr_gross = mr_gross[0].replace('\n', '')
            except:
                mr_gross = "Not Available"

            try:
                mr_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Sound Mix)', text)
                mr_runtime = mr_runtime[0].replace('\n', '')
            except:
                try:
                    mr_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Color)', text)
                    mr_runtime = mr_runtime[0].replace('\n', '')
                except:
                    mr_runtime = "Not Available"
            #*********************************************************************
            mp_links = []
            url = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q="+moviep[2]+"&s=all")
            s = BeautifulSoup(url.text)
            for i in s.find_all('a', text=moviep[2]):
                mp_links.append(i.get('href'))
            link = mp_links[0]
            url = requests.get("http://www.imdb.com"+ link)
            s = BeautifulSoup(url.text)

            for i in s.find_all('a', itemprop='trailer'):
                mp_trailer = i.get('href')

            try:
                imgsrc = ''
                for i in s.find_all('img', title=moviep[2]+" Poster"):
                    imgsrc = i.get('src')
                urllib.request.urlretrieve(imgsrc, "F:/wall/moviep.jpg")
                img = Image.open("F:/wall/moviep.jpg")
                img = img.resize((100, 150), Image.ANTIALIAS)
                img.save("F:/wall/moviep.png")
            except:
                img = Image.open("F:/wall/notavailable.png")
                img.save("F:/wall/moviep.png")

            mp_genres = ''
            for i in s.find_all('div', itemprop='genre'):
                mp_genres = mp_genres + i.text
            mp_genres = mp_genres.replace('\n', '')

            # kill all script and style elements
            for script in s(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = s.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            try:
                mp_director = re.findall(r'(?s)(?<=Director:).*?(?=Writer)', text)
                mp_director = mp_director[0].replace('\n', '')
            except:
                try:
                    mp_director = re.findall(r'(?s)(?<=Directors:).*?(?=Writer)', text)
                    mp_director = mp_director[0].replace('\n', '')
                except:
                    mp_director = re.findall(r'(?s)(?<=Directors:).*?(?=Stars)', text)
                    mp_director = mp_director[0].replace('\n', '')

            mp_country = re.findall(r'(?s)(?<=Country:).*?(?=Language)', text)
            mp_country = mp_country[0].replace('\n', '')

            mp_language = re.findall(r'(?s)(?<=Language:).*?(?=Release Date)', text)
            mp_language = mp_language[0].replace('\n', '')

            mp_release_date = re.findall(r'(?s)(?<=Release Date:).*?(?=See)', text)
            mp_release_date = mp_release_date[0].replace('\n', '')

            try:
                mp_gross = re.findall(r'(?s)(?<=Gross:).*?(?=See)', text)
                mp_gross = mp_gross[0].replace('\n', '')
            except:
                mp_gross = "Not Available"

            try:
                mp_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Sound Mix)', text)
                mp_runtime = mp_runtime[0].replace('\n', '')
            except:
                try:
                    mp_runtime = re.findall(r'(?s)(?<=Runtime:).*?(?=Color)', text)
                    mp_runtime = mp_runtime[0].replace('\n', '')
                except:
                    mp_runtime = "Not Available"

            def mv(event):
                webbrowser.open_new(r"https://proxyspotting.in/s/?q="+moviev[2]+"&video=on&page=0&orderby=99")

            def mv1(event):
                webbrowser.open_new(r"http://www.imdb.com"+ mv_trailer)

            def mr(event):
                webbrowser.open_new(r"https://proxyspotting.in/s/?q="+movier[2]+"&video=on&page=0&orderby=99")

            def mr1(event):
                webbrowser.open_new(r"http://www.imdb.com"+ mr_trailer)

            def mp(event):
                webbrowser.open_new(r"https://proxyspotting.in/s/?q="+moviep[2]+"&video=on&page=0&orderby=99")

            def mp1(event):
                webbrowser.open_new(r"http://www.imdb.com"+ mp_trailer)


            window2.destroy()
            window3 = Tk()
            window3.title("Star Movies Info")
            window3.configure(bg="black")
            img_moviev = PhotoImage(file="F:/wall/moviev.png")
            x = Label(image=img_moviev)
            x.grid(row=0, column=0)
            x.place(x=50, y=50)
            m_vl=Label(window3,text=moviev[2]+" (vote)",fg="yellow",bg="black",font=("Helvetica, 20"))
            m_vl.place(x=175,y=12)
            m_vt = Text(height=9, width=100)
            m_vt.place(x=175, y=50)
            m_vt.insert(INSERT, mv_genres
                        +"\n  Director        : "+ mv_director
                        +"\n  Country         : "+ mv_country
                        +"\n  Language        : "+ mv_language
                        +"\n  Release Date    : "+ mv_release_date
                        +"\n  Gross           : "+ mv_gross
                        +"\n  Duration        : "+ mv_runtime)
            m_vb = Button(window3, text="Download Movie", fg="blue")
            m_vb.place(x=275, y=170)
            m_vb.bind("<Button-1>", mv)
            m_vb1 = Button(window3, text="Watch Trailor", fg="blue")
            m_vb1.place(x=180, y=170)
            m_vb1.bind("<Button-1>", mv1)

            img_movier = PhotoImage(file="F:/wall/movier.png")
            x = Label(image=img_movier)
            x.grid(row=0, column=0)
            x.place(x=50, y=250)
            m_rl = Label(window3, text=movier[2]+" (Imdb Rating)", fg="yellow", bg="black", font=("Helvetica, 20"))
            m_rl.place(x=175, y=212)
            m_rt = Text(height=9, width=100)
            m_rt.place(x=175, y=250)
            m_rt.insert(INSERT, mr_genres
                        + "\n  Director        : " + mr_director
                        + "\n  Country         : " + mr_country
                        + "\n  Language        : " + mr_language
                        + "\n  Release Date    : " + mr_release_date
                        + "\n  Gross           : " + mr_gross
                        + "\n  Duration        : " + mr_runtime)
            m_rb = Button(window3, text="Download Movie", fg="blue")
            m_rb.place(x=275, y=370)
            m_rb.bind("<Button-1>", mr)
            m_rb1 = Button(window3, text="Watch Trailor", fg="blue")
            m_rb1.place(x=180, y=370)
            m_rb1.bind("<Button-1>", mr1)

            img_moviep = PhotoImage(file="F:/wall/moviep.png")
            x = Label(image=img_moviep)
            x.grid(row=0, column=0)
            x.place(x=50, y=450)
            m_pl = Label(window3, text=moviep[2]+" (popularity)", fg="yellow", bg="black", font=("Helvetica, 20"))
            m_pl.place(x=175, y=412)
            m_pt = Text(height=9, width=100)
            m_pt.place(x=175, y=450)
            m_pt.insert(INSERT, mp_genres
                        + "\n  Director        : " + mp_director
                        + "\n  Country         : " + mp_country
                        + "\n  Language        : " + mp_language
                        + "\n  Release Date    : " + mp_release_date
                        + "\n  Gross           : " + mp_gross
                        + "\n  Duration        : " + mp_runtime)
            m_pb = Button(window3, text="Download Movie", fg="blue")
            m_pb.place(x=275, y=570)
            m_pb.bind("<Button-1>", mp)
            m_pb1 = Button(window3, text="Watch Trailor", fg="blue")
            m_pb1.place(x=180, y=570)
            m_pb1.bind("<Button-1>", mp1)

            window3.geometry("1000x625")
            window3.mainloop()

        window.destroy()
        window2 = Tk()
        window2.geometry("1100x357")
        window2.title("Star Info")
        bg_image = PhotoImage(file="F:/wall/star.png")
        x = Label(image=bg_image)
        x.grid(row=0, column=0)
        x.place(x=20, y=20)
        t = Text(height=22, width=3, bg="blue")
        t.place(x=0, y=0)
        t2 = Text(height=2, width=135, bg="blue")
        t2.place(x=28, y=0)
        t3 = Text(height=2, width=135, bg="blue")
        t3.place(x=28, y=320)
        t4 = Text(height=22, width=3, bg="blue")
        t4.place(x=235, y=0)
        t5 = Text(height=3, width=106)
        t5.place(x=263, y=36)
        t5.tag_configure("bold", font="Helvetica 30 bold")
        t5.insert(INSERT, fn + " " + ln, "bold")
        lstar = str(len(fn) + len(ln) + 1)
        t5.tag_add("one", "1.0", "1." + lstar + "")
        t5.tag_config("one", background="yellow", foreground="blue")
        t6 = Text(height=14, width=106)
        t6.place(x=263, y=94)
        t6.insert(INSERT, "\nBirth Date & Place    : " + birth
                  + "\n" + "Height                : " + height
                  + "\n" + "Star Sign             : " + sign
                  + "\n" + "Best Film(vote)       : " + moviev[2]
                  + "\n" + "Best Film(rating)     : " + movier[2]
                  + "\n" + "Best Film(popularity) : " + moviep[2])
        ldob = str(len(birth) + 24)
        t6.tag_add("two", "2.24", "2." + ldob + "")
        t6.tag_config("two", foreground="#8b4513")
        lh = str(len(height) + 24)
        t6.tag_add("three", "3.24", "3." + lh + "")
        t6.tag_config("three", foreground="#8b4513")
        ls = str(len(sign) + 24)
        t6.tag_add("four", "4.24", "4." + ls + "")
        t6.tag_config("four", foreground="#8b4513")
        lv = str(len(moviev[2]) + 24)
        t6.tag_add("five", "5.24", "5." + lv + "")
        t6.tag_config("five", foreground="#8b4513")
        lr = str(len(movier[2]) + 24)
        t6.tag_add("six", "6.24", "6." + lr + "")
        t6.tag_config("six", foreground="#8b4513")
        lp = str(len(moviep[2]) + 24)
        t6.tag_add("seven", "7.24", "7." + lp + "")
        t6.tag_config("seven", foreground="#8b4513")
        b = Button(text="Above Movies Details", foreground="blue",command=download_movies)
        b.place(x=450, y=240)

        window2.mainloop()

    except:
        showmsg()


window = Tk()
window.title("Get Star Info")
bg_image = PhotoImage(file="F:/wall/movies.png")
x = Label(image=bg_image)
x.grid(row=0, column=0)
l1 = Label(window, text="First Name")
l1.place(x=10,y=10)
l2 = Label(window, text="Last Name")
l2.place(x=10,y=40)
e1=Entry(window)
e1.place(x=100,y=10)
e2=Entry(window)
e2.place(x=100,y=40)
b=Button(window,text="Get Info",command=onClick)
b.place(x=250,y=25)


window.geometry("500x281")
window.mainloop()

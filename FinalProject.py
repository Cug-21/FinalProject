import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import pydeck as pdk
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import numpy as np
import plotly_express as px
import sqlite3
import altair as alt


# volcanos = pd.read_csv("volcanoes.csv", encoding='latin-1')


def main():

    st.set_page_config(
     page_title="ViewCano")

    userconn = sqlite3.connect('users.db')
    postconn = sqlite3.connect('posts.db')
    profileconn = sqlite3.connect('profiles.db')

    c = userconn.cursor()
    d = postconn.cursor()
    pdata = profileconn.cursor()

    def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

    def create_posttable():
        d.execute('CREATE TABLE IF NOT EXISTS poststable(username TEXT,post TEXT)')

    def create_profiletable():
        pdata.execute('CREATE TABLE IF NOT EXISTS profilestable(username TEXT,profile TEXT)')

    def add_userdata(username, password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
        userconn.commit()

    def add_posts(username, post):
        d.execute('INSERT INTO poststable(username,post) VALUES (?,?)', (username, post))
        postconn.commit()

    def add_profile(username, profile):
        pdata.execute('INSERT INTO profilestable(username,profile) VALUES (?,?)', (username, profile))
        profileconn.commit()

    def login_user(username, password):
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
        data = c.fetchall()
        return data

    def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

    def view_all_posts():
        d.execute('SELECT * FROM poststable')
        data = d.fetchall()
        return data

    def view_all_profiles():
        pdata.execute('SELECT * FROM profilestable')
        data = pdata.fetchall()
        return data

    def delete_posts(posts):
        d.execute('DELETE FROM poststable WHERE post="{}"'.format(posts))
        postconn.commit()


    st.markdown("<h1 style='text-align: center; color: black;'>Welcome To ViewCano Where You Can View Volcanoes</h1>",
                unsafe_allow_html=True)
    menu = ['Volcanos', 'Login', 'SignUp']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == "Volcanos":
        st.markdown("<h2 style='text-align: center; color: red;'>Analytics!</h2>",
                    unsafe_allow_html=True)
        st.write("***")
        task = st.selectbox("Charts",
                            ["Map of Volcano's", "Density Map", "Bar Chart Data", "Pie Chart Data", "Interactive"])
        volcanos = pd.read_csv("volcanoes.csv", encoding='latin-1')
        volcanos.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)
        if task == "Map of Volcano's":
            st.markdown("<h2 style='text-align: center; color: red;'>The Map of All Volcanoes!</h2>",
                        unsafe_allow_html=True)
            st.write("***")
            v = volcanos[["latitude", "longitude"]]
            st.map(v)
            st.subheader("Caption:")
            st.write("This first map displays all of the volcanoes in the data set, showing there is a defined pattern these volcanoes follow.")
            st.write("***")

            title = st.markdown("<h2 style='text-align: center; color: red;'>Select the Region You Wish to View!</h2>",
                                unsafe_allow_html=True)
            unireg = volcanos["Subregion"].unique()
            t = st.multiselect("Unique Region Selected", unireg, default='Italy')
            subregQ = volcanos.query("Subregion == @t")
            fig = go.Figure()
            fig.add_trace(go.Scattergeo(
                lat=subregQ['latitude'],
                lon=subregQ['longitude'],
                marker={
                    "color": ['blue'],
                    "line": {
                        "width": 1
                    },
                    "size": 10
                },
                mode="markers+text",
                name="",
                text=subregQ["Volcano Name"],
                textfont={
                    "color": ["MidnightBlue"]
                },
                textposition=["top right"]
            ))
            fig.update_layout(
                geo=dict(
                    lataxis=dict(range=[-90, 90]),
                    lonaxis=dict(range=[-180, 180]),
                    scope="world"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Caption")
            st.write("This map displays all of the volcanoes in the Subregion selected, it also displays the names above the points and you can hover on the points to see the name. ")


        elif task == "Density Map":
            st.markdown("<h2 style='text-align: center; color: red;'>Density Map</h2>",
                        unsafe_allow_html=True)
            st.write("***")

            fig = go.Figure(go.Densitymapbox(lat=volcanos['latitude'], lon=volcanos['longitude'], radius=5))
            fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("<h3 style='text-align: left; color: red;'>Caption:</h3>",
                        unsafe_allow_html=True)
            st.markdown("<body style='text-align: left; color: red;'>This displays all of the volcanoes in the data set and where they are located. This map included a cool feature where you can view the density of the volcanoes in an area based on the color the more yellow an area is the more dense the volcanoes are.</body>",
                        unsafe_allow_html=True)


        elif task == "Bar Chart Data":
            st.write("***")
            st.markdown(
                "<h2 style='text-align: center; color: black;'>This Bar Chart Shows the Number of Credible Evidence Observed Per Region</h2>",
                unsafe_allow_html=True)
            st.write("***")
            uniele = volcanos["Activity Evidence"].unique()
            select_color = st.sidebar.radio("Please Select the Color of the First Bar Chart",
                                            ["Red", "Yellow", "Blue", "Orange"])
            uniele.sort()
            eleslslider = st.select_slider("Select the Observation Evidence", uniele)
            eleq = volcanos[volcanos["Activity Evidence"] == eleslslider]
            elebar = eleq["Region"].value_counts()
            fig, ax = plt.subplots()
            data = eleq['Activity Evidence'].value_counts()
            ax.bar(x=elebar.keys(), height=elebar.values, color=select_color)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.subheader("Caption:")
            st.write("This bar chart shows the frequency of volcanoes that have the given observation evidence, the x axis sorts by region.")
            st.write("***")
            st.markdown(
                "<h2 style='text-align: center; color: red;'>This Bar Chart Shows the Total Elevation for Volcanoes in a given Region</h2>",
                unsafe_allow_html=True)

            uniregion = volcanos["Region"].unique()
            regslider = st.select_slider("Select the Desired Region", uniregion)
            regq = volcanos[volcanos["Region"] == regslider]
            regbar = regq["Country"].value_counts()

            chart = (
                alt.Chart(regq)
                .mark_bar()
                .encode(
                    alt.X("Country:O"),
                    alt.Y("Elevation (m)"),
                    alt.Color("Country:O"),
                    alt.Tooltip(["Country", "Elevation (m)"]),
                )
                .interactive()
            )
            st.altair_chart(chart)
            st.markdown("<h3 style='text-align: left; color: red;'>Caption:</h3>",
                unsafe_allow_html=True)
            st.markdown("<body style='text-align: left; color: red;'>This bar chart shows the total elevation of the volcanoes for a given region, it then filters further to show the countries in said region</body>",
                unsafe_allow_html=True)

        elif task == "Pie Chart Data":
            st.markdown("<h2 style='text-align: center; color: red;'>Volcano Data Displayed Via Pie Chart!</h2>",
                        unsafe_allow_html=True)
            st.write("***")
            uniOrigin = volcanos["Country"].unique()
            selecter = st.multiselect('Select the Country Volcano Origin', uniOrigin, default='Turkey')

            fig = plt.figure(figsize=(12, 8))
            ax1 = fig.add_axes([0.1, 0.6, 0.3, 0.3])
            ax2 = fig.add_axes([0.6, 0.6, 0.3, 0.3])
            ax3 = fig.add_axes([0.1, 0.1, 0.3, 0.3])
            ax4 = fig.add_axes([0.6, 0.1, 0.3, 0.3])
            newdd = volcanos.query("Country == @selecter")
            x = newdd["Country"].value_counts()
            ax1.pie(x, labels=x.keys(), autopct="%.1f%%")
            dataax2 = newdd[newdd["Tectonic Setting"] == "Rift zone / Continental crust (>25 km)"]
            y = dataax2["Country"].value_counts()
            ax2.pie(y, labels=y.keys(), autopct="%.1f%%")

            dataax3 = newdd[newdd["Activity Evidence"] == "Eruption Observed"]
            v = dataax3["Country"].value_counts()
            ax3.pie(v, labels=v.keys(), autopct="%.1f%%")

            dataax4 = newdd[newdd["Dominant Rock Type"] == "Andesite / Basaltic Andesite"]
            z = dataax4["Country"].value_counts()
            ax4.pie(z, labels=z.keys(), autopct="%.1f%%")

            ax1.set_title("All Volcanoes Selected")
            ax2.set_title("Only Volcanoes With Rift zone >25 Km")
            ax3.set_title("All Volcanoes with Activity Observed")
            ax4.set_title("Volcanoes With Dominate Rock Type of Andesite")

            st.pyplot(fig)
            st.markdown("<h3 style='text-align: left; color: red;'>Caption:</h3>",
                        unsafe_allow_html=True)
            st.markdown("<body style='text-align: left; color: red;'>These four pie charts all display different data. The top left chart shows the percentage of volcanoes in each selected country. The top right displays percentage of all volcanoes in countries selected that have a rift zone above 25KM. The bottom left shows all volcanoes from selected countries that had the activity observed. And the bottom right chart shows percentage of all volcanoes in countries selected that have a dominate rocky type of Andesite. </body>",
                        unsafe_allow_html=True)
            st.markdown('***')
            st.subheader("Countries with the most Volcanoes")
            fig1 = plt.figure()
            axx = fig.add_axes([0.1, 0.6, 0.3, 0.3])
            p1 = volcanos["Country"].value_counts()

            fig1, axx = plt.subplots(figsize=(20, 20))
            axx.pie(p1, labels=p1.keys(), autopct='%1.1f%%',
                    shadow=True, startangle=90)
            legend = axx.legend(loc="upper left", bbox_to_anchor=(1, 1))

            # pixels to scroll per mousewheel event
            d = {"down": 30, "up": -30}

            def func(evt):
                if legend.contains(evt):
                    bbox = legend.get_bbox_to_anchor()
                    bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                    tr = legend.axes.transAxes.inverted()

                    legend.set_bbox_to_anchor(bbox.transformed(tr))
                    fig1.canvas.draw_idle()

            fig1.canvas.mpl_connect("scroll_event", func)
            fig1.savefig("chart", bbox_inches='tight')
            st.pyplot(fig1)
            st.subheader("Caption:")
            st.write("This chart shows all of the volcanoes in the data set by their origin Country.")
            st.write("***")

        elif task == "Interactive":
            st.markdown("<h2 style='text-align: center; color: black;'>Bar Chart Of Selected Data by Dominate Rock Type</h2>",
                        unsafe_allow_html=True)
            unicountry = volcanos["Country"].unique()
            multi = st.sidebar.multiselect('Select the Country Volcano Origin', unicountry)

            data = volcanos.query("Country == @multi")
            tr = data["Dominant Rock Type"].value_counts()

            fig = px.histogram(data, x="Country",
                                   color="Dominant Rock Type", barmode='group', histfunc="count",
                                   height=400)
            st.plotly_chart(fig)
            st.subheader("Caption:")
            st.write("This bar chart displays groups of countries selected on the X axis grouped by the dominate rock type. This rock type is then counted and compared.")
            st.write("***")
            st.markdown("<h2 style='text-align: center; color: red;'>Map of Selected Volcanoes</h2>",
                        unsafe_allow_html=True)
            v = data
            st.map(v)
            st.markdown("<h3 style='text-align: left; color: red;'>Caption:</h3>",
                        unsafe_allow_html=True)
            st.markdown("<body style='text-align: left; color: red;'>This Map Displays the locations of volcanoes in the Country Selected.</body>",
                        unsafe_allow_html=True)



    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')

        if st.sidebar.checkbox("Login"):
            create_usertable()
            result = login_user(username, password)
            if result:
                st.success("Login In as {}".format(username))
                task = st.selectbox("Task", ["Chat Room", "Add A Profile", "Profiles"])

                if task == "Chat Room":
                    st.subheader("Welcome to the Explore Page")

                    post = st.text_input("Enter Your Post")
                    if st.button("Enter Your post"):
                        create_posttable()
                        add_posts(username, post)
                        st.success("You have entered a post")
                    st.subheader("Posts")
                    post_results = view_all_posts()
                    clean_post = pd.DataFrame(post_results, columns=["Username", "Post"])
                    clean_post.set_index("Username", inplace=True)
                    for i in clean_post.iterrows():
                        name = i[0]
                        post = str(i[1]).split(":")[0].replace('Post', '"').replace('Name', '"')
                        st.write(str(post)+' posted by: '+str(name))

                    postss = [j[1] for j in view_all_posts()]
                    delete_poost_by_title = st.selectbox("Post Title", postss)

                    if st.button("Delete Post"):
                        delete_posts(delete_poost_by_title)
                        st.warning(f"{delete_poost_by_title} deleted")




                elif task == "Add A Profile":
                    st.subheader("Let Other Volcano Enthusiast Know about Yourself!")
                    profile = st.text_input("Tell Us About Yourself!")
                    if st.button("Confirm Your Profile"):
                        create_profiletable()
                        add_profile(username, profile)
                        st.success("You have Entered a Profile")


                elif task == "Profiles":
                    st.subheader("User Profiles")
                    profile_results = view_all_profiles()
                    st.write(profile_results)



            else:
                st.write("Incorrect Username")

    elif choice == "SignUp":
        st.subheader("Create New account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        check_name = view_all_users()
        clean_name = pd.DataFrame(check_name, columns=["Username", "Password"])
        justName = clean_name["Username"].values.tolist()

        for i in justName:
            if new_user == i:
                st.warning('Username Already Taken')
                break
            if new_password == '':
                st.warning('Enter a Password')
                break

        if new_user != i and st.button("SignUp") and new_password != '':
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("You have successfully created an account")
            st.info("Go to Login Page")


if __name__ == '__main__':
    main()

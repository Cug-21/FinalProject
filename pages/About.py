import streamlit as st

st.set_page_config(
     page_title="About - ViewCano")

st.markdown("<h1 style='text-align: center; color: black;'>Welcome to the About Page!</h1>",
                unsafe_allow_html=True)

x = st.sidebar.radio("Select your Page: ", ['About Me', 'About the Project'])

if x == 'About Me':
    st.markdown("<h2 style='text-align: center; color: black;'>Let me Introduce myself, I am Conor Segreti, the developer of this Application. </h2>",
                unsafe_allow_html=True)

    me = st.selectbox("Select something you would like to know!", ["Interests", "Education", "Experience", "Social Media"])
    if me == 'Interests':
        st.markdown("<h3 style='text-align: center; color: black;'>Interests</h3>",
                unsafe_allow_html=True)
        st.subheader("1. Coral Reefs- The worlds most beautiful ecosystem, supporting so much more than just the ocean.")
        st.write("***")
        st.subheader("2. Aquariums & Terrariums- Having built many, bringing the natural world into my home.")
        st.write("***")
        st.subheader("3. Sports- I have played lacrosse my whole life and love it.")
        st.write("***")
        st.subheader("4. App Development- Having developed a few apps and enjoing doing so.")
    elif me == 'Education':
        st.markdown("<h3 style='text-align: center; color: black;'>My Education is as Follows!</h3>",
                unsafe_allow_html=True)
        school = st.select_slider("Choose Education Level", ["High School", "College"])
        if school == "High School":
            st.subheader("1. I attended St. Johns College High School In DC")
            st.write("***")
            st.subheader("2. I played varsity lacrosse all 4 years and was the president of the booster club my senior year")
            st.write("***")
            st.subheader("3. I also won an entrepreneurial challenge, winning a tour of the Innovation Light House which UA runs")
            st.write("***")
            st.subheader("4. During High School i volunteered to help at risk kids through an organization called Winner Lacrosse")

        elif school == "College":
            st.subheader("1. I currently attend Bentley University, I am a Computer Information System Major with a Minor in Finance.")
            st.write("***")
            st.subheader("2. I have been a member of the Bentley Mens lacrosse team for 3 years now.")
            st.write("***")
            st.subheader("3. The staff is very supportive and campus involvement is so easy.")
            st.write("***")
            st.subheader("4. Bentley has provided me great friends and a phenomenal education.")

    elif me == "Experience":
        st.markdown("<h3 style='text-align: center; color: black;'>Here is my Professional Work Experience!</h3>",
                unsafe_allow_html=True)
        st.subheader("1. Most Recently I was an intern of a Commercial Real Estate Bank.")
        st.write("***")
        st.subheader("2. Two Summers ago I worked as a server in a Country Club.")
        st.write("***")
        st.subheader("3. Prior to Covid my two best friends and I worked on a golf resort.")

    elif me == "Social Media":
        st.markdown("<h3 style='text-align: center; color: blue;'>To Learn more about me check out my Social Media Accounts!</h3>",
                unsafe_allow_html=True)
        st.write("***")
        st.write("Check out my linkedin! [link](https://www.linkedin.com/in/conorsegreti/)")
        st.write("Check out my twitter! [link](https://twitter.com/Cug_21)")
        st.write("Check out my GitHub! [link](https://github.com/Cug-21?tab=repositories)")


elif x == 'About the Project':
    st.markdown("<h2 style='text-align: center; color: purple;'>Final Project Python CS230</h2>",
                unsafe_allow_html=True)
    st.write("The purpose of this webpage is to show our knowledge in python more particular streamlit and manipulating dataframes.")
    st.write("My personal data was Volcanic eruptions and while I do feel like my data was easy to manipulate there were a few issue I ran into.")
    st.write("For example the date of the eruptions was formatted not as a date, this led me to some issues.")
    st.write("In addition the way some rock types where labeled maybe with an (s) at the end would lead to some issues.")
    st.write("We had to manipulate this data to display three different type of queries using three types of graphs.")
    st.write("I then decided to make a front end back end with a user sign-up and a chat room feature.")

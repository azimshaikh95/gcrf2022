import pdfkit
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader, Template
import os



st.set_page_config(layout="centered", page_icon="☁️", page_title="GoogleCloudReady Progress Report")

#Added by Azim
from datetime import date
today = date.today()


#Variable Names
date = "10-07"


#Program Variables
header = st.container()
login = st.container()
body = st.container()
owners = st.container()

#Hide Hamburger Menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



#Reading the file
data = pd.read_csv("data/" + date + ".csv")
df = pd.DataFrame(data)

for i in range(len(df["Student Email"])):
    df['Student Email'][i] = df['Student Email'][i].lower()


#WebApp -- "Milestone Leaderboard"
sidebarContent = st.sidebar.radio("Menu", ["Progress Report", "Milestone Leaderboard", "Program Resources", "Admin Zone"])
#sidebarContent = st.sidebar.radio("Menu", ["Progress Report", "Milestone Leaderboard", "Generate Badge", "Program Resources"])
#Progress Report Page
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
}
.last {
    font-size: 15px !important;
}

</style>
""", unsafe_allow_html=True)

def milestoneCal(quest, skillbg, tindex):
    rquest = int(df["# of Quests Completed"][tindex])
    rskillbg = int(df["# of Skill Badges Completed"][tindex])
    if (int(df["# of Quests Completed"][tindex]) >= quest):
        rquest = quest
    if (int(df["# of Skill Badges Completed"][tindex]) >= skillbg):
        rskillbg = skillbg
    per = int(((rquest + rskillbg) / (quest+skillbg)) * 100)
    return rquest, rskillbg, per

def findMilestoneLevel(tindex):
    level = 0
    cquest = int(df["# of Quests Completed"][tindex])
    cskillbg = int(df["# of Skill Badges Completed"][tindex])

    if (cquest >= 10 and cskillbg >= 5):
        level = 1
    if (cquest >= 20 and cskillbg >= 10):
        level = 2
    if (cquest >= 30 and cskillbg >= 15):
        level = 3
    if (cquest >= 40 and cskillbg >= 20):
        level = 4

    return level

def showStats():
    inactive = 0
    m0Count = 0
    m1Count = 0
    m2Count = 0
    m3Count = 0
    m4Count = 0
    totalQuests = 0
    totalSkillBadges = 0

    for i in range(len(df)):
        qCount = int(df["# of Quests Completed"][i])
        sCount = int(df["# of Skill Badges Completed"][i])

        level = 0

        if (qCount == 0 and sCount == 0):
            inactive += 1

        if (qCount < 10 or sCount < 5):
            if qCount == 0:
                if sCount >= 1:
                    m0Count += 1

            if sCount == 0:
                if qCount >= 1:
                    m0Count += 1

            if (qCount > 0 and sCount > 0):
                m0Count += 1

        if (qCount >= 10 and sCount >= 5):
            level = 1
        if (qCount >= 20 and sCount >= 10):
            level = 2
        if (qCount >= 30 and sCount >= 15):
            level = 3
        if (qCount >= 40 and sCount >= 20):
            level = 4

        if level == 1:
            m1Count += 1
        elif level == 2:
            m2Count += 1
        elif level == 3:
            m3Count += 1
        elif level == 4:
            m4Count += 1

        totalQuests += qCount
        totalSkillBadges += sCount

    return m0Count, m1Count, m2Count, m3Count, m4Count, totalQuests, totalSkillBadges, inactive

def prizeWinners(limit):
    finalList =[]
    for i in range(len(df)):
        if(df["level"][i] == limit):
            arr = str(df["Student Name"][i])
            URL = str(df["Google Cloud Skills Boost Profile URL"][i])
                        # arr = str(df["Student Name"][i]).split()
            # fname = arr[0]
            # lname = arr[-1]
            # name = fname + " " + lname
            name = "[" + arr.title() + "](" + URL + ")"
            finalList.append(name)         
            
    finalList.sort()    
    return finalList

    
def fmsc(tq, ts):
    frquest = int(questTotal)
    frskillbg = int(skillbgTotal)
    if (questTotal >= tq):
        frquest = tq
    if (skillbgTotal >= ts):
        frskillbg = ts
    fper = int(((frquest + frskillbg) / (tq + ts)) * 100)
    return frquest, frskillbg, fper
    
    
# def prizeWinners(limit):
    # finalList =[]
    # for i in range(len(df)):
        # if(df["level"][i] == limit):
            # arr = str(df["Student Name"][i]).split()
            # fname = arr[0]
            # lname = arr[-1]
            # name = fname + " "+ lname[0] + "."
            # finalList.append(name)
    # finalList.sort()
    # return finalList
    


if (sidebarContent == "Progress Report"):
    with(header):
        st.image('images/banner.png', use_column_width=True)
        st.markdown("<h1 style='text-align: center'><b>Daily Progress Report 🌩</b></h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center'><b>LJ Institute of Engineering & Technology, Ahmedabad</b></h1>", unsafe_allow_html=True)
        st.write("Last Updated On: " + date + "-2022")
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID").lower()

        #Input Activity
        status = False
        for i in df["Student Email"]:
            if( i == textInput):
                status = True
        if(textInput != "" and status):
            tindex = df[df["Student Email"] == textInput].index[0] #Finding the index of the search emailID
            st.title("Welcome " + str(df["Student Name"][tindex]) +" !")

            st.write("**Enrollment Status:** " + str(df["Enrolment Status"][tindex]))
            st.write("**EmailID:** " + str(df["Student Email"][tindex]))
            st.write("[View Google Cloud Skills Boost Profile URL](" + str(df["Google Cloud Skills Boost Profile URL"][tindex]) + ")")
            st.write("**Institution:** " + str(df["Institution"][tindex]))

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<b class="big-font">Milestone Status</b>', unsafe_allow_html=True)

            quest, skillbg, per = milestoneCal(40, 40, tindex)
            st.subheader("You have completed " + str(quest) + " Quests and " + str(skillbg) +" Skill Badges.")
            if(quest >= 10 and skillbg >= 5):
                st.balloons()

            #Milestone1
            quest, skillbg, per = milestoneCal(10, 5, tindex)
            #per = int(((quest+skillbg)/12)*100)
            st.subheader("Milestone1 :    " + str(per) +"% Completed\n Quests: " + str(quest)+ "/10, Skill Badge: " + str(skillbg)+ "/5")
            if(quest >= 10 and skillbg >= 5):
                st.write("🥳 Congratulations! You have completed your 1st Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            #Milestone2
            quest, skillbg, per = milestoneCal(20, 10, tindex)
            st.subheader("Milestone2 :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/20, Skill Badge: " + str(skillbg) + "/10")
            if (quest >= 20 and skillbg >= 10):
                st.write("🥳 Congratulations! You have completed your 2nd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Milestone3
            quest, skillbg, per = milestoneCal(30, 15, tindex)
            st.subheader("Milestone3 :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/30, Skill Badge: " + str(skillbg) + "/15")
            if (quest == 30 and skillbg == 15):
                st.write("🥳 Congratulations! You have completed your 3rd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Ultimate Milestone
            quest, skillbg, per = milestoneCal(40, 20, tindex)
            st.subheader("Ultimate Milestone :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/40, Skill Badge: " + str(skillbg) + "/20")
            if (quest >= 40 and skillbg >= 20):
                st.write("🥳 Congratulations! You have completed you Ultimate Milestone 🎊🎊🎊")
            else:
                st.progress(per)

        elif (textInput != "" and status == False):
            st.error("No Entry Found")

    with(owners):
        st.write("####")
        st.markdown('<body class= "last" >Developed & Managed By: <a href="https://in.linkedin.com/in/mohammedazim-shaikh">MohammedAzim Shaikh</a></body>', unsafe_allow_html=True)
        #st.write("Developed & Managed By : MohammedAzim Shaikh")

#Milestone Leaderboard Page
elif (sidebarContent == "Milestone Leaderboard"):
    with(header):
        st.image('images/banner.png', use_column_width=True)
        st.markdown("<h1><b>Milestone Leaderboard 🏃‍♂️ LJIET Ahmedabad</b></h1>", unsafe_allow_html=True)
        st.write("Last Updated On: " + date + "-2021")
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID").lower()
        st.write("####")

    status = False

    # if (textInput == "azim@ljku.edu.in" or textInput == "azim" or textInput == "azim@ljp" or textInput == "jayniyati2233@gmail.com" or textInput == "kirtankp1902@gmail.com"):
    
    if ( textInput == st.secrets["mail_fac1"] or textInput == st.secrets["mail_fac2"] or textInput == st.secrets["mail_fac3"] or textInput == st.secrets["mail_fac4"] or textInput == st.secrets["mail_fac5"] ):
    
        ml0, ml1, ml2, ml3, ml4, questTotal, skillbgTotal, inactiveCount = showStats()

        labels = ['Milestone0', 'Milestone1', 'Milestone2', 'Milestone3', 'Milestone4', 'Inactive']
        values = [ml0, ml1, ml2, ml3, ml4, inactiveCount]
        colors = ['cyan', 'blue', 'green', 'orange', 'gold', 'red']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=colors, line=dict(color='#000000', width=1)))
        
      
        
        st.write("## **📊 Facilitator Stats:** " + today.strftime("%B %d, %Y"))
        st.write("####")
        st.write("**No. of Quest completions:** " + str(questTotal))
        st.write("**No. of Skill Badge completions:** " + str(skillbgTotal))
        st.write("**Total Count:** " + str(questTotal + skillbgTotal))
        st.write("**Milestone 1 Achievers:** " + str(ml1))
        st.write("**Milestone 2 Achievers:** " + str(ml2))
        st.write("**Milestone 3 Achievers:** " + str(ml3))
        st.write("**Milestone 4 Achievers:** " + str(ml4))
        st.write("**Total Achievers:** " + str(ml1 + ml2 + ml3 + ml4))
        st.write("**Milestone 1 In Progress:** " + str(ml0))
        st.write("**Inactive Students:** " + str(inactiveCount))
        st.write("**Total Students Enrolled:** " + str(ml0 + ml1 + ml2 + ml3 + ml4 + inactiveCount))
        st.plotly_chart(fig)
        export_as_pdf = st.button("Export Report")
        
        

    for i in df["Student Email"]:
        if( i == textInput or textInput == "azim"):
            status = True
    if(textInput != "" and status):
        m4 = st.container()
        m3 = st.container()
        m2 = st.container()
        m1 = st.container()
        cred = st.container()

        df["level"] = 0
        for i in range(len(df)):
            quests = df["# of Quests Completed"][i]
            badges = df["# of Skill Badges Completed"][i]
            level=0
            if (quests >= 10 and badges >= 5):
                level = 1
            if (quests >= 20 and badges >= 10):
                level = 2
            if (quests >= 30 and badges >= 15):
                level = 3
            if (quests >= 40 and badges >= 20):
                level = 4
            df["level"][i] = level

        with(m4):
            flist  = prizeWinners(4)
            
            
            # st.subheader(m4_names)
            if (len(flist) != 0):
                st.markdown('<b class="big-font">🏆 Ultimate Milestone : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                for i in flist:
                    st.write("🔓 4️⃣ " + str(i))
                st.markdown("<hr>", unsafe_allow_html=True)

        with(m3):
            flist = prizeWinners(3)
            # st.subheader(m3_names)
            if (len(flist) != 0):
                st.markdown('<b class="big-font">🏆 Milestone 3 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 3 : Winners *-------- </h2>", unsafe_allow_html=True)
                for i in flist:
                    st.write("🔓 3️⃣ " + str(i))
                    #st.write("🔸  " + str(i))
                st.markdown("<hr>", unsafe_allow_html=True)

        with(m2):
            flist = prizeWinners(2)
            if (len(flist) != 0):
                st.markdown('<b class="big-font">🏆 Milestone 2 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 2 : Winners *-------- </h2>", unsafe_allow_html=True)
                for i in flist:
                    st.write("🔓 2️⃣ " + str(i))

                st.markdown("<hr>", unsafe_allow_html=True)

        with(m1):
            flist = prizeWinners(1)
            # st.subheader(m1_names)
            if (len(flist) != 0):
                st.markdown('<b class="big-font">🏆 Milestone 1 : Winners</b>', unsafe_allow_html=True)
                st.write("######")
                #st.markdown("<h2> --------* Milestone 1 : Winners *-------- </h2>", unsafe_allow_html=True)

                for i in flist:
                    st.write("🔓 1️⃣ " + str(i) )

                st.markdown("<hr>", unsafe_allow_html=True)
                st.write("#####")

        with(cred):
            st.markdown('<body class= "last" >Developed & Managed By: <a href="https://in.linkedin.com/in/mohammedazim-shaikh">MohammedAzim Shaikh</a></body>',unsafe_allow_html=True)
            #st.write("Developed & Managed By : MohammedAzim Shaikh")
            
    elif (textInput == "azim@ljku.edu.in" or textInput == "azim" or textInput == "azim@ljp" or textInput == "jayniyati2233@gmail.com" or textInput == "kirtankp1902@gmail.com"):

        st.snow()
        st.info("Dear Facilitator, Please find the above progress for LJ Institute of Engineering & Technology, Ahmedabad.")
        status = True
        

    elif (textInput != "" and status == False):
        st.error("Sorry, we won't be able to show you the Milestone Achievers unless and until you are a Participant under GCRF Program LJ Institute of Engineering & Technology, Ahmedabad.")

elif (sidebarContent == "Generate Badge"):
    with(header):
        st.image('images/banner.png', use_column_width=True)
        st.markdown("<h1 style='text-align: center'><b>🔖 Generate GoogleCloudReady Badge</b></h1>", unsafe_allow_html=True)
        st.write("#####")

    with(login):
        textInput = st.text_input("Enter your Email ID").lower()

        #Input Activity
        status = False
        for i in df["Student Email"]:
            if( i == textInput):
                status = True
        if(textInput != "" and status):
            tindex = df[df["Student Email"] == textInput].index[0]
            level = findMilestoneLevel(tindex)

            if level == 0:
                st.warning("Achieve Your First Milestone  to Get your Badge")
                st.image('images/milestone0.png', use_column_width=True)
            else:
                st.success(f"You're Currently on Milestone {level}")
                image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
                if image_file is not None:
                    size = (750, 750)
                    if level == 1:
                        img = Image.open("images/milestone1.png").convert("RGBA")
                    elif level == 2:
                        img = Image.open("images/milestone2.png").convert("RGBA")
                    elif level == 3:
                        img = Image.open("images/milestone3.png").convert("RGBA")
                    elif level == 4:
                        img = Image.open("images/milestone4.png").convert("RGBA")
                    elif level == 0:
                        img = Image.open("images/milestone0.png").convert("RGBA")
                    img = img.resize(size, Image.ANTIALIAS)
                    card = Image.open(image_file)

                    card = card.resize(size, Image.ANTIALIAS)

                    card.paste(img, (0, 0), img)
                    card.save("first.jpg", format="png")
                    st.image(card)
        elif (textInput != "" and status == False):
            st.error("No Entry Found")

        st.write("### **Instructions on Uploading your Image and Downloading the Badge:**")
        st.write(f"""
        * You should have completed at least 1st Milestone to get your badge
        * Click on Browse Files below to Upload an image
        * Upload a Square Image to get the best version of your Badge
        * If you upload a landscape or out of shape image, it would be resized to 1:1
        * According to your Milestone, your picture will be automatically applied with a badge
        * Right click on the Image and select save image as to Download the file
        * Then do share on your social media handles by tagging us as your Facilitator and Google Cloud India, also use `#GoogleCloudReady` tag. Google Cloud team closely monitor this tag :smile: :tada:
        """)
        st.info("Made With ❤️ by [MohammedAzim Shaikh](https://in.linkedin.com/in/mohammedazim-shaikh)")




elif (sidebarContent == "Admin Zone"):

    with(header):
        st.image('images/banner.png', use_column_width=True)
        st.markdown("<h1><b>LJIET 🏃‍♂️ Facilitator Leaderboard</b></h1>", unsafe_allow_html=True)
        st.write("Last Updated On: " + date + "-2021")
        st.write("#####")

    with(login):
        st.warning("Only Facilitator are allowed to enter this zone !")
        textInput = st.text_input("Enter Secret Code", type="password").lower()
        st.write("####")

    status = False


    if (textInput == st.secrets["app_secret"] ):
    
        ml0, ml1, ml2, ml3, ml4, questTotal, skillbgTotal, inactiveCount = showStats()

        labels = ['Milestone0', 'Milestone1', 'Milestone2', 'Milestone3', 'Milestone4', 'Inactive']
        values = [ml0, ml1, ml2, ml3, ml4, inactiveCount]
        colors = ['cyan', 'blue', 'green', 'orange', 'gold', 'red']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=colors, line=dict(color='#000000', width=1)))
        
        st.snow()
        st.info("Dear Facilitator, Please find the progress for LJ Institute of Engineering & Technology, Ahmedabad - Updated On: " + date + "-2022")        
        
        
        st.write("## **📊 Facilitator Stats:** " + today.strftime("%B %d, %Y"))
        st.write("####")
        st.write("**No. of Quest completions:** " + str(questTotal))
        st.write("**No. of Skill Badge completions:** " + str(skillbgTotal))
        st.write("**Total Count:** " + str(questTotal + skillbgTotal))
        st.write("**Milestone 1 Achievers:** " + str(ml1))
        st.write("**Milestone 2 Achievers:** " + str(ml2))
        st.write("**Milestone 3 Achievers:** " + str(ml3))
        st.write("**Milestone 4 Achievers:** " + str(ml4))
        st.write("**Total Achievers:** " + str(ml1 + ml2 + ml3 + ml4))
        st.write("**Milestone 1 In Progress:** " + str(ml0))
        st.write("**Inactive Students:** " + str(inactiveCount))
        st.write("**Total Students Enrolled:** " + str(ml0 + ml1 + ml2 + ml3 + ml4 + inactiveCount))
        st.plotly_chart(fig)
        # export_as_pdf = st.button("Export Report")
               
        
        ###           

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<b class="big-font">🏆 Facilitator Milestone Status</b>', unsafe_allow_html=True)

        tq, ts, tp = fmsc(500, 250)
        # st.subheader("You have completed " + str(tq) + " Quests and " + str(ts) +" Skill Badges.")
        if(tq >= 500 and ts >= 250):
            st.balloons()

        #Milestone1
        tq, ts, tp = fmsc(500, 250)            
        st.subheader("Milestone1 :    " + str(tp) +"% Completed\n Quests: " + str(tq)+ "/500, Skill Badge: " + str(ts)+ "/250")
        M1Per = str(tp)
        if(tq >= 500 and ts >= 250):
            st.progress(tp)
            st.write("🥳 Congratulations! You have completed your 1st Milestone 🎉🎉🎉")
            
        else:
            st.progress(tp)

        #Milestone2
        tq, ts, tp = fmsc(1000, 500)
        st.subheader("Milestone2 :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/1000, Skill Badge: " + str(ts) + "/500")
        M2Per = str(tp)
        if (tq >= 1000 and ts >= 500):
            st.progress(tp)
            st.write("🥳 Congratulations! You have completed your 2nd Milestone 🎉🎉🎉")            
        else:
            st.progress(tp)
            

        # Milestone3
        tq, ts, tp = fmsc(2000, 1000)
        st.subheader("Milestone3 :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/2000, Skill Badge: " + str(ts) + "/1000")
        M3Per = str(tp)
        if (tq >= 2000 and ts >= 1000):
            st.progress(tp)
            st.write("🥳 Congratulations! You have completed your 3rd Milestone 🎉🎉🎉")
            M3Per = str(tp);
        else:
            st.progress(tp)

        # Ultimate Milestone
        tq, ts, tp = fmsc(3000, 1500)
        st.subheader("Ultimate Milestone :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/3000, Skill Badge: " + str(ts) + "/1500")
        M4Per = str(tp)
        if (tq >= 3000 and ts >= 1500):
            st.progress(tp)
            st.write("🥳 Congratulations! You have completed you Ultimate Milestone 🎉🎉🎉")
            M4Per = str(tp);
        else:
            st.progress(tp)
        
        ###
           
        left, right = st.columns(2)
    
    
        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        template = env.get_template("adminreport.html")

        left.info("Want to Save?")
        submit = left.button("📝 Generate PDF")

        if submit:
            html = template.render(
                questTotal=str(questTotal),
                skillbgTotal=str(skillbgTotal),
                qpluss=str(questTotal + skillbgTotal),
                ml1=str(ml1),
                ml2=str(ml2),
                ml3=str(ml3),
                ml4=str(ml4),
                ta=str(ml1 + ml2 + ml3 + ml4),
                ml0=str(ml0),               
                inactiveCount=str(inactiveCount),
                te=str(ml0 + ml1 + ml2 + ml3 + ml4 + inactiveCount),
                M1Per=str(M1Per),
                M2Per=str(M2Per),
                M3Per=str(M3Per),
                M4Per=str(M4Per),
                date=today.strftime("%B %d, %Y"),
                
                 
            )

            pdf = pdfkit.from_string(html, False)
            # st.balloons()          
            # if ( str(df["Status"][tindex]) == "Pass" ):
                # st.balloons()  
                # st.success("You have cleared the exam!")
            # else:
                # st.error("You haven't cleared the exam!")
          

            right.success("🎉 Your Result PDF Generated!")                 
            right.download_button(
                "🖨️ Download PDF",
                data=pdf,
                file_name="GCRF-LJIET-"+date+".pdf",
                mime="application/octet-stream",
            )
        
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("**🎁 Facilitator Prizes**")
        st.image('images/facilitator_prizes.png', use_column_width=True)
        
        
        
    elif (textInput != "" ):
            st.error("Sorry, we won't be able to enter you to Admin Zone unless and until you are a Facilitator at LJ Institute of Engineering & Technology, Ahmedabad.")
        
        
        


else:  
    with(header):
        st.image('images/banner.png', use_column_width=True)
        st.markdown("<h1><b>GoogleCloudReady Program Resources</b></h1>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("**Program Deadline: 25 June, 2022**")

        st.subheader("**Important Links**")
        st.write("🌐 [GCR Program Site](https://bit.ly/crf-site)")
        st.write("📁 [Program Syllabus](https://bit.ly/crf-syllabus)")
        #st.write("✅ [Solution Videos](https://docs.google.com/document/d/1MKLH88xd8YjW9qdGHTiWQ2CP3KvB9B8FWYEYwfOrTA8/view)")
        #st.write("✅ [Solution Videos](https://docs.google.com/document/d/1B0iHlOd2LkuOW1j7dpfSW_GFAzR_jhUX-WnuqSwrXUA/edit)")

        st.subheader("**Prizes**")
        st.image('images/student_prizes.png', use_column_width=True)

        st.info("Made With ❤️ by [MohammedAzim Shaikh](https://in.linkedin.com/in/mohammedazim-shaikh)")

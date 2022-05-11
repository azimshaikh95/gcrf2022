def fmilestoneCal(tquest, tskillbg):
    frquest = int(questTotal)
    frskillbg = int(skillbgTotal)
    #if (int(df["# of Quests Completed"][tindex]) >= tquest):
        frquest = tquest
    #if (int(df["# of Skill Badges Completed"][tindex]) >= tskillbg):
        frskillbg = tskillbg
    per = int(((frquest + frskillbg) / (tquest+tskillbg)) * 100)
    return frquest, frskillbg, fper



        if(textInput != "" and status):
            

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<b class="big-font">Facilitator Milestone Status</b>', unsafe_allow_html=True)

            quest, skillbg, per = fmilestoneCal(750, 750)
            st.subheader("You have completed " + str(quest) + " Quests and " + str(skillbg) +" Skill Badges.")
            if(quest >= 500 and skillbg >= 250):
                st.balloons()

            #Milestone1
            quest, skillbg, per = fmilestoneCal((750, 750)            
            st.subheader("Milestone1 :    " + str(per) +"% Completed\n Quests: " + str(quest)+ "/10, Skill Badge: " + str(skillbg)+ "/5")
            if(quest >= 500 and skillbg >= 250):
                st.write("🥳 Congratulations! You have completed your 1st Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            #Milestone2
            quest, skillbg, per = fmilestoneCal(1500, 1500)
            st.subheader("Milestone2 :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/20, Skill Badge: " + str(skillbg) + "/10")
            if (quest >= 1000 and skillbg >= 500):
                st.write("🥳 Congratulations! You have completed your 2nd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Milestone3
            quest, skillbg, per = fmilestoneCal(3000, 3000)
            st.subheader("Milestone3 :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/30, Skill Badge: " + str(skillbg) + "/15")
            if (quest == 2000 and skillbg == 1000):
                st.write("🥳 Congratulations! You have completed your 3rd Milestone 🎊🎊🎊")
            else:
                st.progress(per)

            # Ultimate Milestone
            quest, skillbg, per = fmilestoneCal(4500, 4500)
            st.subheader("Ultimate Milestone :    " + str(per) +"% Completed\n Quests: " + str(quest) + "/40, Skill Badge: " + str(skillbg) + "/20")
            if (quest >= 3000 and skillbg >= 1500):
                st.write("🥳 Congratulations! You have completed you Ultimate Milestone 🎊🎊🎊")
            else:
                st.progress(per)

        elif (textInput != "" and status == False):
            st.error("No Entry Found")
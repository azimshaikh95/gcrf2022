def fmsc(tq, ts):
    frquest = int(tq)
    frskillbg = int(ts)
    
    per = int(((frquest + frskillbg) / (tquest+tskillbg)) * 100)
    return frquest, frskillbg, fper

           

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown('<b class="big-font">Facilitator Milestone Status</b>', unsafe_allow_html=True)

            tq, ts, tp = fmsc(750, 750)
            st.subheader("You have completed " + str(tq) + " Quests and " + str(ts) +" Skill Badges.")
            if(tq >= 500 and ts >= 250):
                st.balloons()

            #Milestone1
            tq, ts, tp = fmsc((750, 750)            
            st.subheader("Milestone1 :    " + str(tp) +"% Completed\n Quests: " + str(tq)+ "/10, Skill Badge: " + str(ts)+ "/5")
            if(tq >= 500 and ts >= 250):
                st.write("🥳 Congratulations! You have completed your 1st Milestone 🎊🎊🎊")
            else:
                st.progress(tp)

            #Milestone2
            tq, ts, tp = fmsc(1500, 1500)
            st.subheader("Milestone2 :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/20, Skill Badge: " + str(ts) + "/10")
            if (tq >= 1000 and ts >= 500):
                st.write("🥳 Congratulations! You have completed your 2nd Milestone 🎊🎊🎊")
            else:
                st.progress(tp)

            # Milestone3
            tq, ts, tp = fmsc(3000, 3000)
            st.subheader("Milestone3 :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/30, Skill Badge: " + str(ts) + "/15")
            if (tq >= 2000 and ts >= 1000):
                st.write("🥳 Congratulations! You have completed your 3rd Milestone 🎊🎊🎊")
            else:
                st.progress(tp)

            # Ultimate Milestone
            tq, ts, tp = fmsc(4500, 4500)
            st.subheader("Ultimate Milestone :    " + str(tp) +"% Completed\n Quests: " + str(tq) + "/40, Skill Badge: " + str(ts) + "/20")
            if (tq >= 3000 and ts >= 1500):
                st.write("🥳 Congratulations! You have completed you Ultimate Milestone 🎊🎊🎊")
            else:
                st.progress(tp)


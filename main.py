import streamlit as st
import os

#logo
st.image(os.path.join(os.getcwd(),"static","HotWheels.png"))


#vars

tabs = st.tabs(["Leader Board","Players","New Race"])

if "players" not in st.session_state:
    st.session_state.players=[]

#functions

def addPlayer(_name,_points):
    print(f"added {_name}")
    st.session_state["players"].append({"name":_name,"points":_points,"lore":f"*insert {_name}'s lore*","image":None})

def removePlayer(_player):
    st.session_state["players"].remove(_player)

def newRace(_racers):
    st.balloons()
    st.success(f"{_racers[0]} won the race!")

    count = len(_racers)*2
    for racer in _racers:
        print(racer)

        newPlayer=True
        for player in st.session_state["players"]:
            if racer==player["name"]:
                print(f"FOUND {racer}/{player} ALREADY EXISTED")
                newPlayer=False
                player["points"]+=count
        
        if newPlayer:
            addPlayer(racer,count)
        
        count-=2
        

#save and load



#tabs

#tab 1
with tabs[0]:
    leaderboard=[]
    st.title("Leader Board")
    count=1
    try: jutsSoThatItDoesntWriteToTheWebsite = st.session_state["players"][0]
    except IndexError:
        st.write("Try making a character or documenting a race ")
    else:
        container = st.container(border=True)
        leaderboard=st.session_state["players"]
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        for player in leaderboard:
            with container:
                if count==1:
                    st.header(f"{count}. {player["name"]}, with {player["points"]} points")
                elif count <= 3:
                    st.header(f"*{count}. {player["name"]}, with {player["points"]} points*")
                else:
                    st.subheader(f"*{count}. {player["name"]}, with {player["points"]} points*")
            count+=1
#tab 2
with tabs[1]:

    st.title("Players")

    if not st.session_state["players"]:
        st.write("No made characters")
    else:
        for player in st.session_state["players"]:
            container=st.container(border=True)
            with container:
                st.header(player["name"])
                st.write(f"Currently has {player['points']} points")

                #image
                if player["image"]is None:
                    player["image"]=st.file_uploader(f"Choose an image for {player["name"]}...",type=["jpg","png","jpeg"])
                    st.button(f"Submit {player["name"]}'s image")
                else:
                    st.image(player["image"],width=1080)

                player["lore"]=st.text_input(f"{player['name']}'s lore",player["lore"],label_visibility="hidden")
            
                st.button(f"Remove {player["name"]}",on_click=removePlayer,args=(player,))
    
    st.divider()

    st.header("New Player")

    newPlayerName=st.text_input("New Players name")
    if newPlayerName != "":
        trueNewPlayer=True
        for player in st.session_state["players"]:
            if player["name"]==newPlayerName:
                trueNewPlayer=False
        if trueNewPlayer:   
            st.button("Add New Player",on_click=addPlayer(newPlayerName,0))
        else:
            st.write("There is already a player with this name")
    else:
        st.write("Enter the new players name first")
            
            

        
#tab3
with tabs[2]:
    st.title("New Race Stats")
    racersI=st.slider("Racers",2,12,5)
    racersL=[]
    newPlayers=[]
    for racer in range(racersI):
        r=st.text_input(f"p{racer+1}")
        racersL.append(r)
        newPlayer=True
        for player in st.session_state["players"]:
            if r==player["name"]:
                newPlayer=False
        
        if newPlayer and racersL[racer]!="":
            newPlayers.append(st.checkbox(f"p{racer+1} has not been entered previously, make a new player?"))

    if all(newPlayers) and all(x!="" for x in racersL):
        st.button("done",on_click=newRace,args=(racersL,))
    else:
        st.warning("Some of the players havent been previously entered, please make them already created characters or create them using the checkbox below them. Also remeber to fill out ALL of the players names.")

import streamlit as st
import pandas as pd
import os

#logo
st.image(os.path.join(os.getcwd(),"static","HotWheels.png"))


#vars

tabs = st.tabs(["Leader Board","Players","Teams","New Race"])

#sess state

if "players" not in st.session_state:
    st.session_state.players=[]

if "teams" not in st.session_state:
    st.session_state.teams=[]

#functions

def toggleEditLore(_player):
    _player["editingLore"]=not _player["editingLore"]

def addPlayer(_name,_points):
    print(f"added {_name}")
    st.session_state["players"].append({"name":_name,"points":_points,"lore":f"*insert {_name}'s lore*","editingLore":True,"image":None,"team":None,"nationality":None})

def addTeam(_name):
    st.session_state["teams"].append({"name":_name,"points":0,"players":[],"icon":None})

def addPlayerToTeam(_playerName,_teamName):
    for team in st.session_state["teams"]:
        if team["name"]==_teamName:
            team["players"].append(_playerName)
            break
    
    for player in st.session_state["players"]:
        if player["name"]==_playerName:
            player["team"]=_teamName

def removePlayer(_player):
    st.session_state["players"].remove(_player)

def calcPoints(_team):
    points=0
    for team in st.session_state["teams"]:
        if team["name"]==_team:
            for teamPlayer in team["players"]:
                for player in st.session_state["players"]:
                    if teamPlayer==player["name"]:
                        points+=player["points"]
            return points

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
        leaderboard=st.session_state["players"]
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        
        positions=[]
        names=[]
        nationalities=[]
        teams=[]
        points=[]
        teamPoints=[]

        position = 1

        for racer in leaderboard:
            positions.append(position)
            position+=1

            names.append(racer["name"])

            if racer["nationality"] is None:
                nationalities.append("IDK")
            else:
                nationalities.append(racer["nationality"])

            if racer["team"] is None:
                teams.append("NON")
            else:
                teams.append(racer["team"])
            
            points.append(racer["points"])

            if racer["team"] is None:
                teamPoints.append("N/A")
            else:
                for team in st.session_state["teams"]:
                    if team["name"]==racer["team"]:
                        teamPoints.append(team["points"])
                        break
            

        leaderboardDF=pd.DataFrame({
            "POS.":positions,
            "RACERS":names,
            "NATIONALITY":nationalities,
            "TEAM":teams,
            "PTS.":points,
            "TEAM PTS.":teamPoints
        })

        st.dataframe(leaderboardDF,hide_index=True)
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
                if not player["nationality"]:
                    player["nationality"]=st.text_input(f"Insert {player["name"]}'s nationality")
                    st.button(f"Submit {player["name"]} nationality")
                else:
                    st.write(f"Nationality is {player["nationality"]}")
                st.write(f"In the team: {player["team"]}")
                #image
                if player["image"]is None:
                    player["image"]=st.file_uploader(f"Choose an image for {player["name"]}...",type=["jpg","png","jpeg"])
                    st.button(f"Submit {player["name"]}'s image")
                else:
                    st.image(player["image"],width=1080)

                if player["editingLore"]:
                    player["lore"]=st.text_input(f"{player['name']}'s lore",player["lore"],label_visibility="hidden")
                    st.button("Submit Lore",on_click=toggleEditLore,args=(player,))
                else:
                    with st.container(border=True):
                        st.write(player["lore"])
                        st.button("Edit lore",on_click=toggleEditLore,args=(player,))
            
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
            

#tab 3
with tabs[2]:
    st.title("Teams")

    if not st.session_state["teams"]:
        st.write("Make a team first")
    else:
        for team in st.session_state["teams"]:
            team["points"]=calcPoints(team["name"])
            container=st.container(border=True)
            with container:
                st.header(team["name"])
                st.write(f"Currently has {team['points']} points")
                
                if team["icon"]is None:
                    team["icon"]=st.file_uploader(f"Choose an icon for {team["name"]}...",type=["jpg","png","jpeg"])
                    st.button(f"Submit {team["name"]}'s icon")
                else:
                    st.image(team["icon"],width=100)

                st.subheader("Players:")
                if team["players"] == []:
                    st.write("Add a player to the team")
                else:
                    for player in team["players"]:
                        st.write(f"{player}")
                
                st.divider()

                newPlayerName = st.text_input(f"Add a player to {team["name"]}")
                
                existingPlayer=False
                for player in st.session_state["players"]:
                    if player["name"]==newPlayerName:
                        existingPlayer=True
                
                if existingPlayer:
                    st.button(f"Add player to {team["name"]}",on_click=addPlayerToTeam,args=(newPlayerName,team["name"]))
                else:
                    st.write("That player doesnt exist")

                st.divider()

    
    st.divider()
    st.header("New Team")

    newTeamName=st.text_input("Team Name")
    if newTeamName == "":
        st.write("Give the team a name first")
    else:
        st.button("Make Team",on_click=addTeam,args=(newTeamName,))


        
#tab4
with tabs[3]:
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

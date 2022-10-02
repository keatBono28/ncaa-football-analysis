import pandas as pandas
import os
import csv

drop_set_headings = [20,21,42,43,64,65,86,87,108,109,130,131]

excel_writer = pandas.ExcelWriter("football.xlsx", engine='xlsxwriter')



def main():
    print("Starting to gather defense data...\n")
    get_defense_data()
    print("Completed\n")
    print("Starting to gather offensive data...\n")
    get_offense_data()
    print("Completed\n")
    print("Starting to gather special teams data...\n")
    get_special_teams_data()
    print("Completed\n")
    

def get_defense_data():
    raw_table = pandas.read_html("https://www.sports-reference.com/cfb/years/2022-team-defense.html", header=1)
    raw_table = raw_table[0].drop((drop_set_headings), axis=0)
    final_table = raw_table.sort_values(by='School')
    final_table.to_csv('defense.csv', index=False)

def get_offense_data():
    raw_table = pandas.read_html("https://www.sports-reference.com/cfb/years/2022-team-offense.html", header=1)
    raw_table = raw_table[0].drop((drop_set_headings), axis=0)
    final_table = raw_table.sort_values(by='School')
    table_size = final_table["School"].size-1
    # Alter the table columns
    final_table = alter_offense_table_columns(final_table)
    final_table["Avgerage Passing Yards Per Attempt"] = final_table["Average Passing Yards Per Game"].astype(float) / final_table["Average Passing Attempts"].astype(float)
    final_table["AvgPassYdsGame"] = (final_table["Average Passing Yards Per Game"].astype(float) * 1.0) / (final_table["Games"].astype(float) * 1)
    final_table["pTilePassYardsAttempts"] = final_table["Average Passing Attempts"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["pTilePercentCmp"] = final_table["Pct"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["AvgYdsGamePTile"] = final_table["AvgPassYdsGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["AvgRushYardsPerAttempt"] = (final_table["Yds.1"].astype(float)) / (final_table["Att.1"].astype(float))
    final_table["AvgRushYardsPerAttempt-Ptile"] = final_table["AvgRushYardsPerAttempt"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["AvgRushYardsPerGame"] = final_table["Yds.1"].astype(float) / final_table["Games"].astype(float)
    final_table["AvgRushYardsPerGamePtile"] = final_table["AvgRushYardsPerGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["AvgPlaysPerGame"] = final_table["Plays"].astype(float) / final_table["Games"].astype(float)
    final_table["AvgPlaysPerGamePtile"] = final_table["AvgPlaysPerGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["TotalOffenseYdsPtile"] = final_table["Yds.2"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["YardsPerPlayPtile"] = final_table["Avg.1"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["1stDownPerGame"] = final_table["Tot"].astype(float) / final_table["Games"].astype(float)
    final_table["1stDownPerGamePtile"] = final_table["1stDownPerGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["PenaltyYardsPerGame"] = final_table["Yds.3"].astype(float) / final_table["Games"].astype(float)
    final_table["PenYardsPerGamePtile"] = final_table["PenaltyYardsPerGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    final_table["TurnoversPerGame"] = final_table["Tot.1"].astype(float) / final_table["Games"].astype(float)
    final_table["TurnoversPerGamePtile"] = final_table["TurnoversPerGame"].rank(method='max', pct=True).apply(lambda x: 100.0*(x-1/table_size))
    
    #final_table.to_excel(excel_writer, sheet_name='offense',index=False)
    #excel_writer.save()
    final_table.to_csv('offense.csv', index=False)

def get_special_teams_data():
    raw_table = pandas.read_html("https://www.sports-reference.com/cfb/years/2022-special-teams.html", header=1)
    raw_table = raw_table[0].drop((drop_set_headings), axis=0)
    final_table = raw_table.sort_values(by='School')
    final_table.to_csv('special.csv', index=False)

def alter_offense_table_columns(table):
    # Rename Column Headers in order
    table.rename(columns={
        "Rk" : "Rank", 
        "G" : "Games",
        "Pts" : "Average Points Per Game",
        "Cmp" : "Average Passing Completions",
        "Att" : "Average Passing Attempts",
        "Yds" : "Average Passing Yards Per Game"
    }, inplace=True)
    table.insert(6, "Avgerage Passing Yards Per Attempt", "")
    table.insert(7, "pTilePassYardsAttempts","")
    table.insert(9, "pTilePercentCmp","")
    table.insert(11, "AvgPassYdsGame", "")
    table.insert(12, "AvgYdsGamePTile", "")
    table.insert(15, "AvgRushYardsPerAttempt", "")
    table.insert(16, "AvgRushYardsPerAttempt-Ptile", "")
    table.insert(18, "AvgRushYardsPerGame", "")
    table.insert(19, "AvgRushYardsPerGamePtile", "")
    table.insert(23, "AvgPlaysPerGame", "")
    table.insert(24, "AvgPlaysPerGamePtile", "")
    table.insert(26, "TotalOffenseYdsPtile", "")
    table.insert(28, "YardsPerPlayPtile", "")
    table.insert(33, "1stDownPerGame", "")
    table.insert(34, "1stDownPerGamePtile", "")
    table.insert(37, "PenaltyYardsPerGame", "")
    table.insert(38, "PenYardsPerGamePtile", "")
    table.insert(42, "TurnoversPerGame", "")
    table.insert(43, "TurnoversPerGamePtile", "")
    return table

main()
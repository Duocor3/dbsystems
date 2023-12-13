from openai import OpenAI
import re

client = OpenAI()

usrdone = False
tables = dict()
skip = False

# Schema Input
while not usrdone:
    print("Add a table in this format (no quotes): 'table_name'/'table_desc'")
    table_name_desc = input("Type DONE to complete:\n").split("/")
    if table_name_desc[0] == "abuka":
        skip = True
        break
    if table_name_desc[0] == "DONE":
        usrdone = True
    else:
        tables[table_name_desc[0]] = [table_name_desc[1]]
        columns = input("What are the columns of \""+table_name_desc[0]+
                        "\"?\nType in this format (no quotes): 'col_1_name'/'col_1_desc','col_2_name'/'col_2_desc'...\n").split(",")
        
        for col in columns:
            c = col.split("/")
            yn = "Y"
            relations = []
            
            while yn == "Y":
                relation = tuple(input("What are the relations between "+c[0]+" and other foreign columns in the schema?"+
                " If none, leave blank.\nChoose between 1-1 (one-to-one), 1-n (one-to-many), n-1 (many-to-one), and n-n (many-to-many).\n"+
                "Type in this format (no quotes): 'foreign_table_name','foreign_col_name',[1-1/1-n/n-1/n-n]\n").split(","))
                
                if len(relation) > 1:
                    relations.append(relation)
                yn = input("Add another relation for the "+c[0]+" column? Y/N\n")

            tables[table_name_desc[0]].append((c[0], c[1], relations))

numrows = input("How many rows should each table in the database have?\n")

while int(numrows)*len(tables) > 100:
    numrows = input("Total number of rows in the database can't exceed 100! You have "+len(tables)+" tables! How many rows should each table in the database have?\n")

#Prompt Generator
ai_prompt = ""

s1 = "Generate "+str(len(tables))+" SQL tables. Each table should have "+numrows+" table entries inserted. Generate all data and don't skip any rows. The names of the tables are "
s2 = "Don't include any other text besides the SQL code. The CREATE TABLE functions should only create columns, and not impose any constraints. Here are the rules for the tables that all entries MUST follow, no matter what. Only generate table entries that follow all the rules:\n\n"
s_tables = ""

for table in tables:
    s3 = ""
    s4 = ""
    
    s1 += "\"" + table + "\", "
    
    s3 += "\"" + table + "\" table:\n"
    s3 += "- Description: " + tables[table][0] + "\n- Contains these " + str(len(tables[table])-1) + " columns: "
    
    for column in tables[table][1:]:
        s3 += "\""+column[0]+"\" ("+column[1]+"), "
        
        for relation in column[2]:
            s4 += "- \""+column[0]+"\" maintains an exact " + relation[2] + " relationship with column \"" + relation[1] + "\" in table \"" + relation[0]+"\"\n"
    s3 = s3[:-2]+"\n"+s4+"\n"
    
    s_tables += s3
    

s1 = s1[:-2]+". All data must be real or as close to real as possible. "

# AI Interface
ai_prompt = s1+s2+s_tables

if skip:
    ai_prompt = input("Paste AI prompt\n")
    
regenerate = "N"

while regenerate == "N":
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a system that generates SQL relational tables with realistic data that ALWAYS follow the relational rules betweeen each table. Responses should only comprise of SQL code, with no additional remarks."},
        {"role": "user", "content": ai_prompt},
      ]
    )

    ai_response = completion.choices[0].message.content

    print(ai_prompt)
    print(ai_response)

    f = open("database.sql", "w")
    f.write(ai_response)
    f.close()
    
    regenerate = input("Are you satisfied with the database generated? Y/N\n")
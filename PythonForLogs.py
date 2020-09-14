import glob
import os
import requests
import http.client
import time

def reform():       

    for file in glob.glob('logs/*.log'):
        with open(file, 'r+') as f:
            text = f.readlines()
            list = []
            list.append(text[3])

            for x in text: 
                if (x[0] != "#"):
                    list.append(x)

        f = open(file,"w+")
        for i in list:
            f.write(i)

    f.close()


def change_name():

    for file in glob.glob('logs/*.log'):
        with open(file, 'r+') as f:
            text = f.readlines()
    
        if len(text[3].split(' ')) == 14:
            os.rename(file, file.replace('u','12'))
        else:
            os.rename(file, file.replace('u','15'))

    f.close()


def ip_transformation():

    ip_translator = []

    for file in glob.glob('logs/*.log'):
        with open(file, 'r+') as f:
            text = f.readlines()
            print("-----------LOG CHANGED------------")

        ip_position=8

        for i in range(1,len(text)):
            
            try:
                ip = text[i].split(' ')[ip_position]
            except (IndexError, KeyError, TypeError):
                ip = "NA"

            position = []
            for j in range(len(ip_translator)):
                if ip == ip_translator[j][0]:
                    position = j
                
            if position != []:
                ##### Get the values directly from the ip translator list
                final_ip_columns = [ip,'|' , ip_translator[position][2], '|', ip_translator[position][4], '|', ip_translator[position][6], '|', ip_translator[position][8]]               
            else:
                ##### If values are not found fetch them from API and append them to the ip_translator as well as the final list
                try: 
                    r = requests.get("http://api.ipstack.com/" + ip + "?access_key=9a3e2e46b62ad8e929806aef92ad7833&format=1")
                    ip_translator.append([ip,'|', r.json()["country_name"],'|', r.json()["region_name"],'|', r.json()["city"],'|', r.json()["zip"]])
                    final_ip_columns = [ip,'|', r.json()["country_name"],'|', r.json()["region_name"],'|', r.json()["city"],'|', r.json()["zip"]]
                except (IndexError, KeyError, TypeError):
                    ip_translator.append([ip,'|', " ",'|', " ",'|', " ",'|', " "])
                    final_ip_columns = [ip,'|', " ",'|', " ",'|', " ",'|', " "]

                print(ip_translator[-1])  
                
                if(final_ip_columns) is not None:
                    f2 = open("ip_locations.txt", "a", encoding="utf-8")
                    f2.write(" ".join(map(str, ip_translator[-1])))
                    f2.write("\n")

            ##### 10.000 Requests per account
            #r = requests.get("http://api.ipstack.com/" + ips + "?access_key=9a3e2e46b62ad8e929806aef92ad7833&format=1")
            ##### Free has only with continent
            #r = requests.get("https://api.ipgeolocationapi.com/geolocate/" + ips)
      
    f.close()


def same_columns():

    for file in glob.glob('logs/*.log'):  
        with open(file, 'r+') as f:
            text = f.readlines()

            #os.rename(file, file.replace('12','12to15'))
            f3 = open("Final_NR_NG.log", "a", encoding="utf-8")
            f4 = open("possible_errors.log", "a", encoding="utf-8")
            error_count = 0
            
            if "12_ex" in file:
                log_display = False
                for i in range(len(text)):
                    if i == 0:            
                        a = text[0].split(' ')[1:11]
                        a.extend(["cs(Cookie)", "cs(Referer)"])
                        a.extend(text[0].split(' ')[11:14])
                        a.extend(["sc-bytes", "cs-bytes"])
                        a.append(text[0].split(' ')[14])

                        f3.write(" ".join(map(str, a)))
                    else:
                        if len(text[i].split(' ')) == 14:
                            a = text[i].split(' ')[0:10]
                            a.extend(["-", "-"])
                            a.extend(text[i].split(' ')[10:13])
                            a.extend(["-", "-"])
                            a.append(text[i].split(' ')[13])

                            f3.write(" ".join(map(str, a)))
                        else:
                            if log_display == False:
                                print(file)
                                f4.write("##")
                                f4.write(file)                            
                                f4.write("\n")
                                log_display = True
                        
                            a = text[i].split(' ')
                            f4.write(" ".join(map(str, a)))
                            error_count += 1
                if log_display == True:                
                    print(error_count)
            elif "15_ex" in file:
                for i in range(1,len(text)):
                    if len(text[i].split(' ')) == 18:
                        a = text[i].split(' ')
                        f3.write(" ".join(map(str, a)))
                    else:
                        if log_display == False:
                            print(file)
                            f4.write("##")
                            f4.write(file)
                            f4.write("\n")
                            log_display = True
                        
                        a = text[i].split(' ')
                        f4.write(" ".join(map(str, a)))
                        error_count += 1
                if log_display == True:
                    print(error_count)
    f3.close()
    f4.close()
    

def manage_errors():

    for file in glob.glob('possible_errors.log'):  
        with open(file, 'r+') as f:
            text = f.readlines()
            
            f3 = open("Final_NR_NG.log", "a", encoding="utf-8")
            f5 = open("errors.log", "a", encoding="utf-8")
            log_name = []
            for i in range(len(text)):
                if "##" in text[i]:
                    log_name = text[i][2:]
                    f5.write(log_name)
                elif "##" not in text[i]:
                    if len(text[i].split(' ')) == 18:
                        a= text[i].split(' ')
                        f3.write(" ".join(map(str, a)))
                    else:
                        f5.write(" ".join(map(str,text[i].split(' '))))

    f3.close()
    f5.close()


def find_bot():

    for file in glob.glob('Final_NR_NG.log'):  
        with open(file, 'r+') as f:
            text = f.readlines()

            f7 = open("robots.log", "a", encoding="utf-8")
            f7.write("".join("##Robot"))
            f7.write("\n")

            bots = ["bot", "Bot", "slurp", "spider", "crawler", "zmeu", "facebookexternalhit", "BPImageWalker"]
            for i in range(1, len(text)):
                #print(text[i].split(' ')[4] + "       " +text[i].split(' ')[9])                
                bot = False
                for k in range(len(bots)):                    
                    if ((str(bots[k]) in text[i].split(' ')[9]) or (str(bots[k]) in text[i].split(' ')[4])):
                        bot = True

                ##### Create a column with a boolean 1 or 0 depending on if its HUMAN or NOT  
                if bot == True:
                    f7.write("".join("BOT"))
                    f7.write("".join("\n"))
                else:
                    f7.write("".join("HUMAN"))
                    f7.write("".join("\n"))
    
    f7.close()


def add_Geo_Ro():

    counter = 0
    for file in glob.glob('Final_NR_NG.log'):  
        with open(file, 'r+') as f:
            text = f.readlines()            
            # Add the names on the ##Fields bar
            f6 = open("Final.log", "a", encoding="utf-8")
            a = text[0].split(' ')[:17]
            a.extend(["robots", "country_name", "region_name", "city", "zip"])
            a.append(text[0].split(' ')[17])
            f6.write(" ".join(map(str, a)))

            for file1 in glob.glob('robots.log'):  
                with open(file1, 'r+') as f7:
                    robots = f7.readlines()

            for file2 in glob.glob('ip_locations.txt'):  
                with open(file2, 'r+', encoding="utf-8") as f8:
                    locations = f8.readlines()

            # Not the first field
            for i in range(1,len(text)): 
                if (text[i].split(' ')[0] != "date"):                 

                    a= text[i].split(' ')[1:17]
                    f6.write(" ".join(map(str, a)))
                    f6.write(" ".join(" "))
                    b = []
                    for k in range(len(locations)):
                        if (locations[k].split('|')[0].rstrip() == text[i].split(' ')[8].rstrip()): 
                            print(counter)
                            counter += 1
                            b.extend([robots[i].rstrip(), locations[k].split('|')[1], locations[k].split('|')[2], locations[k].split('|')[3], locations[k].split('|')[4].rstrip()])
                    
                    b.append(text[i].split(' ')[17])
                    f6.write("|".join(map(str, b)))


#reform()
#change_name()
#ip_transformation()
#same_columns()
#manage_errors()
#find_bot()
#add_Geo_Ro()
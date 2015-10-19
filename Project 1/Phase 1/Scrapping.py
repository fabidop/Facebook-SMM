from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import cPickle as pickle
import os

username=raw_input("Enter email : ")    
passw = raw_input("Enter password : ")
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)
firefoxProfile = FirefoxProfile()

def main():
    nodes=[]
    l=[]
    j=0
    driver.get("https://facebook.com")
    email = "email"    
    login="loginbutton"
    password="pass"
    emailelement = driver.find_element_by_name(email)
    passwordelement = driver.find_element_by_name(password)
    emailelement.send_keys(username)
    passwordelement.send_keys(passw)
    loginelement = driver.find_element_by_id(login)
    loginelement.click()
    time.sleep(3)
    nodes,l,j=intialize(nodes,l,j)      #function to resume scrapping from the pickeled list and counters
    while(j<1500):                      #For 1500 nodes, can be changed according to need"
        #print j
        print "For node", l[j]
        driver.get(l[j])
        driver.find_element_by_xpath("//div[@id='fbTimelineHeadline']/div[2]/div/a[3]").click()
        name=driver.find_element_by_xpath("//span[@id='fb-timeline-cover-name']").text
        time.sleep(3)
        #print name
        nodes.append(name)
        actions = ActionChains(driver)
        pp=driver.find_elements_by_xpath("//div[@class='fsl fwb fcb']/a")
        curr=len(pp)
        #print curr
        newfr=0
        while(curr != newfr and newfr <= 100 ): #Sampling to get first 100 friends, can be removed to consider all
            curr=len(pp)
            #print curr
            lastfrnd=pp[len(pp)-1]
            actions.move_to_element(lastfrnd)
            actions.perform()
            time.sleep(2)
            pp=driver.find_elements_by_xpath("//div[@class='fsl fwb fcb']/a")
            newfr=len(pp)
            #print newfr            
        for n in pp:
            t = n.text
            links=n.get_attribute("href")
            #print t
            nodes.append(t)
            l.append(links)
        #print("#")
        nodes.append("#")
        j=j+1
        y=remove(l);
        l=y
        print "Total Nodes visited",len(nodes)
        pickle.dump( l, open( "links.p", "wb" ) )
        pickle.dump( nodes, open( "nodes.p", "wb" ) )
        pickle.dump( j, open( "j.p", "wb" ) )

    nodes=[x.encode('UTF8') for x in nodes]
    print ("Nodes decoded ")
    normalizednodes,names,normalnames=normalize(nodes)
    normalizededges=edgeform(normalizednodes)
    writenodes(normalnames)
    print "Nodes Written to file"
    writeedges(normalizededges)
    print "Edges Written to file"
    writenodesnames(names)


def intialize(nodes,l,j):
    if os.path.exists("links.p") and os.path.exists("nodes.p") and os.path.exists("j.p"):
        print "loading values"
        nodes = pickle.load( open( "nodes.p", "rb" ) )
        l = pickle.load( open( "links.p", "rb" ) )
        j=pickle.load( open( "j.p", "rb" ) )
    else:
        j=0
        driver.find_element_by_xpath("//div[@id='pagelet_welcome_box']/ul/li[1]/div/div/a").click()
        time.sleep(3)
        currentURL = driver.current_url
        #print currentURL
        l.append(currentURL)
    return nodes,l,j    

def writeedges(edge):
    csv_out = open('edges.csv', 'wb')
    mywriter = csv.writer(csv_out,delimiter=',')
    e=[]
    for h in edge:
        t=str(h)
        e=t.split(",")
        mywriter.writerow(e)
    #print e
    csv_out.close()
  
  

def writenodes(p):
    csv_out = open('nodes.csv', 'wb')
    mywriter = csv.writer(csv_out,delimiter=',')
    for q in p:
        mywriter.writerow([q])
    csv_out.close()
    
def writenodesnames(p):
    csv_out = open('nodes_names.csv', 'wb')
    mywriter = csv.writer(csv_out,delimiter=',')
    i=1
    for q in p:
        mywriter.writerow([q,i])
        i=i+1
    csv_out.close()


def remove( l ):
    s=[]
    for o in l:
        if o not in s:
            s.append(o);
    return s;

def normalize(l):
    s=[]
    for o in l:
        if o not in s and o != '#':
            s.append(o) 
    node=s
    normal=[]
    i=1
    for o in node:
       normal.append(i)
       i=i+1
    #print node
    #print normal
    i=1
    for o in node:
        for j in range(0,len(l)):
            if l[j]==o:
                l[j]=i    
        i=i+1
    print "Nodes Anonymized"
    return l,node,normal

def edgeform(l):
    #print l
    #print len(l)
    i=0
    j=1
    edge=[]
    while(i<len(l)):
        #print i
        #print l[i]
        while(l[i+j]!="#"):
            frd=str(l[j])
            frd=str(l[i])+","+str(l[i+j])
            edge.append(frd)
            j=j+1
        #print j
        #print l[i+j+1]
        i=i+j+1
        j=1
    #print edge
    #print len(edge)
    s=[]
    for o in edge:
        if o not in s:
            s.append(o);
    edge=s
    print "Edges formed"
    return edge

if __name__ == '__main__':
    main()

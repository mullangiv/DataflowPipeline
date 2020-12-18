from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fastapi import Depends, FastAPI
from mangum import Mangum
import os, shutil, uuid, logging, boto3, inquirer, json
import result
app = FastAPI(root_path="/prod")

logger = logging.getLogger()

@app.post("/predict")
async def predict(content: str):

    def label_article(url_choice, label_definitions, response):
        chrome_options = webdriver.ChromeOptions()

        lambda_options = [
            '--autoplay-policy=user-gesture-required',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-update',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-domain-reliability',
            '--disable-extensions',
            '--disable-features=AudioServiceOutOfProcess',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-notifications',
            '--disable-offer-store-unmasked-wallet-cards',
            '--disable-popup-blocking',
            '--disable-print-preview',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-setuid-sandbox',
            '--disable-speech-api',
            '--disable-sync',
            '--disk-cache-size=33554432',
            '--hide-scrollbars',
            '--ignore-gpu-blacklist',
            '--ignore-certificate-errors',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-default-browser-check',
            '--no-first-run',
            '--no-pings',
            '--no-sandbox',
            '--no-zygote',
            '--password-store=basic',
            '--use-gl=swiftshader',
            '--use-mock-keychain',
            '--single-process',
            '--headless']

        for argument in lambda_options:
            chrome_options.add_argument(argument)    

        chrome_options.binary_location = "/opt/bin/chromium"
        
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get("https://www.fakerfact.org/try-it-out")
        driver.implicitly_wait(5) # delay ensures link loads from cnn
        inputElement = driver.find_element_by_xpath("//body/div[@id='root']/div[1]/div[1]/div[1]/form[1]/textarea[1]")
        inputElement.send_keys(url_choice)
        inputElement.send_keys(Keys.TAB)
        submit = driver.find_element_by_xpath("//button[contains(text(),'Submit')]")
        submit.send_keys(Keys.ENTER)
        driver.find_element_by_css_selector("div.d-flex.flex-column:nth-child(3) div.flex-grow:nth-child(2) div.container.mt-4 div:nth-child(1) form:nth-child(3) > button.btn.btn-primary:nth-child(3)").click()
        driver.implicitly_wait(5)

        try:
            walt_list = ((driver.find_element_by_xpath("//body/div[@id='root']/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]")).text).splitlines()
            opList = len(walt_list)
            label = walt_list[0]
            confidence = walt_list[1]
            confidence = confidence.replace("Similar", "Confident")
            output_definition = label_definitions.get(label)
            aiHTmsg = (driver.find_element_by_xpath("//div[contains(@class, 'h5 mb-4')]")).text
            aiHTmsg = str(aiHTmsg)
            aiHTmsg = aiHTmsg.replace("Walt","HT")
            response = (f"  AI Conclusion: {aiHTmsg}")
            response = response + (f"   Article Label: {label}   Confidence Score: {confidence}   Label Defintion: {output_definition}")
            
            if opList > 10:
                label1 = walt_list[2]
                confidence1 = walt_list[3]
                confidence1 = confidence1.replace("Similar", "Confident")
                output_definition1 = label_definitions.get(label)
                response = response + (f"   Article Label: {label1}   Confidence Score: {confidence1}   Label Defintion: {output_definition1}")
                label2 = walt_list[4]
                confidence2 = walt_list[5]
                confidence2 = confidence2.replace("Similar", "Confident")
                output_definition2 = label_definitions.get(label)
                response = response + (f"   Article Label: {label2}   Confidence Score: {confidence2}   Label Defintion: {output_definition2}")
                label3 = walt_list[6]
                confidence3 = walt_list[7]
                confidence3 = confidence3.replace("Similar", "Confident")
                output_definition3 = label_definitions.get(label)
                response = response + (f"   Article Label: {label3}   Confidence Score: {confidence3}   Label Defintion: {output_definition3}")
                label4 = walt_list[8]
                confidence4 = walt_list[9]
                confidence4 = confidence4.replace("Similar", "Confident")
                output_definition4 = label_definitions.get(label4)
                response = response + (f"   Article Label: {label4}   Confidence Score: {confidence4}   Label Defintion: {output_definition4}")
                label5 = walt_list[10]
                confidence5 = walt_list[11]
                confidence5 = confidence5.replace("Similar", "Confident")
                output_definition5 = label_definitions.get(label5)
                response = response + (f"   Article Label: {label5}   Confidence Score: {confidence5}   Label Defintion: {output_definition5}")
            
            elif opList > 8:
                label1 = walt_list[2]
                confidence1 = walt_list[3]
                confidence1 = confidence1.replace("Similar", "Confident")
                output_definition1 = label_definitions.get(label)
                response = response + (f"   Article Label: {label1}   Confidence Score: {confidence1}   Label Defintion: {output_definition1}")
                label2 = walt_list[4]
                confidence2 = walt_list[5]
                confidence2 = confidence2.replace("Similar", "Confident")
                output_definition2 = label_definitions.get(label)
                response = response + (f"   Article Label: {label2}   Confidence Score: {confidence2}   Label Defintion: {output_definition2}")
                label3 = walt_list[6]
                confidence3 = walt_list[7]
                confidence3 = confidence3.replace("Similar", "Confident")
                output_definition3 = label_definitions.get(label3)
                response = response + (f"   Article Label: {label3}   Confidence Score: {confidence3}   Label Defintion: {output_definition3}")
                label4 = walt_list[8]
                confidence4 = walt_list[9]
                confidence4 = confidence4.replace("Similar", "Confident")
                output_definition4 = label_definitions.get(label4)
                response = response + (f"   Article Label: {label4}   Confidence Score: {confidence4}   Label Defintion: {output_definition4}")

            elif opList > 6:
                label1 = walt_list[2]
                confidence1 = walt_list[3]
                confidence1 = confidence1.replace("Similar", "Confident")
                output_definition1 = label_definitions.get(label1)
                response = response + (f"   Article Label: {label1}   Confidence Score: {confidence1}   Label Defintion: {output_definition1}")
                label2 = walt_list[4]
                confidence2 = walt_list[5]
                confidence2 = confidence2.replace("Similar", "Confident")
                output_definition2 = label_definitions.get(label2)
                response = response + (f"   Article Label: {label2}   Confidence Score: {confidence2}   Label Defintion: {output_definition2}")
                label3 = walt_list[6]
                confidence3 = walt_list[7]
                confidence3 = confidence3.replace("Similar", "Confident")
                output_definition3 = label_definitions.get(label3)
                response = response + (f"   Article Label: {label3}   Confidence Score: {confidence3}   Label Defintion: {output_definition3}")

            elif opList > 4:
                label1 = walt_list[2]
                confidence1 = walt_list[3]
                confidence1 = confidence1.replace("Similar", "Confident")
                output_definition1 = label_definitions.get(label1)
                response = response + (f"   Article Label: {label1}   Confidence Score: {confidence1}   Label Defintion: {output_definition1}")
                label2 = walt_list[4]
                confidence2 = walt_list[5]
                confidence2 = confidence2.replace("Similar", "Confident")
                output_definition2 = label_definitions.get(label2)
                response = response + (f"   Article Label: {label2}   Confidence Score: {confidence2}   Label Defintion: {output_definition2}")

            elif opList > 2:
                label1 = walt_list[2]
                confidence1 = walt_list[3]
                confidence1 = confidence1.replace("Similar", "Confident")
                output_definition1 = label_definitions.get(label1)
                response = response + (f"   Article Label: {label1}   Confidence Score: {confidence1}   Label Defintion: {output_definition1}")

            response = response + ("   ---Article has no warning indicators---   ")
            result.Response = response
            print(response)

        except:
            try:
                too_short_alert = (driver.find_element_by_xpath("//ul[contains(@class, 'alert-danger')]")).text
                print(too_short_alert)

            except:
                print("Error Try Again")

    response = result.Response
    url_choice = content
    label_definitions = {'Journalism': 'Journalism focuses on sharing information. These articles do not attempt to persuade or influence the reader by means other than presentation of facts. Journalistic articles avoid opinionated, sensational or suspect commentary. Good journalism does not draw conclusions for the reader unless manifestly supported by the presented evidence. Journalistic articles can make mistakes, including reporting statements that are later discovered to be false, however the mark of good journalism is responsiveness to new information (via a follow up articles or a retraction) especially if it coutermands previously reported claims.', 'Wiki': 'Like Journalism, the primary purpose of Wiki articles is to inform the reader. Wiki articles do not attempt to persuade or influence reader by means other than presentation of the facts. Wiki articles tend to be pedagogical or encyclopedic in nature, focusing on scientific evidence and known or well studied content, and will highlight when a claim or an interpretation is controversial or under dispute.  Like Journalism, Wiki articles are responsive to new information and will correct or retract prior claims when new evidence is available.', 'Satire': 'Satirical articles are characteristically humorous, leveraging exaggeration, absurdity, or irony often intending to critique or ridicule a target. Claims in works of satire may be intentionally false or misleading, tacitly presupposing the use of exaggeration or absurdity as a rhetorical technique. Satirical articles can often be written in a journalistic voice or style for humorous intent.', 'Sensational': 'Sensational articles provoke public interest or excitement in a given subject matter. Sensational articles tend to leveraging emotionally charged language, imagery, or characterizations to achieve this goal. While sensational articles do not necessarily make false claims, informing the reader is not the primary goal, and the presentation of claims made in sensational articles can often be at the expense of accuracy.', 'Opinion': 'Opinion pieces present the author’s judgments about a particular subject matter that are not necessarily based on facts or evidence. Opinion pieces can be written in a journalistic style (as in “Op-Ed” sections of news publications). Claims made in opinion pieces may not be verifiable by evidence or may draw conclusions that are not materially supported by the available facts. Opinion pieces may or may not be political in nature, but often advocate for a particular position on a controversial topic or polarized debate.', 'Agenda Driven': 'Agenda Driven articles are primarily written with the intent to persuade, influence, or manipulate the reader to adopt certain conclusions. Agenda-driven articles may or may not be malicious in nature, but characteristically do not convince the reader by means of fact based argumentation or a neutral presentation of evidence. Agenda-driven articles tend to be less reliable or more suspect than fact based journalism, and an author of agenda-driven material may be less responsive to making corrections or drawing different conclusions when presented with new information.'}
    label_article(url_choice, label_definitions, response)
    response = result.Response
    return response

handler = Mangum(app)
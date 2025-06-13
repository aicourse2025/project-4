"""
    Summary generation
"""

import os
from openai import OpenAI
import pandas as pd

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY')

#get cleaned and clustered dataset of Amazon reviews
dataset_reviews = pd.read_csv("../data/top3_products.csv")  # replace with your actual path

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)


def get_completion(prompt, model="gpt-3.5-turbo"):
    """
    Get a completion from the OpenAI API using the specified model.

    Args:
        prompt (str): The input prompt to send to the model
        model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo"

    Returns:
        str: The model's response text
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

dataset_reviews["prompt"] = (
    dataset_reviews["positive_reviews"].fillna("") +
    "\n" + dataset_reviews["negative_reviews"].fillna(""))
# dataset_reviews["target"] = "Summarize the product based on the reviews."

for category, group in dataset_reviews.groupby("name"):
    COMBINED_REVIEWS = " ".join(group["prompt"].astype(str).tolist())

    # PROMPT_1 = f"""
    # Your task is to generate a short summary of the three products from a single category.
    # It should read like a review.
    # Write it in the style of product reviews on Consumer Reviews website,
    # The Verge, The Wirecutter.

    # What are the best qualities of each of those products?
    # You should also identify top complaints for each of those products.
    # What is the worst product in the category and why you should never buy it.

    # Summarize the review below, delimited by triple backticks, in at most 200 words.

    # Review: ```{COMBINED_REVIEWS}```
    # """


    PROMPT_1 = f"""
    You are an expert product reviewer writing a concise blog post to help customers choose the best product.

1. **Top 3 products in this category:**  
   - List the top 3 products.  
   - Highlight their key differences and unique selling points.  
   - Explain when a customer should choose one product over the others.

2. **Top complaints for each product:**  
   - Summarize the most common issues customers mention for each product.

3. **Worst product in the category:**  
   - Identify the product with the most negative feedback or poorest performance.  
   - Explain why customers should avoid it.

4. **Additional insights:**  
   - Include any recurring themes or patterns from the reviews.  
   - Mention notable features that impress or frustrate customers.  
   - Provide practical advice based on customer experiences.

---
Product 1: Echo (White)
Positive Reviews: love echo want device performs command alexa name.she 's constant companion kitchen sings tell joke share recipe tell story quote bible verse give weather forecast much more.if add additional device control light thermostat grandson really like alexa tell stories.this inanimate object begin feel like real person longer around love ... amazon echo become critical appliance kitchen admittedly bought echo serve yet another cool toy around ... 're finding 's great addition lives.the top used function family probably simple use timer function close second ability call artist want hear amazon prime music 's well worth buck month get music service sound quality device although audiophile worthy quite good.our family still exploring many great tool available alexa ... say without reservation 's great device household forget 's like alexa around alexa transformed life home chooses music listen `` alexa play music '' keep track shopping `` alexa reorder cat food '' make sure n't burn dinner `` alexa set 15 minute timer '' ... find asking thing 'm home disappointed n't looking forward buying `` smart home '' item help use even amazing echo amazon echo amazing also somewhat frustrating experience convenience brings timer turning connected light playing music corny joke amazing love machine also become little frustrating n't work immediately time 've mostly worked first try definitely day light wo n't turn asked sometimes take long time alexa respond command could internet issue still detracts experience awesome device enjoyed immensely useful informative entertaining part daily life giving u news update locally world information anything ask like word definition synonym antonym math science educational question ... name 's like book encyclopedia course entertainment-playing music bluetooth connection and/or amazon music playlist great amazing gadget whole family buy another one pretty decent information gathering tool bought two echo one wife one expected something along line siri google could follow many command say specific command get response also echo cant distinguish commercial one commercial come try answer question hears alexa also trying set wife 's echo phone calling ca n't pull page setup option there.we like still trying learn easy home automation starting point easy setup.easily connected home harmony setup gave u reason get phillip hue light could happier alexa work great `` '' time found location key especially playing tv alexa sometimes gear voice due location close speaker moved work better always getting better .... echo call soon video another device echo product ... amazon amazon cell phone fun productive bought gag gift wife returned gift bottle perfume us device every day music play shopping list get made daily news caught time alexa pretty good converting unit cook need know many tablespoon liter handsfree timer request easy find looking way add clever little device would highly recommend fact 'm buy one parent great product around purchased amazon echo mother 's day gift wife quickly become gift entire family sound quality speaker average play music either iheart radio connected bluetooth device quickly connects wifi house portable n't used alexa many home automated function light electronic ordering food online etc purchase wifi outlet likely try technology overall happy product lot fun lot fun play music game weather much however making phone call text message hope develop way determine able send text message phone call make call anyone choose united state app device feel google may better device advanced database sometimes alexa understand asking would think would able know fun however would 've probably purchased google tell probably able play music
Negative Reviews: work properly device stay connected wifi always disconnecting make product unusable alarm timer used work harmony time turn device priced overrated purchased google home past week lost contact wifi work perfectly harmony hub difficult setup echo even 5-6 time echo support ca n't figure wish could return late purchased without research unimpressed found opened tried programming awesome alexa basically nothing come 's listening device home wo n't anything unless pay amazon fact synced pandora account pointless spell want alexa play saying `` alexa play x station pandora play list '' rest family suppose know request one know pandora play list barely many complaint basically disappointed purchase lead believe radio future pay amazon music unlimited monthly bluetooth bummer on/off timer wonderfully designed device use fairly limited bought primarily use smart home control device however although allows turn light add timer control instruction instance tell echo turn light 30 minute tell turn immediately finding incredible disappointing n't know understand would hard add feature useless without prime matter asked either alexa n't know answer offered order item n't ask prime membership.could n't even get weather forecast right.kept giving forcast area 20 mile away.i returned it.by way whatever ask '' ok google '' get answer usually 99 correct.never asks pay 99 membership offer order something online me.do n't need n't want n't waste money could give lower rating would.this nothing speaker big one.it wireless even take outside w/o power source ask question alexa search answer expensive would like try google since return ca n't justify price everyone said give time like alexa gave much time realize return within time frame bad knowledgable many question miss interpreted replied understanding looking distance hear u minimal returned one purchased `` google '' one much better knowledgeable answer device recommend using phone app also making purchase usage item may available n't expect additional charge 'm thrilled either one keep google device hope better come future alexa malexa item useless play music voice recognition unless pay amazon prime amazon music account disconnected play music manual control blue tooth connection phone pointless half question ask n't know answer thing 's good far time weather basically expensive blue tooth speaker clock ever purchased want money back intuitive overly argumentative purchased item recommendation many existing owner however got home attempted set device frustrating instructions/faqs helpful echo could find nest thermostat could find half hue light argued fought alexa 45 minute finally started pick light comletely re-configuring thermostat could see would work found light would turn would change color brightness level run software company worked computer whole life quirky would recommend item get google home

---

Product 2: Amazon - Echo Plus w/ Built-In Hub - Silver
Positive Reviews: alexa rock present husband originally asked radio home office set relatively quick amazed sound quality loved versatility could specific radio station played random song well tell joke etc fun u looking getting smaller `` dot '' room commented would never get rid 's fun functional smart bulb handy well love amazon echo plus awesome purchased two amazon echo plus two dot plus four fire stick hub philip hue lamp family christmas 2017. i‚äôm happy purchase learning much alexa start daily routine alexa program whatever would like include news weather music horoscope also start day compliment think important alexa gave best chili recipe mean best it‚äôs called chili i. want husband use alexa stay organized business date reminder way go alexa review yesterday evening decided purchase amazon echo machine intrusive yeah guess could allow purchased home automation fantastic capability name capability subscription unprecedented amount music listen worth thing include sport travel recipe traffic home automation part lock door turn light random lighting vacation .. amazon echo plus wow echo plus demonstrated u best buy bit skeptical bought check wow impressed tell turn turn light living room family room bedroom also dim light need local weather forecast ask want listen christmas music yes want know distance someplace population city country yes 're still discovering seems limitless absolutely love amazon echo smart device hub take echo 've amazon echo dot year really wanted develop smart device usage around house upgraded echo great device use drop feature communicate others house especially upstairs without yell smart hub amazing attaching smart device much seamless 1st gen echo got time tell 2nd gen echo device worth echo plus purchased echo plus reading new generation upgraded improving sound integration controller price provided thought deal good value first generation unit well quick comparison two sound look etc perspective really n't lead think noticeable sound improvement improved aesthetic least price unit come quite bit addition philip bulb 'free smart move.overall think unit good purchase beginning home automation project alexa awesome joke rapping everyday new fact alexa awesome super easy pull phone check weather honestly never would always surprised walked outside whatever day every morning ask alexa whats weather give depth review day rest week ton skill alexa useful random shes must try also plus echo plus want start smart home dont need hub like echo piece buy compatible smart bulb nice update additional original echo like idea built-in hub control smart home device get them.sound quality marginally better n't buy echo audiophiles ... background music 's perfect that.my complaint date account home amazon echo must one make frustrating user particularly playing configuring music play room excited expand smart capability echo plus fantastically easy use smarthome hub easy setup fast responsive ton capability expanding daily look sound great currently use mine manage smart ‚äúthings‚äù like light bulb lamp smart switch even robot vac made automating lot daily breeze simplified life didn‚äôt know needed simplified definitely worth extra money go plus echo dot love alexa echo plus alight 's becoming part family echo plus much different discovered yet anyway echo 2nd generation n't echo 1st generation know echo plus echos-2nd generation dot 3 week thing think make difference better sound quality talking really connoisseur kind ear one like turn volume hue lightbulb great bought echo plus black friday extended sale hue lightbulb real bonus liked much went back bought pack hue bulb also sale loving whole system lightbulbNegative Reviews: /
Negative Reviews: /

---

Product 3: Amazon Echo Show Alexa-enabled Bluetooth Speaker with 7" Screen
Positive Reviews: practical easy setup well designed good sound everything alexa plus hd video always ready answer associated video text applicable show movie trailer also watch amazon video excellent on-demand security video amazon compatible camera voice activated message and/or video call amazon show owner alexa app holder highly recommended simple powerful little hesitant spend money get glad alexa always answer say command noticed probably 95 right command given love fact see thing screen news briefing picture/video 's nice also love video call option planning getting one grandma technologically advanced could sit table talk grandkids worth every penny terrific product jealous son showed u amazon show thing capable since aol eliminated instant messaging wife less able communicate office separate floor got two show two spot intercom easily use alexa music many thing probably start using smart home device alexa also control 's fun device seems getting better time returned nucleus gem beauty previously owned nucleus device similar device great device lot bug much returned device masterpiece tied alexa echo universe used intercom throughout house echo also used view thing even call people echo directly amazing piece hardware amazon proud developing beautiful device echo show first concerned funny looking angle saw picture item displayed local store decided take chance owner echo dot figured would work manner love work arlo pro screen great soon figured reason funny angle item angled screen work great setback recommendation would add auxiliary output rear also watch prime movie youtube video etc overall excellent product amazon 9.5/10 rating one best ai product used screen smart home device useful really ca n't compete google home show brings convenience without call primarily use show turn on/off smart light simple cooking measurement simple math travel time store location hour calling video calling .... everything else like news calendar weather already displayed screen definitely worth plan using minimum feature great addition amazon echo family love amazon echo show video display helpful good quality video audio sound better echo plus speaker search recipe use without flipping recipe book need know measurement conversion ask alexa learn cooking technique recommended cooking time ... endless list available answer great addition kitchen love play christmas music throughout home using echo device lot fun work like echo product .with smart accessory control home thermostat light etc alot expandable option feature expected already 6 amazon device 2 echo 's 4 dot 's expected device slightly different amazon device screen pleasantly surprised large number helpful feature screen could bring occasionally scroll suggestion across screen helpful 'm planning setting another one 93 year old mother house 'll get kick also delivers promise despite less friendly price point n't get sale amazon item well designed delivers promise hype product description emphasis item `` show '' 's surprise sound quality compare echo want convenience voice controlled screen phone product delivers 's value even greater paired smart device security cam another added bonus come friend family also show `` drop '' essentially visual phone call 's great checking elderly family require technically savvy best echo kitchen/living room lot echo device room house kind smart speaker also google home device .the echo show best device use living room kitchen screen bright sharp 's nice feature follow recipe watch video even listen music lyric displayed screen.it 's also best way see calendar entry shopping list
Negative Reviews: pas waited couple month review giving amazon time make product equal sony dash nearly decade ago n't screen provides nothing value ca n't turn amazon tip near zero customization ca n't even move clock side screen something sony dash nearly 10 year ago pandora prime music alarm seriously biggest fail run away half baked amazon disaster less useless doesn‚äôt work cloudcam less useless work amazon cloudcam purchased best buy allow monitor two cloud cam kitchen tech savvy numerous alexa device unable get work tried installing enabling amazon cloudcam skill made sure new update show show automatically updated first plugged final straw tech support rep told can‚äôt use show cloudcam‚äîand unable connect someone could actually solve problem useless help less useless actually make work echo show less useless
Please write the blog-style review article based on these reviews.


    Review: ```{COMBINED_REVIEWS}```
    """

    res = get_completion(PROMPT_1)

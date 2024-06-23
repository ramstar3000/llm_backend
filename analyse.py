import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from json import load, dump

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech




def speech_to_text(mp3_file):
   
    client = SpeechClient()

    with open(mp3_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = cloud_speech.RecognitionAudio(content=content)
    config = cloud_speech.RecognitionConfig(
        encoding=cloud_speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        t = ("Transcript: {}".format(result.alternatives[0].transcript))
   
    return t


   

  

def multiturn_generate_content_witness_statements(witness_statements):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid who help create summaries"""]
  )
  
  info = (model.generate_content(f"Here are the witness statements, please highlight any discrepencies, can you summarise them: {witness_statements} "))

  return info.text

def multiturn_generate_content_pass_one(case, summary):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid is rating if these documents are similar or not"""]
  )
  
  info = (model.generate_content(f"""We are given a case and we are currently evaluating case notes and witness statements for a project. When comparing these, we need to judge the similarity of these cases and if they can be used to build up an arguement.
                                  The case we are questioning is as follows: {case}
                                  The summary of our current statements  is as follows: {summary}

                                    Please reply with only an integer answer of similarity score which is an integer from 1 to 100 where 100 means they are very similar

                                    Higher the score the more similar the documents

"""))

  return info.text


def multiturn_generate_content(case, nda):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid who helps create summaries"""]
  )
  
  info = (model.generate_content(f"""We are given a case and we are currently evaluating case notes and witness statements for a project. When comparing these, we need to judge the similarity of these cases and if they can be used to build up an arguement.
                                  The case we are questioning is as follows: {case}
                                  The NDA we are questioning is as follows: {nda}

                                    Please highlight any discrepencies between the documents
"""))

  return info.text


def multiturn_generate_content2(case):
  vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""You are a legal aid who helps create summaries"""]
  )
  
  info = (model.generate_content(f"""
                                    The case we are questioning is as follows: {case}, please summarise the case succinctly
"""))

  return info.text


generation_config = {
    "max_output_tokens": 100,
    "temperature": 1,
    "top_p": 0.6,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


def multiturn_generate_content_pass_two(summary, case_one, case_two):
    vertexai.init(project="cambridge-law24cam-7858", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=["""You are a legal aid is rating which these documents is most similar to the original document"""]
    )

    info = (model.generate_content(f"""We are given a case and we are currently evaluating case notes and witness statements for a project. When comparing these, we need to judge the similarity of these cases and if they can be used to build up an argument.
                                  The summary of the statements we have our: {summary}
                                  Case 1 is: {case_one}
                                  Case 2 is: {case_two}
                                    If the summary we are questioning is more similar to Case 1 reply with ONLY: 1
                                    Otherwise reply ONLY: 2

"""))

    return info.text

# multiturn_generate_content()

def main():

    # text_info = get

    witness_message = """

TRADE MARKS ACT 1994 
 
IN THE MATTER OF 
Trade Mark application number 1234567 
in the name of Bloggins Ltd 
and  
opposition number 456789 by Mark Jonesi 
 
 
WITNESS STATEMENT 
 
1. I, Mark Jones, of 14 Acacia Avenue, London W32 1XY am the director of Bloggers 
plc, a position which I have held since 2010. The facts in this statement come from 
my personal knowledge or the records of my company and I am duly authorised to 
speak on my company’s behalf in the prosecution of this application.ii 
 
2. My company has been using its trade mark since March 2001, initially in its shop 
in Acacia Avenue but expanding online and to premises in Manchester in 2003, 
Leeds in 2003 and both Birmingham and Edinburgh in 2005.iii Attached at exhibit 
JS1 are press articles which discuss the opening of these shops. At exhibit JS2 I 
provide copies of advertisements which appeared in the press at the time to promote 
our shops’ opening.iv 
 
3. Although the business began by selling overcoats, by the time the Manchester 
shop opened we sold a wide variety of articles of clothing. Now shown to me is 
exhibit JS3, which shows archive prints from the relevant period (25 November 2012 
to 24 November 2017) of the clothing items available on our online site.v I confirm 
that the full range of items was also available in-store. The trade mark is clearly 
visible on the website. Exhibit JS3 also contains photographs of the labels attached 
to our products, which show the trade mark. These have been used throughout the 
relevant period.vi 
 
4. Evidence of the publicity my company and its trade mark have received is shown 
at exhibit JS4, in the form of articles which appeared in national newspapers and 
magazines in the relevant period, as well as advertisements placed by us. 
Advertising spend was roughly £350,000 in each year of the relevant period. 
Evidence of advertising breakdown by publication is at exhibit JS5.vii 
 
5. Turnover in the relevant period was as follows:  
2012/2013  £561,298 
2013/2014 £732,987 
2014/2015 £982,225 
2015/2016 £813,562 
2016/2017 £812,255 
 
6. Produced at exhibit JS5 is a selection of invoices dated within the relevant period 
which show sales of goods under our trade mark.viii 
 
7. The fact in this witness statement are true to the best of my knowledge and belief. 
 
SIGNED: 
 
 
DATED: 
 
 
 i Opposition and cancellation details only need to be provided if you are involved in tribunal proceedings. 
 ii The witness statement must be in the name of an individual, so it is important you say who is giving this 
evidence and where your information comes from. 
 iii The way in which you give information is not critical, as long as you explain the circumstances and try to 
support your claims (e.g. turnover figures) with documents (“exhibits”: see guidance notes). If you are bringing 
a claim under s. 3(6) (“bad faith”), you may not need to give details about sales like in this example but you 
should try to explain all the relevant facts regarding the filing of the trade mark, including, for example, why 
your interest in the mark is legitimate. Any documents you are able to provide to back up your claims should 
be filed as exhibits. 
 iv Providing independent evidence can help support your claims, particularly if it shows the range of 
goods/services you offered. Note how the documentary evidence (adverts) which supports the statements is 
introduced as exhibits. 
 v Evidence about how long the trade mark has been used and where it has been used (whether that is in a 
particular area or throughout the UK, or in the EU if it is an EU mark) is important.  
 vi It is important to make sure that you show which goods/services the trade mark has been used on, especially 
if you are applying for or relying on lots of different goods and services. Note how the witness confirms that 
the labels with the trade mark were used at the relevant time. 
 vii Press articles and adverts, as well as the amount spent on advertising, are helpful in showing how widely 
your mark has been publicised, especially if they were in national publications. 
 viii Invoices help support the claim to turnover made above. They sometimes also show the trade mark, the 
range of goods/services sold and how wide the geographical reach of the business is. 




    """

    nda = """

    
1
 
 
COMMITMENT TO CONFIDENTIALITY 
 
Between, the company P S.A.S with a capital of 3849045 €, 
Headquartered  at  1  rue  F.,  V.,  registered  in  the  MELUN  Trade  and  Companies  Register  under  number  000  000  000, 
represented by Mr. D. S., in his capacity as Chairman, 
hereinafter referred to as "P", 
On the one hand, 
 
And, the company _______________________ with a capital of _______________ €, 
Headquartered  at _______________________________,  registered with the  Registre  du Commerce et des Sociétés de 
_______________, under number _______________, represented by _______________, 
hereinafter referred to as "_______________", 
On the other hand, 
 
Hereinafter referred to jointly as the "Parties" or separately as a "Party". 
 
Whereas : 
The "Parties" will cooperate on joint projects within the scope of their respective normal activities, and will exchange 
technical and commercial information. 
The term "Confidential Information" includes, by way of non-limitative examples, databases, know-how, formulas, 
processes, drawings, sketches, photographs, plans, drafts, specifications, samples, reports, customer and supplier lists, 
pricing information, studies, results, inventions and ideas transmitted by one of the "Parties" to the other in connection 
with such projects.  
 
It has been agreed as follows: 
 
Each "Party" hereby acknowledges that any "Confidential Information" which may be made available to it by the 
other "Party", in any form whatsoever, is strictly confidential and may not be disclosed. 
 
The "Parties" therefore undertake, under the terms of this letter, to keep all such information confidential and, in 
particular, to : 
1. to use the "Confidential Information" only for the purposes of the project for which it was shared. The parties 
will refrain from using the "Confidential Information" that may be provided to them in any way that could be 
detrimental to the other "Party", i.e. its industrial and commercial activities, 
2. to limit by all appropriate means the total or partial distribution and use of the "Confidential Information" to 
employees and executives of their companies directly involved in the project. The "Parties" will take all 
necessary steps to ensure that their employees, managers and outside consultants keep the "Confidential 
Information" secret and confidential. 
3. the "Confidential Information" disclosed or made available by one of the "Parties" remains its property, to 
hand over to it, at its written request, any medium containing the "Confidential Information" disclosed or 
made available to it, or to destroy it.  
 
Each of the "Parties" acknowledges that the other "Party" would suffer certain and significant harm if it failed to 
comply with the confidentiality obligations contained in this letter.  
The "Parties" shall have no obligation with respect to any "Confidential Information" which is or may become public 
knowledge through no fault of their own. 
 
The "Parties" undertake to respect the commitments made in this letter for a period of 10 years (ten years) from the 
date of receipt of the "Confidential Information". 
 
To be effective, any amendment to this agreement must be in writing and signed by a duly authorized representative of 
the "Parties", their successor or assignee. 
This agreement is governed by French law and is subject to the exclusive jurisdiction of the Tribunal de Commerce de 
Melun. 
 
Signed in two original copies in Vaux-le-Pénil, on 21/03/2024 
 
For P,     For _______________, 
First name: D. S.    First name: _______________ 
Title : President     Title : _______________ 
Signature + stamp :    Signature + stamp : 
      


"""

    summary_witness = multiturn_generate_content_witness_statements(witness_message)

    nda_summary = multiturn_generate_content_witness_statements(nda)


    cross_compare = multiturn_generate_content(witness_message, nda)


    case_file = "cases.json"

    with open(case_file, 'r') as f:
        cases = load(f)

    print(type(cases))



    # Now we need to compare the summaries with the cases in the file

    # 2 pass

    # pass 1 check if any relevance to our original case

    scores = dict()

    info = """

    Easter Term
[2015] UKSC 31
On appeal from: [2013] EWCA Civ 1465
JUDGMENT
Starbucks (HK) Limited and another (Appellants) v
British Sky Broadcasting Group PLC and others
(Respondents)
before
Lord Neuberger, President
Lord Sumption
Lord Carnwath
Lord Toulson
Lord Hodge
JUDGMENT GIVEN ON
13 May 2015
Heard on 25 and 26 March 2015
Appellants Respondents
Michael Silverleaf QC Geoffrey Hobbs QC
Kathryn Pickard Iain Purvis QC
Guy Hollingworth
(Instructed by Dechert
LLP
)
(Instructed by King and
Wood Mallesons LLP
)
Page 2
LORD NEUBERGER: (with whom Lord Sumption, Lord Carnwath, Lord
Toulson and Lord Hodge agree)
1. This appeal raises the issue whether, as the appellants contend, a claimant
who is seeking to maintain an action in passing off need only establish a reputation
among a significant section of the public within the jurisdiction, or whether, as the
courts below held, such a claimant must also establish a business with customers
within the jurisdiction. It is an issue on which there is conflicting jurisprudence in
the common law world, and it is of particularly acute significance in the age of global
electronic communication.
The factual background
2. The claim in these proceedings relates to internet protocol television
(“IPTV”), which is a way of delivering TV or video content over the internet. There
are two main types of IPTV, “closed circuit” and “over the top”. Closed circuit IPTV
uses dedicated bandwidth on the provider’s network. It requires the subscriber to
have a set top box to receive the service, the signal for which is encrypted. In many
respects, closed circuit IPTV services are akin to traditional cable broadcasts.
However, in addition to linear television broadcasts, IPTV services typically include
catch-up facilities and other forms of video-on-demand. Over the top (“OTT”) IPTV
involves the signal being delivered via a standard broadband connection. OTT IPTV
can be viewed (with appropriate software applications) on any device with a
broadband connection.
3. The appellant claimants, Starbucks (HK) Ltd and PCCW Media Ltd, are
members of a substantial group based in Hong Kong headed by PCCW Ltd, and I
will refer to group members compendiously as “PCCM”. Since 2003, PCCM has
provided a closed circuit IPTV service in Hong Kong. The service was launched
under the name NOW BROADBAND TV, but in March 2006 the name was
changed to NOW TV, under which it has operated ever since. By 2012, after PCCM
had spent substantial sums on marketing, NOW TV had become the largest pay TV
operator in Hong Kong, with around 1.2m subscribers, covering over half the
households in Hong Kong. Having started with 23 channels it now has around 200,
and many of the programmes are PCCM’s, quite a few of them under brand names
using the word NOW. Although the name of the channel has always been English,
all PCCM’s programmes are in Mandarin or Cantonese, but the channel also carries
some English language programmes (including Sky News and Manchester United’s
channel, MUTV). Ninety per cent of PCCM’s pay TV revenue comes from
subscriptions, the balance coming from advertising.
Page 3
4. People in the United Kingdom cannot receive PCCM's closed circuit service.
No set top boxes for it have been supplied in the UK, no subscription has been
registered to a subscriber with a UK billing address, and there is no evidence of any
subscriptions having been paid for with credit or debit cards with billing addresses
in the UK. Consistently with this, PCCM has never held an Ofcom licence for
broadcasting in the UK. However, a number of Chinese speakers permanently or
temporarily resident in the UK in 2012 were aware of the NOW TV service through
exposure to it when residing in or visiting Hong Kong.
5. On the findings made by the trial judge, UK residents could also become
acquainted with the NOW TV service in three other ways by 2012. First, since July
2007, the Chinese language content had been accessible free of charge via PCCM’s
own websites. Secondly, programmes and trailers from the NOW TV service had
been available free of charge on PCCM’s “channel” on the YouTube website.
Thirdly, a few of PCCM’s programmes from its NOW TV service had been
available as videos-on-demand on various international airlines, three of which flew
into the UK, but none of whose in-flight magazines made reference to NOW TV.
6. PCCM had been giving consideration to expanding its NOW TV subscription
service internationally, including into the UK, since some time in 2009, when it
began discussions with a potential UK partner, and those discussions had been
continuing during 2012. In June 2012, PCCM had launched a NOW player “app” in
the UK, both on its website and via the Apple App Store, in order to warm up the
market for the launch of PCCM’s NOW TV on the platform of its proposed UK
partner. The app and the channels were to be targeted at the Chinese-speaking
population in the UK. By October 2012, just over 2,200 people in the UK had
downloaded the app.
7. Meanwhile, on 21 March 2012, the three respondent defendants, British Sky
Broadcasting Group PLC, British Sky Broadcasting Ltd and Sky IP International
Ltd, who are all part of the British Sky Broadcasting Group, and have been referred
to throughout these proceedings as “Sky”, announced that they intended to launch a
new IPTV service under the name NOW TV, as an OTT service. They subsequently
effected that launch in beta form in mid-July 2012.
8. The development of Sky’s NOW TV service had begun with a presentation
to their operating executives in late March 2011, and, after consulting an external
branding organisation, Sky chose the name “Sky Movies NOW” in September 2011.
However, further consideration suggested that it would be unwise to include the
word “Sky” in the name of the new service, and a consumer research agency was
instructed to address the naming issue. The agency recommended simply using the
word “Now”, and Sky decided to follow that advice, while including the phrase
“Powered by Sky” in the branding.
Page 4
The instant proceedings
9. On 19 April 2012, PCCM began these proceedings, seeking to prevent Sky
from using the name NOW TV in connection with its OTT IPTV service in the UK,
on the grounds that the use of that name amounted to passing off. (There was also a
claim that it infringed a trade mark registered in the name of PCCM. That claim was
dismissed by the courts below and is not pursued in this appeal.)
10. The claim came before Arnold J, and in the course of his judgment, he found
that a substantial number of Chinese speakers permanently or temporarily resident
in the UK were acquainted with PCCM’s NOW TV service through exposure to it
when residing in or visiting Hong Kong. He also found that PCCM’s NOW TV
service had acquired a reputation amongst members of the Chinese-speaking
community in the UK, based on their exposure to it via PCCM’s NOW TV
“channel” on the YouTube website and PCCM’s NOW TV websites (together “the
websites”) as well as the showing of PCCM’s programmes on international flights.
Arnold J held that this reputation was modest but more than de minimis.
11. However, Arnold J dismissed PCCM’s claim. He rejected the argument that
it was sufficient for PCCM to identify a body of people in the UK who associated
the mark NOW TV with its IPTV service in Hong Kong: they were not customers
in the UK, and therefore did not represent goodwill in the jurisdiction. He also
considered that the mere accessibility of PCCM’s material in the UK via the
websites did not give rise to a protectable goodwill, stating that “the key question is
whether the viewers of PCCM’s programmes in the [UK] were customers for its
service so as to give rise to a protectable goodwill in the UK” - [2012] EWHC 3074
Ch, [2013] FSR 29, para 147. Two paragraphs later, he said that the contention that
viewers in the UK of PCCM’s programmes on the websites represented goodwill
would, as he put it, stretch the concept of “customer” to breaking point. As he
explained, if it were otherwise, hundreds of television channels worldwide would
have customers, and hence protectable goodwill, in the UK, as a result of the
YouTube website. In para 150 of his judgment, he concluded that the reality was
that “PCCM's primary purpose in making programme content available via
YouTube, its own websites and international airlines was to promote its Hong Kong
business by encouraging people to subscribe in Hong Kong”. Therefore, he held that
PCCM’s “customers were its viewers in Hong Kong, but not viewers in the UK”,
and so its “business had goodwill in Hong Kong but not in the UK”, so that the
passing off claim failed.
12. Arnold J nonetheless added in para 158 that, if he had found PCCM to have
a protectable goodwill in the UK, he would have accepted that there was a likelihood
that a substantial number of UK viewers who were previously familiar with PCCM’s
NOW TV would wrongly believe that Sky’s NOW TV emanated from the same or
Page 5
a connected source. Arnold J gave PCCM permission to appeal against his decision
on the passing off claim.
13. PCCM’s appeal to the Court of Appeal was dismissed for reasons given by
Sir John Mummery, with whom Patten and Pitchford LJJ agreed – [2013] EWCA
Civ 1465, [2014] FSR 20. The Court of Appeal essentially agreed with Arnold J’s
analysis as briefly summarised in para 11 above. In the circumstances, they did not
need to deal with the issues raised in Sky’s respondent’s notice, in which it was
contended that Arnold J had erred in finding that (i) the reputation of PCCM's NOW
service in the UK was more than de minimis, and (ii) internet users visiting PCCM’s
website could access any video content from the UK at any relevant time.
14. With the permission of this Court, PCCM now appeals against the decision
of the Court of Appeal, upholding Arnold J’s dismissal of its passing off claim.
The issue on this appeal
15. As Lord Oliver of Aylmerton explained in Reckitt & Colman Products Ltd v
Borden Inc [1990] 1 WLR 491, “[t]he law of passing off can be summarised in one
short general proposition – no man may pass off his goods as those of another”. As
he immediately went on to say, a claimant, or a plaintiff as it was then, has to
establish three elements in order to succeed in a passing off action:
“First, he must establish a goodwill or reputation attached to the goods
or services which he supplies in the mind of the purchasing public by
association with the identifying ‘get-up’ (whether it consists simply of
a brand name or a trade description, or the individual features of
labelling or packaging) under which his particular goods or services
are offered to the public, such that the get-up is recognised by the
public as distinctive specifically of the plaintiff’s goods or services.
Secondly, he must demonstrate a misrepresentation by the defendant
to the public (whether or not intentional) leading or likely to lead the
public to believe that goods or services offered by him are the goods
or services of the plaintiff. Whether the public is aware of the
plaintiff’s identity as the manufacturer or supplier of the goods or
services is immaterial, as long as they are identified with a particular
source which is in fact the plaintiff. … Thirdly, he must demonstrate
that he suffers or … that he is likely to suffer, damage by reason of the
erroneous belief engendered by the defendant’s misrepresentation that
the source of the defendant’s goods or services is the same as the
source of those offered by the plaintiff.”
Page 6
16. It is common ground that, in order to succeed, a claimant in a passing off
action has to establish its claim as at the inception of the use complained of.
Although there is no decision of the House of Lords specifically to that effect, it is
supported by a number of Court of Appeal decisions, perhaps most clearly from
Anheuser-Busch Inc v Budejovicky Budvar NP [1984] FSR 413, 462, and it appears
to me that it must be right. Accordingly, as the Judge accepted, PCCM had to
establish the three elements (or, on one view of PCCM’s case on the first element,
an updated version of the three elements) identified by Lord Oliver, in relation to
the NOW TV mark for IPTV services as at 21 March 2012, the date when Sky went
public about its imminent intention to launch its IPTV service in the UK under the
name NOW TV.
17. Subject to the issues raised by Sky in their respondent’s notice, and based on
the conclusions reached by the Judge, PCCM established the second and third of the
three elements identified by Lord Oliver. The argument on this appeal has therefore
focussed on the first element, namely the requirement that PCCM must establish
what Lord Oliver referred to as “a goodwill or reputation attached to the goods or
services which he supplies in the mind of the purchasing public by association” with
the relevant “get-up”, viz. the mark NOW TV with PCCM’s IPTV service. The
Judge and the Court of Appeal thought that it was not enough for PCCM to establish
that it had a reputation among a significant number of people in this country, if it
had no goodwill in this country. Thus, they considered that the fact that there were
people in this country who associated NOW TV with PCCM’s product would not
satisfy the first element, if those people were not or had not been customers for
PCCM’s product in this country. They also considered that the fact that people in
this country had been exposed to PCCM’s NOW TV products via the websites and
the showing of PCCM’s programmes on international flights did not make them
customers for the purpose of establishing goodwill in this country. On behalf of Sky,
Mr Hobbs QC, who appeared with Mr Purvis QC and Mr Hollingworth, supported
these conclusions.
18. Mr Silverleaf QC, who appeared with Ms Pickard for PCCM, argued that the
courts below were wrong, and in particular that (i) it was sufficient for PCCM to
succeed in its passing off claim that it had established a reputation for the NOW TV
name in connection with its IPTV service among a significant number of people in
this country, even if they were not customers of PCCM’s IPTV services in this
country, but in Hong Kong, and (ii) in any event, PCCM had customers in this
country, because a significant number of people were PCCM’s customers in this
country by virtue of having been exposed to PCCM’s programmes on the websites
and on international flights.
Page 7
The House of Lords and Privy Council authorities and Anheuser-Busch
19. In the course of their excellent arguments, each counsel referred to a number
of judgments to support their respective cases. A degree of caution is appropriate
when considering these earlier cases, for two reasons. First, in many (but not all) of
the cases, the precise issue which this appeal raises was not being considered, and
therefore the judges may not have had that issue in the forefront of their minds or
have received full argument in connection with it. Secondly, (despite certifying in
its notice of appeal that PCCM would not be inviting this Court to depart from any
decision of the House of Lords) Mr Silverleaf argued that we should, if necessary,
develop the law so that it accords with their case: thus, it would not automatically
be enough to conclude that the reasoning in a previous decision of the House of
Lords effectively disposes of this appeal.
20. Nonetheless, it does appear that the courts in the United Kingdom have
consistently held that it is necessary for a claimant to have goodwill, in the sense of
a customer base, in this jurisdiction, before it can satisfy the first element identified
by Lord Oliver. That this has been the consistent theme in the cases can be well
established by reference to a series of House of Lords decisions, and a decision of
the Judicial Committee of the Privy Council, over the past century.
21. In AG Spalding & Bros v AW Gamage Ltd (1915) 32 RPC 273, 284, Lord
Parker of Waddington said that “the nature of the right the invasion of which is the
subject of [a] passing-off action” was “a right of property … in the business or
goodwill likely to be injured by the misrepresentation”, and, at least unless the
concept of goodwill is given a significantly wider meaning than that which it
naturally has, it would not extend to a mere reputation. Thus, in Inland Revenue
Commissioners v Muller & Co’s Margarine Ltd [1901] AC 217, 235, Lord Lindley
explained that goodwill “is inseparable from the business to which it adds value,
and, in my opinion, exists where the business is carried on”. As he went on to
explain, goodwill can have “a distinct locality” even within a particular jurisdiction.
Observations of Lord Macnaghten, Lord James of Hereford and Lord Brampton at
pp 224, 228 and 231-233 respectively were to much the same effect. Although the
observations were made in the context of a revenue case, they purported to be
general statements about the meaning of “goodwill”.
22. In T Oertli AG v EJ Bowman (London) Ltd [1959] RPC 1, the House of Lords
unanimously upheld a decision of the Court of Appeal, where Jenkins LJ had said
that it was “of course essential to the success of any claim in respect of passing-off
based on the use of a given mark or get-up that the plaintiff should be able to show
that the disputed mark or get-up has become by user in this country distinctive of
the plaintiff’s goods” – see at [1957] RPC 388, 397.
Page 8
23. In another passing off case, Star Industrial Co Ltd v Yap Kwee Kor [1976]
FSR 256, 269, Lord Diplock, giving the advice of the Privy Council, referred to and
relied on the observations of Lord Parker in Spalding. Lord Diplock explained that
“[g]oodwill, as the subject of proprietary rights, is incapable of subsisting by itself”,
having “no independent existence apart from the business to which it is attached”.
He went on to explain that it “is local in character and divisible”, so that “if the
business is carried on in several countries a separate goodwill attaches to it in each”.
24. In Erven Warnink BV v J Townend & Sons (Hull) Ltd [1979] AC 731, 752,
Lord Fraser of Tullybelton quoted Lord Diplock’s observations in Star Industrial
with approval. At pp 755-756, he went on to identify five “facts” which it was
“essential” for a plaintiff to establish in a passing off action, of which the first was
that “his business consists of, or includes, selling in England a class of goods to
which a particular trade name applies”. In the same case, Lord Diplock at p 742,
citing Spalding, identified “five characteristics which must be present in order to
create a valid cause of action for passing off”, which included “caus[ing] actual
damage to a business or goodwill of the [plaintiff]”. Viscount Dilhorne, Lord
Salmon and Lord Scarman agreed with both speeches.
25. In the passage in his speech in Reckitt & Colman, quoted in para 15 above,
Lord Oliver referred to “a goodwill or reputation … in the mind of the purchasing
public”, and at p 510, Lord Jauncey of Tullichettle referred to a requirement that
“the plaintiff’s goods have acquired a reputation in the market and are known by
some distinguishing feature”. Lord Bridge of Harwich (with “undisguised
reluctance”, albeit not in connection with the point at issue), Lord Brandon of
Oakbrook and Lord Goff of Chieveley agreed with both speeches.
26. The ratio of the decision of the Court of Appeal in Anheuser-Busch was
indisputably that, in order to support a passing off claim, the claimant must establish
goodwill in the form of customers for its goods or services within the jurisdiction.
In that case the importation from the United States of bottled beer under the
plaintiff’s BUDWEISER mark for use and sale in US military and diplomatic
establishments within the UK and other European countries did not entitle the
plaintiff to establish what Lord Oliver later stated was the first element of a passing
off claim in relation to the UK, at any rate outside those establishments. Oliver LJ
(later of course Lord Oliver) said at p 470 that the sales of 5,000,000 cases of bottles
over 12 years in US diplomatic and military establishments in European countries
were “sales for a very special market having no connection with the market in the
countries in which the consumption actually took place”; having said that, he
accepted that there could well be “a localised goodwill” within the diplomatic and
military establishments. He also emphasised that the fact that the BUDWEISER
mark may have had a reputation among a significant number of people in the UK
did not assist the plaintiff as it involved “confus[ing] goodwill, which cannot exist
in a vacuum, with mere reputation”, adding that “reputation which may, no doubt,
Page 9
and frequently does, exist without any supporting local business, … does not by
itself constitute a property which the law protects”. O’Connor and Dillon LJJ
expressed similar views at pp 471-472 and 476 respectively.
PCCM’s case
27. PCCM contends that, particularly in an age of global electronic
communication and relatively quick and cheap travel, it is inconsistent with
commercial reality and unrealistic in terms of practicality to treat the “reputation or
goodwill” associated with a mark for a particular product or service as limited to
jurisdictions in which there is a business with customers for the product or service,
and incapable of extending to jurisdictions in which the mark is simply associated
with the particular product or service as a matter of reputation. More specifically,
PCCM argues that, in any event, on the facts found by Arnold J, it had a sufficient
“goodwill or reputation” “in the mind of the purchasing public [in the United
Kingdom] by association with the identifying ‘get-up’” of NOW TV “attached to its
products and services”, namely its IPTV service, to satisfy the first element, as
identified by Lord Oliver, of its passing off claim.
28. On behalf of PCCM, Mr Silverleaf contended that the notion that goodwill
should be limited to jurisdictions where the claimant had business is wrong in
principle: the question of where the claimant had goodwill was a matter of fact and
evidence, not a matter of law. Further, in the present age of “international travel and
the presence of the internet”, he argued that it would be anachronistic and unjust if
there was no right to bring passing off proceedings, particularly in relation to an
electronically communicated service, in a jurisdiction where, as a matter of fact, the
plaintiff’s mark had acquired a reputation. He suggested that the mere fact that the
customers are in Hong Kong when they enjoy the service should not undermine
PCCM’s case that they have such a reputation here which deserves to be protected.
He also submitted that the law would be arbitrary if PCCM had no right to bring
passing off proceedings despite having a reputation in this country simply because
users did not pay when they viewed PCCM’s programmes free on the websites.
29. Mr Silverleaf contrasted what he suggested was the slight difference between
the present case and cases such as Sheraton Corporation of America v Sheraton
Motels Ltd [1964] RPC 202. In that case, Buckley J held that a United States hotel
company had a sufficiently arguable case for saying that it had goodwill in the UK
to justify an interlocutory injunction against use of its mark; the goodwill was based
on the fact that customers living in the United Kingdom booked rooms in the
plaintiff’s hotels through the plaintiff’s London office or through UK-based travel
agents.
Page 10
30. So far as authorities are concerned, Mr Silverleaf suggested that there was no
decision of the House of Lords which was inconsistent with this analysis, and, if we
concluded that there was, we should depart from it. He accepted that some of the
reasoning of the Privy Council in Star Industrial and the decision and reasoning of
the Court of Appeal in Anheuser-Busch were inconsistent with PCCM’s argument,
but rightly said that we were not bound by them. He also relied on some decisions
of the English courts to which I have not so far referred, some decisions of courts in
other common law jurisdictions, and the economic and practical realities of the early
21st century.
31. Lord Diplock’s suggestion in Star Industrial that, if business is carried on in
more than one country there is a separate goodwill in each country, has been
questioned in more than one domestic case. Thus, in two first instance decisions,
Graham J suggested that the geographical boundaries of any goodwill should be a
question of fact in each case, rather than one of law - see Baskin-Robbins Ice Cream
Co v Gutman [1976] FSR 545, 547-548 and Maxim’s Ltd v Dye [1977] 1 WLR 1155,
1159, 1162. Megarry V-C in Metric Resources Corporation v Leasemetrix Ltd
[1979] FSR 571, 579 also expressed some doubt about Lord Diplock’s view on this
point. And Lord Diplock’s analysis was described as not being “an exactly accurate
rendering of what was said in Inland Revenue Commissioners v Muller's Margarine”
by Lloyd LJ (with whom Jacob and Stanley Burnton LJJ agreed) in Hotel Cipriani
Srl v Cipriani (Grosvenor Street) Ltd [2010] EWCA Civ 110, [2010] RPC 485, para
99, although Lloyd LJ clearly considered that the actual decision in Star Industrial
was correct. As he concluded, however, in para 106, Anheuser-Busch was binding
authority “for the proposition that an undertaking which seeks to establish goodwill
in relation to a mark for goods cannot do so, however great may be the reputation of
his mark in the UK, unless it has customers among the general public in the UK for
those products”.
32. So far as Anheuser-Busch is concerned, as I have already indicated, the fact
that the decision proceeded on the basis that a plaintiff in a passing off action must
have goodwill, in the form of customers, in the jurisdiction did not represent any
departure from an approach already approved by the House of Lords. As Oliver LJ
pointed out at p 464, Lord Diplock in Erven Warnink at p 744 stated that a plaintiff
must have “used the descriptive term long enough on the market in connection with
his own goods and have traded successfully enough to have built up a goodwill for
his business”, and, as Oliver LJ then observed, this “emphasises the point that
goodwill (as opposed to mere reputation) does not exist here apart from a business
carried on here”. As Oliver LJ went on to say, the same feature “emerges with even
greater clarity from the decision of the Privy Council in Star Industrial”. And Dillon
LJ in Anheuser-Busch at pp 475-476 cited Spalding, Star Industrial and Inland
Revenue Commissioners v Muller to make the same point.
Page 11
33. A number of first instance, mostly interlocutory, cases were cited by Mr
Silverleaf to support his argument that there is or should be no requirement that a
claimant in a passing off action should be able to establish goodwill, as opposed to
mere reputation, in the jurisdiction concerned. I do not think that any of the decisions
in question assists PCCM.
34. In La Société Anonyme des Anciens Établissements Panhard et Levassor v
Panhard Levassor Motor Company Ltd [1901] 2 Ch 513, it is true that the French
motor car manufacturer plaintiffs, as Farwell J put it at p 516, “did not sell directly
in England”. However, as he went on to explain, “their cars were brought and
imported into England, … so that England was one of their markets”. As Dillon LJ
put it in Anheuser-Busch at pp 477-478, “the French plaintiffs there had a market
for their cars with the general public in this country through the importers who had
obtained licences from the third parties who had relevant patent rights and … the
reputation, when the cars were imported into this country, enured to the French
plaintiffs”. Nor does Sheraton help PCCM. As explained in para 29 above, the US
hotel company had a booking office and agents in London, so it had customers in
England. In Suhner & Co AG v Suhner Ltd [1967] RPC 336, Plowman J made no
conclusive finding that the plaintiff had goodwill in the UK, but it is clear that its
goods had been sold here - see at pp 337-338. In Globelegance BV v Sarkissian
[1974] RPC 603, Templeman J reviewed many of the authorities at pp 609-613, and
clearly accepted that it was necessary to have custom in this country, concluding
that “[p]ure advertisement is clearly insufficient [but taking] bookings [is] sufficient
[as is] carrying out orders in this country”. He then decided that the activities of the
plaintiff in that case, selling patterns to a department store, who then used the
patterns to make up dresses which were sold under the plaintiff’s mark, was enough.
35. In a significant number of other cases at first instance, it is clear that, well
before the Court of Appeal decision in Anheuser-Busch, Chancery Judges
considered that a plaintiff had to establish at least an arguable case that it had
business in the UK before it could obtain an interlocutory injunction against passing
off. Before turning to them, it is instructive to refer to Maxwell v Hogg (1867) LR 2
Ch 307, which appears to have been the first case in which an English court
specifically decided that mere reputation, without customers, was not enough to
found a passing off claim. The Court of Appeal held that the plaintiff’s advertising
campaign in respect of a proposed new newspaper called “Belgravia” with a view
to imminent publication did not give him any right to enjoin the defendant from
publishing a newspaper with the same name. Turner LJ, after mentioning the
inconvenience of a plaintiff who had not even used the mark being able to restrain
someone else from doing so, said at p 312 that the plaintiff had “neither given, nor
come under any obligation to give, anything to the world; so that there is a total want
of consideration for the right which he claims”. Cairns LJ at pp 313-314, explained
that the plaintiff had no “right of property” for which he could claim protection, as
Page 12
“there has been no sale, or offering for sale, of the articles to which the name is to
be attached”.
36. More recent cases which support Sky’s case include the decisions of
Pennycuick J in Alain Bernardin et Cie v Pavilion Properties Ltd [1967] RPC 581,
Brightman J in Amway Corporation v Eurway International Ltd [1974] RPC 82, and
Walton J in Athlete’s Foot Marketing Associates Inc v Cobra Sports Ltd [1980] RPC
343. In Alain Bernardin, Pennycuick J held that the plaintiffs could not obtain an
injunction against the use of the mark CRAZY HORSE in the UK, even though they
could establish a reputation here for its cabaret in Paris under that name. The
plaintiff’s problem was that they could not identify any business done in the UK,
either directly or indirectly (to use Farwell J’s expression in Panhard), in connection
with their “Crazy Horse Saloon” in Paris, and the mere distribution of
advertisements was not enough (hence Templeman J’s observation in Globelegance
[1974] RPC 603). In other words, there does not seem to have been any evidence of
any customers in England of the plaintiffs’ Paris establishment as opposed to people
in England who visited that establishment when they were in Paris (see at p 582).
37. Mr Silverleaf pointed out that the reasoning of Pennycuick J caused Sir
Nicolas Browne-Wilkinson V-C some concern in Pete Waterman Ltd v CBS United
Kingdom Ltd [1993] EMLR 27, 53-55. At pp 53-54, Sir Nicolas said that Pennycuick
J’s reasoning was based on the proposition that “even if the foreign trader has
customers here he cannot protect his reputation unless he has conducted some
business here”, whereas the Vice-Chancellor thought that the law was or should be
that “[i]f there is a use by the foreign trader in this country of his name for the
purposes of his trade, the piracy of that name is an actionable wrong”. But, as Mr
Hobbs pointed out, the decision in Alain Bernardin would have been the same if the
test identified by the Vice-Chancellor had been applied.
38. Turning now to the cases in other jurisdictions, PCCM contends that
decisions of the courts of Ireland, Canada, New Zealand, Australia, South Africa,
Hong Kong and Singapore are consistent with its argument that a claimant does not
have to establish goodwill, in the sense of actual customers, within the jurisdiction,
in order to establish a claim for passing off.
39. In C&A Modes v C&A (Waterford) Ltd [1978] FSR 126, the Supreme Court
of Ireland held that the plaintiff’s C&A department store in Belfast was entitled to
mount a claim in passing off in the Irish Republic. At p 139, Henchy J was clearly
unhappy about the decision in Alain Bernardin, and said that there were in the Irish
Republic “sufficient customers of [the] plaintiff’s business [in Belfast] to justify his
claim”. At pp 140-141, Kenny J rejected the argument that a passing off claim
‘should be limited to cases where the plaintiff had acquired some of its goodwill in
the Republic by user or trading in this country’, and pointed out that the plaintiff in
Page 13
that case had customers in the Republic, where it had “carried out extensive
advertising on television and radio and in the newspapers”. He also said that the
decision in Alain Bernardin was wrong. O’Higgins CJ agreed with Henchy J. I do
not find this decision of much assistance in this case. As Walton J said in Athlete’s
Foot at p 356, these judgments (at least arguably in the same way as the judgment
in Pete Waterman) show a “misapprehension” of the reasoning in Alain Bernardin:
“if there had been customers of the Crazy Horse business in England, in the sense
in which there were customers of the Sheraton Hotels business in England, the
decision in [Alain Bernardin] surely must have been the other way”.
40. The Canadian case relied on by PCCM, Orkin Exterminating Co Inc v Pestco
Co of Canada Ltd (1985) 19 DLR (4th) 90, is of no assistance. Although the
plaintiff’s business was conducted in the USA, it enjoyed thousands of Canadian
clients who used its pest control services for their properties in Canada. At p 101 of
his judgment in the Court of Appeal in Ontario, Morden JA specifically relied on
the fact that the plaintiff had goodwill “including having customers” in Canada,
although he did express disquiet about Lord Diplock’s notion in Star Industrial that
goodwill had to be divided up nationally.
41. The New Zealand decision referred to by PCCM, Dominion Rent A Car Ltd
v Budget Rent A Car Systems (1970) Ltd [1987] 2 TCLR 91, does not take matters
much further. The ultimate decision was that both parties were entitled to use the
name BUDGET in connection with their respective car hire businesses in New
Zealand, and that turned on the facts. At p 101, Cooke P said that he did not think
that Lord Diplock in Star Industrial should be understood as saying that goodwill
should be automatically divisible between jurisdictions, describing it as
“unnecessarily myopic to restrict this process to national boundaries”. The furthest
Cooke P went in the direction PCCM argues for was at pp 101-102, where he said
that he thought that “an Australian company’s reputation and goodwill can extend
to New Zealand (and vice versa)”, but, importantly, he added “and, at least if there
is a sufficient business connection with this country, will be entitled to protection
here”. At pp 106-107, he said that “the rental vehicle business in Australasia cannot
be divided into two mutually exclusive groups of customers, those who hire vehicles
for driving in Australia and those who hire vehicles for driving in New Zealand.
Obviously the same persons may do both”, thereby rejecting the contention that the
defendant only had customers in New Zealand and the plaintiff in Australia. In his
judgment, Somers J said at p 116 that a plaintiff in a passing off action “must show
an invasion of that intangible right of property compendiously described as goodwill
which can only exist in New Zealand when attached to a business having some
connection with this country”. At p 120, Casey J quoted with apparent approval the
view of Lord Fraser in Erven Warnink. Richardson J was “in general agreement”
with Cooke P and Somers J, and McMullin J was “in general agreement” with Cooke
P.
Page 14
42. Support for PCCM’s case may however be found in the decision of the
Federal Court of Australia in ConAgra Inc v McCain Foods (Aust) Pty Ltd (1992)
106 ALR 465, given by Lockhart J, with whom Gummow and French JJ agreed (and
gave judgments of their own). After a very full review of the common law authorities
(including those I have discussed above) on pp 473-501, Lockhart J said at p 504
that it was “no longer valid, if it ever was, to speak of a business having goodwill or
reputation only where the business is carried on”, relying on “[m]odern mass
advertising … [which] reaches people in many countries of the world”, “[t]he
international mobility of the world population” and the fact that “[t]his is an age of
enormous commercial enterprises”. He also said at p 505 that, in his view, “the ‘hard
line’ cases in England conflict with the needs of contemporary business and
international commerce”. He concluded on the next page that “it is not necessary …
that a plaintiff, in order to maintain a passing off action, must have a place of
business or a business presence in Australia; nor is it necessary that his goods are
sold here”, saying that it would be “sufficient if his goods have a reputation in this
country among persons here, whether residents or otherwise”. Two points should be
noted about this decision. First, the passing off claim nonetheless failed because the
plaintiff was held to have an insufficient reputation in Australia. Secondly, the High
Court of Australia has not considered this issue.
43. The approach of the Supreme Court of South Africa in Caterham Car Sales
& Coachworks Ltd v Birkin Cars (Pty) Ltd [1998] 3 All SA 175 (A) is to similar
effect – see at para 16. Indeed, at para 19, ConAgra was cited with approval.
However, once again, the claim failed on the ground of insufficiency of reputation.
44. As to Hong Kong, PCCM points out that, in Ten-Ichi Co Ltd v Jancar Ltd
[1989] 2 HKC 330, Sears J in the High Court on an application for an interlocutory
injunction seems to have held that mere reputation was enough to found a passing
off claim following an earlier Hong Kong High Court decision. However, more
recently, the Court of Final Appeal in In re Ping An Securities Ltd (2009) 12
HKCFAR 808, para 17, cited Lord Oliver in Reckitt & Colman to support the
(admittedly undisputed) proposition that a plaintiff “must establish a goodwill (in
the country or region) in a business in the supply of goods or services” under the
relevant get-up in order to maintain a claim in passing off.
45. Finally, Singapore. In Jet Aviation (Singapore) Pte Ltd v Jet Maintenance
Pte Ltd [1998] 3 SLR(R) 713, para 45, PCCM contends that Warren LH Khoo J in
the High Court appears to have followed ConAgra. I am not at all sure that he did:
see at para 42. However, it is unnecessary to decide that question, because more
recently, the Court of Appeal considered the issue in an impressively wide-ranging
judgment in Staywell Hospitality Group Pty Ltd v Starwood Hotels & Resorts
Worldwide Inc [2013] SGCA 65, [2014] 1 SLR 911. After briefly considering most
of the authorities to which I have referred (including the decision of Arnold J in this
case), Sundaresh Menon CJ, giving the judgment of the court, explained at para 135
Page 15
that the Singapore courts had “largely followed Star Industrial, holding that a
foreign trader which does not conduct any business activity in Singapore cannot
maintain an action in passing off here”, and that this “draws a clear distinction
between goodwill and reputation”.
46. However, as he explained in the next paragraph, this “hard line” approach
has been softened in one respect in Singapore (citing CDL Hotels International Ltd
v Pontiac Marina Pte Ltd [1998] 1 SLR(R) 975, para 58) namely where the plaintiff
has started “pre-business activities”, such as “embark[ing] on massive advertising
campaigns before the commencement of trading to familiarise the public with the
service or product”. Sundaresh Menon CJ explained at para 138 that this was
consistent with two English decisions, WH Allen & Co v Brown Watson Ltd [1965]
RPC 191 and British Broadcasting Corporation v Talbot Motor Co Ltd [1981] FSR
228, a view which derives some support from the judgment of Dillon LJ in Marcus
Publishing plc v Hutton-Wild Communications Ltd [1990] RPC 576, 584.
Discussion
47. Although I acknowledge that PCCM’s case is not without force (as is well
demonstrated by the reasoning in the judgments in ConAgra), I have reached the
conclusion that this appeal should be dismissed on the same ground on which it was
decided in the courts below. In other words, I consider that we should reaffirm that
the law is that a claimant in a passing off claim must establish that it has actual
goodwill in this jurisdiction, and that such goodwill involves the presence of clients
or customers in the jurisdiction for the products or services in question. And, where
the claimant’s business is abroad, people who are in the jurisdiction, but who are not
customers of the claimant in the jurisdiction, will not do, even if they are customers
of the claimant when they go abroad.
48. It seems to have been the consistent view of the House of Lords and Privy
Council from 1915 to 1990 that a plaintiff who seeks passing off relief in an English
court must show that he has goodwill, in the form of customers, in the jurisdiction
of the court. While it can be said that, in none of the cases discussed in paras 21-25
above was that point the main focus of attention, it nonetheless seems clear that that
is what a succession of respected judges, many of whom had substantial experience
in this area, considered to be the law. That conclusion is underlined by the reasoning
and conclusion in the judgments in Anheuser-Busch, and indeed the first instance
judgments discussed in paras 32-36 above.
49. It is of course open to this court to develop or even to change the law in
relation to a common law principle, when it has become archaic or unsuited to
current practices or beliefs. Indeed it is one of the great virtues of the common law
Page 16
that it can adapt itself to practical and commercial realities, which is particularly
important in a world which is fast changing in terms of electronic processes, travel
and societal values. Nonetheless, we should bear in mind that changing the common
law sometimes risks undermining legal certainty, both because a change in itself can
sometimes generate uncertainty and because change can sometimes lead to other
actual or suggested consequential changes.
50. In addition to domestic cases, it is both important and helpful to consider how
the law has developed in other common law jurisdictions – important because it is
desirable that the common law jurisdictions have a consistent approach, and helpful
because every national common law judiciary can benefit from the experiences and
thoughts of other common law judges. In the present instance, the Singapore courts
follow the approach of the UK courts, whereas the courts of Australia (subject to the
High Court holding otherwise) and South Africa seem to favour the approach
supported by PCCM. The position is less clear in other Commonwealth
jurisdictions. In the United States of America, the approach appears to be consistent
with that of the courts below in this case. Thus in Grupo Gigante SA De CV v Dallo
& Co Inc (2004) 391 F 3d 1088 the Court of Appeals for the 9th circuit said at p 1093
that “priority of trademark rights in the United States depends solely upon priority
of use in the United States, not on priority of use anywhere in the world. Earlier use
in another country usually just does not count”. Accordingly it does not appear to
me that there is anything like a clear trend in the common law courts outside the UK
away from the “hard line” approach manifested in the UK cases discussed in paras
21-26 and 32-36 above.
51. Particularly in the light of what has been said in some of the cases discussed
above, it appears that there are two connected issues which justify further discussion,
namely (i) clarification as to what constitutes sufficient business to give rise to
goodwill as a matter of principle, and (ii) resolution of the judicial disagreement as
to the jurisdictional division of goodwill described by Lord Diplock in Star
Industrial.
52. As to what amounts to a sufficient business to amount to goodwill, it seems
clear that mere reputation is not enough, as the cases cited in paras 21-26 and 32-36
above establish. The claimant must show that it has a significant goodwill, in the
form of customers, in the jurisdiction, but it is not necessary that the claimant
actually has an establishment or office in this country. In order to establish goodwill,
the claimant must have customers within the jurisdiction, as opposed to people in
the jurisdiction who happen to be customers elsewhere. Thus, where the claimant’s
business is carried on abroad, it is not enough for a claimant to show that there are
people in this jurisdiction who happen to be its customers when they are abroad.
However, it could be enough if the claimant could show that there were people in
this jurisdiction who, by booking with, or purchasing from, an entity in this country,
obtained the right to receive the claimant’s service abroad. And, in such a case, the
Page 17
entity need not be a part or branch of the claimant: it can be someone acting for or
on behalf of the claimant. That is why, as explained in Athlete’s Foot, the decision
in Panhard et Levassor and the observations in Pete Waterman are compatible with
the decision in Alain Bernardin.
53. As to Lord Diplock’s statement in Star Industrial that, for the purpose of
determining whether a claimant in a passing off action can establish the first of Lord
Oliver’s three elements, an English court has to consider whether the claimant can
establish goodwill in England, I consider that it was correct. In other words, when
considering whether to give protection to a claimant seeking relief for passing off,
the court must be satisfied that the claimant’s business has goodwill within its
jurisdiction.
54. It would be wrong to suggest that there is a rule of law that, whatever the
point at issue, goodwill has to be divided between jurisdictions, not least because
(unsurprisingly) we have not had an exhaustive analysis of all the circumstances in
which goodwill may have to be considered by the court. However, it seems to me
that, when it comes to a domestic, common law issue such as passing off, an English
court has to consider the factual position in the UK. That is well illustrated by the
fact that, even if PCCM’s argument was accepted and it was enough for a claimant
merely to establish a reputation, that reputation would still have to be within the
jurisdiction.
55. The notion that goodwill in the context of passing off is territorial in nature
is also supported by refusal of judges to accept that a court of one jurisdiction has
power to make orders in relation to the goodwill in another jurisdiction. I have in
mind the decisions of the House of Lords in Lecouturier v Rey [1910] AC 262, 265
per Lord Macnaghten, with whom Lord Atkinson and Lord Collins agreed, and at
pp 269-272 per Lord Shaw of Dunfermline, and the Privy Council in Ingenohl v
Wing On & Co (Shanghai) Ltd (1927) 44 RPC 343, 359-360, per Viscount Haldane
giving the advice of the Board. The territorial approach to goodwill is also apparent
in the context of trade marks in RJ Reuter Co Ltd v Mulhens [1954] Ch 50, 89 and
95-96 (per Lord Evershed MR and Romer LJ respectively) and Adrema Werke
Maschinenbau GmbH v Custodian of Enemy Property [1957] RPC 49, 54-55 and 59
(per Lord Evershed MR and Jenkins LJ). It is also worth mentioning that article 6
of the Paris Convention for the Protection of Industrial Property 1883 (last revised
1967 and last amended 1979) states, in para (1) that “registration of trademarks shall
be determined in each country … by its domestic legislation”, and in para (3) that a
duly registered mark is to be “regarded as independent of marks registered in other
countries of the Union”.
56. My view on the two issues discussed in paras 49-53 above is supported by a
brief extract from Lord Fraser’s speech in Erven Warnink at p 755, where he said
Page 18
that “the meaning of the name in … countries other than England is immaterial
because what the court is concerned to do is to protect the plaintiffs' property in the
goodwill attaching to the name in England and it has nothing to do with the
reputation or meaning of the name elsewhere”.
57. Indirect support for this approach is also to be found in decisions of the Court
of Justice of the European Union, which has emphasised in a number of decisions
the need for “genuine use” of a mark, namely “to guarantee the identity of the origin
of the goods or services for which it is registered, in order to create or preserve an
outlet for those goods or services”, and that this means “real commercial exploitation
of the mark in the course of trade, particularly the usages regarded as warranted in
the economic sector concerned as a means of maintaining or creating market share
for the goods or services protected by the mark” – to quote from Leno Merken BV v
Hagelkruis Beheer BV (Case C-149/11) EU:C:2012:816, para 29. Further, it is
relevant to note that the CJEU has also held that “the mere fact that a website
[advertising or selling the product or service concerned] is accessible from the
territory covered by the trade mark is not a sufficient basis for concluding that the
offers for sale displayed there are targeted at consumers in that territory” – L'Oreal
SA v eBay International AG (Case C-324/09) EU:C:2011:474 [2011] ECR I-6011,
para 64.
58. It is also of interest that, even in the context of the single market, the CJEU
has accepted that “because of linguistic, cultural, social and economic differences
between the Member States, a sign which is devoid of distinctive character or
descriptive of the goods or services concerned in one Member State is not so in
another Member State” – see Junited Autoglas Deutschland GmBH & Co KG v
Office for Harmonisation in the Internal Market (Trade Marks and Designs) (Case
T-297/13) EU:T:2014:893, para 31, citing Matratzen Concord AG v Hukla Germany
SA (Case C-421/04) EU:C:2006:164 [2006] ECR I-2303, para 25.
59. Professor Wadlow has, in my judgment, correctly summarised the position
in The Law of Passing-off - Unfair Competition by Misrepresentation 4
th ed, 2011,
para 3-131:
“The reason why goodwill is territorial is that it is a legal proprietary
right, existing or not in any jurisdiction according to whether the laws
of that jurisdiction protect its putative owner. Goodwill in the legal
sense is therefore something more than bare reputation …. The
distinction between goodwill in the legal sense and reputation in the
everyday sense is like that between copyright and the underlying
literary work. It may be surprising, and even inconvenient, that at the
moment a literary work is reduced to writing tens or hundreds of
legally distinct copyrights may simultaneously come into existence all
Page 19
over the world, but the nature of copyright as a legal right of property
arising in any given jurisdiction from national legislation, common
law or self-executing treaty means that it must be wrong to speak as if
there were a single international copyright.”
60. This analysis can be said with some justification to involve some fine
distinctions, and on some occasions to lead to some difficult questions of fact and to
result in some decisions which could appear rather harsh. However, any decision as
to what a claimant must show in order to establish the first element of Lord Oliver’s
trilogy of elements or requirements will involve fine distinctions, and will
sometimes involve difficult or harsh cases. I am unconvinced that if we accept the
conclusion of the courts below, supported by Sky, it would be likely to lead to more
arguable unfairnesses or difficulties than if we adopted PCCM’s case.
61. It is also necessary to bear in mind the balancing exercise underlying the law
of passing off, which Somers J described in Dominion Rent A Car at p 116 as “a
compromise between two conflicting objectives, on the one hand the public interest
in free competition, on the other the protection of a trader against unfair competition
by others”. More broadly, there is always a temptation to conclude that, whenever a
defendant has copied the claimant’s mark or get-up, and therefore will have
benefitted from the claimant’s inventiveness, expenditure or hard work, the claimant
ought to have a cause of action against the defendant. Apart from the rather narrower
point that passing off must involve detriment to the claimant, it is not enough for a
claimant to establish copying to succeed. All developments, whether in the
commercial, artistic, professional or scientific fields, are made on the back of other
people’s ideas: copying may often be an essential step to progress. Hence, there has
to be some balance achieved between the public interest in not unduly hindering
competition and encouraging development, on the one hand, and on the other, the
public interest in encouraging, by rewarding through a monopoly, originality, effort
and expenditure – the argument which is reflected in Turner LJ’s observation at p
312 in Maxwell v Hogg to the effect that a plaintiff who has merely advertised, but
not marketed, his product, has given no consideration to the public in return for his
claimed monopoly. In the instant case, the assessment of the appropriate balance
between competition and protection, which arises in relation to any intellectual
property right, must be made by the court, given that passing off is a common law
concept.
62. If it was enough for a claimant merely to establish reputation within the
jurisdiction to maintain a passing off action, it appears to me that it would tip the
balance too much in favour of protection. It would mean that, without having any
business or any consumers for its product or service in this jurisdiction, a claimant
could prevent another person using a mark, such as an ordinary English word,
“now”, for a potentially indefinite period in relation to a similar product or service.
In my view, a claimant who has simply obtained a reputation for its mark in this
Page 20
jurisdiction in respect of his products or services outside this jurisdiction has not
done enough to justify granting him an effective monopoly in respect of that mark
within the jurisdiction.
63. I am unpersuaded that PCCM’s case is strengthened by the fact that we are
now in the age of easy worldwide travel and global electronic communication. While
I accept that there is force in the point that the internet can be said to render the
notion of a single international goodwill more attractive, it does not answer the
points made in paras 51-59 above. Further, given that it may now be so easy to
penetrate into the minds of people almost anywhere in the world so as to be able to
lay claim to some reputation within virtually every jurisdiction, it seems to me that
the imbalance between protection and competition which PCCM’s case already
involves (as described in paras 60-62 above) would be exacerbated. The same point
can be made in relation to increased travel: it renders it much more likely that
consumers of a claimant’s product or service abroad will happen to be within this
jurisdiction and thus to recognise a mark as the claimant’s. If PCCM’s case were
correct, it would mean that a claimant could shut off the use of a mark in this
jurisdiction even though it had no customers or business here, and had not spent any
time or money in developing a market here - and did not even intend to do so.
64. A rather different factor which militates against PCCM’s case is section 56
of the Trade Marks Act 1994 which gives effect to article 6(bis) of the Paris
Convention) and is concerned with “well-known marks”. By virtue of subsection
(1), section 56 applies to a mark which is owned by a person who is domiciled or
has a business in a Convention country and which is “well-known in the United
Kingdom”. Section 56(2) entitles such a person to “restrain by injunction the use in
the United Kingdom of a trade mark which, or the essential part of which, is identical
or similar to his mark, in relation to identical or similar goods or services, where the
use is likely to cause confusion”. This provision is significant in the present context
because it substantially reduces the likelihood of the sort of harsh results referred to
at the start of para 60 above. It means that, where a mark which is used abroad and
has a reputation in this country, it still can be protected if it satisfies section 56(1),
even if the proprietor of the mark cannot establish any customers or sufficient
goodwill in this jurisdiction.
65. A more radical argument was advanced by Sky based on section 56 of the
1994 Act, namely that, by that section, the legislature decided on the circumstances
in which mere reputation in this country should be enough to justify protection being
accorded to a mark used in another country, and that the courts should not extend
the common law further than Parliament has thought it right to go. As Mr Hobbs put
it, if Parliament has decided that domestic reputation is enough in the case of a “wellknown” mark, it is not for the courts to extend the principle to marks which are not
“well-known”. Another, perhaps starker, way of putting the point is that, if PCCM’s
case is correct, it is hard to see what purpose section 56 of the 1994 Act would have.
Page 21
I see considerable force in that argument, but it is unnecessary to rule on it, and I
prefer not to do so.
66. Finally, a point which I would leave open is that discussed in the judgment
of Sundaresh Menon CJ in Staywell (see para 46 above), namely whether a passing
off claim can be brought by a claimant who has not yet attracted goodwill in the UK,
but has launched a substantial advertising campaign within the UK making it clear
that it will imminently be marketing its goods or services in the UK under the mark
in question. It may be that such a conclusion would not so much be an exception, as
an extension, to the “hard line”, in that public advertising with an actual and
publicised imminent intention to market, coupled with a reputation thereby
established may be sufficient to generate a protectable goodwill. On any view, the
conclusion would involve overruling Maxwell v Hogg, and, if it would be an
exception rather than an extension to the “hard line”, it would have to be justified
by commercial fairness rather than principle. However, it is unnecessary to rule on
the point, which, as explained in para 46, has some limited support in this
jurisdiction and clear support in Singapore. Modern developments might seem to
argue against such an exception (see para 63 above), but it may be said that it would
be cheap and easy, particularly for a large competitor, to “spike” a pre-marketing
advertising campaign in the age of the internet. It would, I think, be better to decide
the point in a case where it arises. Assuming that such an exception exists, I do not
consider that the existence of such a limited, pragmatic exception to the “hard line”
could begin to justify the major and fundamental departure from the clear, wellestablished and realistic principles which PCCM’s case would involve. In this case,
PCCM’s plans for extending its service into the UK under the NOW TV mark were
apparently pretty well advanced when Sky launched their NOW TV service, but the
plans were still not in the public domain, and therefore, even if the exception to the
“hard line” is accepted, it would not assist PCCM.
Conclusion
67. For these reasons, I conclude that PCCM’s appeal should be dismissed. Its
business is based in Hong Kong, and it has no customers, and therefore no goodwill,
in the UK. It is true that, according to the Judge, there are a significant number of
people who are, temporarily or in the longer term, members of the Chinese
community in the UK, with whom the mark NOW TV is associated with PCCM’s
IPTV service. In so far as they are customers of PCCM, they are customers in Hong
Kong, and not in the UK, because it is only in Hong Kong that they can enjoy the
service in question, and the service is not marketed, sold or offered in the UK. The
people in the UK who get access to PCCM’s NOW TV programmes via the
websites, or on various international airlines, are not PCCM customers at any rate
in the UK, because there is no payment involved (either directly by the people
concerned or indirectly through third party advertising), and the availability of
PCCM’s product in these outlets simply was intended to, and did, promote PCCM’s
Page 22
Hong Kong business. Basically, it simply amounted to advertising in the UK, and,
as explained above, a reputation acquired through advertising is not enough to found
a claim in passing off.
68. Given that we are dismissing the appeal, it is unnecessary to consider Sky’s
other arguments to support this conclusion which were the same as those which it
would have raised before the Court of Appeal in its respondent’s notice (see para 13
above). If we had allowed PCCM’s appeal, because the Court of Appeal
understandably did not address those issues we would have remitted the case to the
Court of Appeal to consider them.

"""

    # for case in cases:
    #    # information = cases[case]

    #    information  = info


    
    #    try:
    #         summary = multiturn_generate_content_pass_one(information, summary_witness+nda_summary)
    #         print(summary)

    #         scores[case] = summary
    

    #         with open('scores.json', 'w') as f:
    #                 dump(scores, f)
    
    #    except Exception as e:
            
    #         continue


    with open('scores2.json', 'r') as f:
       scores = load(f)

    with open('cases.json', 'r') as f:
       cases = load(f)




    # Each case has a score in the scores dictionary
    # We will now sort the cases by their scores

    # Initialise all scores to 0 in cases
    for case in cases:
        cases[case] += "00"


    for case in scores:
        cases[case] += str(scores[case])

    sorted_cases = sorted(cases.keys(), key=lambda x: cases[x][-2::], reverse=True)

    sorted_cases = sorted_cases[:5]
    print(sorted_cases)

    current_max = None
    current_max_index = 0
    sorted_keys = []
    for i in range(5):
        current_max = None
        for case in sorted_cases:
            if current_max is None:
                current_max = case
            else:
                response = multiturn_generate_content_pass_two(summary_witness+nda_summary, cases[current_max], cases[case])
                if '2' in response:
                    current_max = case
                    current_max_index = i
        print(current_max)
        sorted_keys.append(current_max)
        sorted_cases.remove(current_max)


    output = []

    for key in sorted_keys:
        case = (cases[key])

        summary = multiturn_generate_content2(case)
        output.append(summary)

    print(sorted_keys)
    return sorted_keys
    

    
    
    





if __name__ == '__main__':
   main()





    # extract_information('NDA 1.pdf')
    # multiturn_generate_content()